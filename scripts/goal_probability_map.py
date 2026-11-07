"""Probability of a goal as a function of where the ball centre crosses the goal plane, P(goal | y, z).

Usage:  PYTHONPATH=src .venv/bin/python scripts/goal_probability_map.py [--noise rounding] [--draws 24] [--procs 4]

Method. Gravity, drag, Magnus, seam and (uniform) wind forces do not depend on position, so translating the launch point by
(0, dy, dz) translates the whole trajectory rigidly. A posterior shot can therefore be steered onto any target crossing point
while keeping its speed, spin, incidence angle and air parameters. For each target point we draw posterior samples of the final
model (kick prior), shift their launch point so that they cross at the target, and fly them through the frame-impact model with
e_x ~ U(0, 0.2), mu ~ U(0.2, 0.8), e_n offset ~ N(0, 0.03) drawn per shot.

Two 1-D scans are computed: across the post (y varies, z = 1.2 m) and across the crossbar (z varies, y = 1.5 m). Far from the
frame the outcome is decided by geometry alone (inside: goal, outside: miss). Writes results/final/goal_map_<noise>.json.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_stage5 import CURVES, FORCES, sample_params  # noqa: E402

from penalty.collision import CLEAN_GOAL, GOAL_OFF_FRAME, MISS, MISS_OFF_FRAME, FrameImpact, resolve  # noqa: E402
from penalty.constants import P0  # noqa: E402

OUTCOMES = (CLEAN_GOAL, GOAL_OFF_FRAME, MISS_OFF_FRAME, MISS)


def _job(args):
    th, curve, entry, target, seed = args
    rng = np.random.default_rng(seed)
    imp = FrameImpact(e_x=rng.uniform(0.0, 0.2), mu=rng.uniform(0.2, 0.8), e_n_offset=rng.normal(0.0, 0.03))
    v0, ball, p = sample_params(th, curve)
    r0 = P0 + np.array([0.0, target[0] - entry[1], target[1] - entry[2]])
    out, _ = resolve(r0, v0, FORCES, p, ball=ball, imp=imp)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--noise", default="rounding")
    ap.add_argument("--draws", type=int, default=24)
    ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args()
    rng = np.random.default_rng(7)
    pool_th, pool_en, pool_c = [], [], []
    for c in CURVES:
        d = np.load(ROOT / "results" / "raw" / f"stage4_{a.noise}_final_kick_{c}.npz")
        ok = np.all(np.isfinite(d["entries"]), axis=1)
        pool_th.append(d["samples"][ok]); pool_en.append(d["entries"][ok]); pool_c += [c] * int(ok.sum())
    th, en = np.concatenate(pool_th), np.concatenate(pool_en)
    scans = {"post": [(y, 1.2) for y in np.round(np.arange(3.30, 4.001, 0.02), 3)],
             "crossbar": [(1.5, z) for z in np.round(np.arange(2.10, 2.801, 0.02), 3)]}
    jobs, keys = [], []
    for name, pts in scans.items():
        for t in pts:
            for _ in range(a.draws):
                i = int(rng.integers(len(th)))
                jobs.append((th[i], pool_c[i], en[i], t, int(rng.integers(1 << 31))))
                keys.append((name, t))
    with Pool(a.procs) as pool:
        outs = pool.map(_job, jobs, chunksize=4)
    res = {}
    for (name, t), o in zip(keys, outs):
        res.setdefault(name, {}).setdefault(t, []).append(o)
    report = {"noise": a.noise, "draws_per_point": a.draws, "posterior": "final model, kick prior", "scans": {}}
    for name, d in res.items():
        rows = []
        for t, os_ in sorted(d.items()):
            rows.append({"y": t[0], "z": t[1], **{o: os_.count(o) / len(os_) for o in OUTCOMES},
                         "p_goal": (os_.count(CLEAN_GOAL) + os_.count(GOAL_OFF_FRAME)) / len(os_)})
        report["scans"][name] = rows
    out = ROOT / "results" / "final"; out.mkdir(parents=True, exist_ok=True)
    (out / f"goal_map_{a.noise}.json").write_text(json.dumps(report, indent=1))
    for name, rows in report["scans"].items():
        print(name, [(r["y"] if name == "post" else r["z"], round(r["p_goal"], 2)) for r in rows])


if __name__ == "__main__":
    main()
