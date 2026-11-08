"""Stage 5: decide goal or no goal for posterior samples that reach the frame, and check Stage 4 convergence by split halves.

Usage:  PYTHONPATH=src .venv/bin/python scripts/run_stage5.py --noise tracking [--max-contacts 3000] [--procs 11]
        PYTHONPATH=src .venv/bin/python scripts/run_stage5.py --model final --spin-prior kick --noise rounding
        PYTHONPATH=src .venv/bin/python scripts/run_stage5.py --model final --spin-prior kick --noise rounding --chain no_wind
  (--model final reads the unified-model chains results/raw/stage4_<noise>_final_<spin prior>_<curve>.npz, wind included,
   and writes results/final/goal_probability_<noise>_<spin prior>.json)

For every pooled Stage 4 posterior sample (results/raw/stage4_<noise>_<curve>.npz):
* centre crossing far inside the frame (distance to frame ≥ R + 2 r_p + 0.05 m) → clean goal;
* far outside → miss;
* otherwise (a candidate for frame contact) → full 3-D event-driven flight with the frame-impact model (collision.py), with the impact
  parameters drawn per sample: e_x ~ U(0, 0.2), μ ~ U(0.2, 0.8), e_n offset ~ N(0, 0.03) (no football-on-goalpost data exists).
P(goal) = P(clean goal) + P(candidate) · P(goal | candidate).
Also reports split-half posterior quantiles of the entry point (first versus second half of each chain) as a convergence diagnostic.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import json
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from penalty.bayes import TWO_PI, physics, spin_basis_vec
from penalty.coefficients import LIFT_MODELS, ConstantCD
from penalty.collision import CLEAN_GOAL, GOAL_OFF_FRAME, MISS, MISS_OFF_FRAME, FrameImpact, resolve
from penalty.constants import P0, Air, Ball, Goal
from penalty.forces import AeroParams, drag, gravity, magnus, seam_force
from penalty.outcome import distance_to_frame

ROOT = Path(__file__).resolve().parents[1]
CURVES = ["kray2014_re462", "kray2014_re_interp", "asai2007_re455", "asai2007_re_interp"]
FORCES = [gravity, drag, magnus, seam_force]


def sample_params(th, curve):
    v0 = th[:3]
    e1, e2 = spin_basis_vec(v0[None, :])
    spin = th[3] * e1[0] + th[4] * e2[0]
    ph = physics(th[None, :])
    ball = Ball(mass=float(ph["mass"][0]), radius=float(ph["radius"][0]))
    air = Air(density=float(th[6]), kinematic_viscosity=float(ph["nu"][0]))
    wind = np.array([th[12], th[13], 0.0]) if len(th) >= 14 else np.zeros(3)
    return v0, ball, replace(AeroParams(), ball=ball, air=air, drag_model=ConstantCD(float(th[5])), spin=spin,
                             lift_model=LIFT_MODELS[curve], seam_coeffs=(float(th[10]), float(th[11])), wind=wind)


def _job(args):
    th, curve, seed = args
    rng = np.random.default_rng(seed)
    imp = FrameImpact(e_x=rng.uniform(0.0, 0.2), mu=rng.uniform(0.2, 0.8), e_n_offset=rng.normal(0.0, 0.03))
    v0, ball, p = sample_params(th, curve)
    out, info = resolve(P0, v0, FORCES, p, ball=ball, imp=imp)
    return out, info["impacts"]


def split_half(entries):
    ok = np.all(np.isfinite(entries), axis=1)
    e = entries[ok]
    h = len(e) // 2
    q = lambda x: np.percentile(x, [16, 50, 84])
    return {"y_first": q(e[:h, 1]).round(4).tolist(), "y_second": q(e[h:, 1]).round(4).tolist(),
            "z_first": q(e[:h, 2]).round(4).tolist(), "z_second": q(e[h:, 2]).round(4).tolist()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--noise", default="tracking")
    ap.add_argument("--max-contacts", type=int, default=3000)
    ap.add_argument("--procs", type=int, default=11)
    ap.add_argument("--model", choices=("stage4", "final"), default="stage4")
    ap.add_argument("--spin-prior", choices=("lognormal", "kick"), default="kick")
    ap.add_argument("--chain", default=None,
                    help="with --model final: one sensitivity chain instead of the four pooled C_L curves, e.g. no_wind (= Stage 5)")
    a = ap.parse_args()
    prefix = f"final_{a.spin_prior}_" if a.model == "final" else ""
    rng = np.random.default_rng(42)
    g, rp = Goal(), 0.06
    counts = {CLEAN_GOAL: 0, MISS: 0}
    cand, split = [], {}
    n_total = 0
    files = [(a.chain, "kray2014_re462")] if a.chain else [(c, c) for c in CURVES]   # sensitivity chains use the Kray curve
    for f, c in files:
        d = np.load(ROOT / "results" / "raw" / f"stage4_{a.noise}_{prefix}{f}.npz")
        th, en = d["samples"], d["entries"]
        split[f] = split_half(en)
        for i in range(len(th)):
            if not np.all(np.isfinite(en[i])):
                counts[MISS] += 1; n_total += 1; continue
            y, z = en[i, 1], en[i, 2]
            R = th[i, 9] / TWO_PI
            dist = distance_to_frame(y, z)
            inside = abs(y) < g.half_width and z < g.height
            n_total += 1
            if dist >= R + 2 * rp + 0.05:
                counts[CLEAN_GOAL if inside else MISS] += 1
            else:
                cand.append((th[i], c))
    n_cand = len(cand)
    pick = rng.choice(n_cand, size=min(a.max_contacts, n_cand), replace=False) if n_cand else []
    jobs = [(cand[k][0], cand[k][1], 1000 + j) for j, k in enumerate(pick)]
    with Pool(a.procs) as pool:
        res = pool.map(_job, jobs, chunksize=8)
    outs = [r[0] for r in res]
    frac = {o: outs.count(o) / len(outs) for o in (CLEAN_GOAL, GOAL_OFF_FRAME, MISS_OFF_FRAME, MISS)} if outs else {}
    p_cand = n_cand / n_total
    p_goal = counts[CLEAN_GOAL] / n_total + p_cand * (frac.get(CLEAN_GOAL, 0) + frac.get(GOAL_OFF_FRAME, 0))
    se = np.sqrt(p_goal * (1 - p_goal) / max(len(outs), 1)) * p_cand
    report = {"model": a.model, "spin_prior": a.spin_prior if a.model == "final" else "lognormal", "noise": a.noise, "n_samples": n_total, "p_far_clean_goal": counts[CLEAN_GOAL] / n_total,
              "p_far_miss": counts[MISS] / n_total, "p_near_frame": p_cand, "n_resolved": len(outs),
              "near_frame_outcomes": frac, "p_goal": p_goal, "p_goal_mc_se": float(se),
              "impact_priors": {"e_x": "U(0, 0.2)", "mu": "U(0.2, 0.8)", "e_n_offset": "N(0, 0.03)"},
              "split_half_quantiles": split}
    out = ROOT / "results" / ("final" if a.model == "final" else "stage5"); out.mkdir(parents=True, exist_ok=True)
    name = f"goal_probability_{a.noise}_{a.spin_prior}.json" if a.model == "final" else f"goal_probability_{a.noise}.json"
    if a.chain:
        name = name.replace(".json", f"_{a.chain}.json")
    (out / name).write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "split_half_quantiles"}, indent=2))
    for c, v in split.items():
        print(f"  split-half {c:22s} y16/50/84 {v['y_first']} vs {v['y_second']}   z {v['z_first']} vs {v['z_second']}")


if __name__ == "__main__":
    main()
