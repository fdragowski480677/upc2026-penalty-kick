"""The goalkeeper's view: how fast does the prediction sharpen when the ball is observed for longer?

Usage:  PYTHONPATH=src .venv/bin/python scripts/observation_horizon.py [--procs 11] [--nsteps 5000]

Truth: the final-model posterior sample (kick prior, Kray C_L curve, main case) whose entry point is closest to the most probable
entry point, i.e. a trajectory fully consistent with the given test case. Its positions are generated every 0.05 s up to a last
observation time T = 0.10 ... 0.35 s (the ball reaches the goal at about 0.40 s) and the full Bayesian inference of the final model is
run on them, for two noise models:
  rounding: positions rounded to 1 cm, likelihood sigma = 2.9 mm (as the main case);
  tracking: Gaussian noise sigma = 1 cm.
Recorded per T: the 68 % / 95 % half-widths of y and z, the error of the most probable point, and the posterior spin interval.
Writes results/final/observation_horizon.json.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import json
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from penalty.bayes import TWO_PI, Priors, physics, sample, summarise, unpack
from penalty.coefficients import LIFT_MODELS
from penalty.constants import P0, Observation
from penalty.fastsim import Settings, crossings, positions

ROOT = Path(__file__).resolve().parents[1]
CURVE = "kray2014_re462"
SIGMA = {"rounding": 0.01 / np.sqrt(12), "tracking": 0.01}
T_LAST = (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)


def truth():
    d = np.load(ROOT / "results" / "raw" / f"stage4_rounding_final_kick_{CURVE}.npz")
    mode = json.load(open(ROOT / "results" / "final" / "summary_final_rounding.json"))["by_spin_prior"]["kick"]["mode_yz"]
    ok = np.all(np.isfinite(d["entries"]), axis=1)
    th, en = d["samples"][ok], d["entries"][ok]
    i = int(np.argmin(np.hypot(en[:, 1] - mode[0], en[:, 2] - mode[1])))
    return th[i]


def run(args):
    noise, T, th, kw = args
    st = Settings(LIFT_MODELS[CURVE])
    times = tuple(np.round(np.arange(0.05, T + 1e-9, 0.05), 2))
    pos = positions(P0, *unpack(th[None]), st, times=times, dt=5e-3, **physics(th[None]))[0]
    rng = np.random.default_rng(int(T * 1000) + (0 if noise == "rounding" else 7))
    data = np.round(pos, 2) if noise == "rounding" else pos + rng.normal(0, SIGMA[noise], pos.shape)
    obs = tuple(Observation(t, p, SIGMA[noise]) for t, p in zip(times, data))
    post = sample(st, f"horizon_{noise}_{T}", observations=obs, seed=11, priors=Priors(spin_prior="kick"), **kw)
    ok = np.all(np.isfinite(post.entries), axis=1)
    e = post.entries[ok]
    s = summarise(post.entries)
    q = lambda x, a, b: float((np.percentile(x, b) - np.percentile(x, a)) / 2)
    spin = np.hypot(post.samples[:, 3], post.samples[:, 4]) / TWO_PI
    return {"noise": noise, "T": T, "n_obs": len(times),
            "y_hw68": q(e[:, 1], 16, 84), "z_hw68": q(e[:, 2], 16, 84), "y_hw95": q(e[:, 1], 2.5, 97.5), "z_hw95": q(e[:, 2], 2.5, 97.5),
            "mode_yz": s.mode.tolist(), "median_yz": np.median(e[:, 1:3], axis=0).tolist(),
            "spin_rev": [float(v) for v in np.percentile(spin, [16, 50, 84])], "max_tau": float(np.max(post.tau)),
            "acceptance": post.acceptance}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=11)
    ap.add_argument("--nsteps", type=int, default=5000)
    ap.add_argument("--burn", type=int, default=1500)
    a = ap.parse_args()
    th = truth()
    st = Settings(LIFT_MODELS[CURVE])
    t_entry = crossings(P0, *unpack(th[None]), st, **physics(th[None]))[0]
    kw = dict(nwalkers=64, nsteps=a.nsteps, burn=a.burn, thin=10)
    jobs = [(nz, T, th, kw) for T in T_LAST[::-1] for nz in ("rounding", "tracking")]   # longest first
    with Pool(a.procs) as pool:
        rows = pool.map(run, jobs, chunksize=1)
    rep = {"truth_theta": th.tolist(), "truth_entry_tyz": t_entry.tolist(),
           "truth_spin_rev": float(np.hypot(th[3], th[4]) / TWO_PI), "curve": CURVE, "chains": kw,
           "rows": sorted(rows, key=lambda r: (r["noise"], r["T"]))}
    out = ROOT / "results" / "final" / "observation_horizon.json"
    out.write_text(json.dumps(rep, indent=1))
    for r in rep["rows"]:
        print(f"{r['noise']:9s} T={r['T']:.2f}  y±{100 * r['y_hw68']:.1f} cm  z±{100 * r['z_hw68']:.1f} cm  "
              f"mode {np.round(r['mode_yz'], 3)}  spin {np.round(r['spin_rev'], 1)}  tau_max {r['max_tau']:.0f}")
    print("truth entry", np.round(t_entry, 3), "spin", rep["truth_spin_rev"])


if __name__ == "__main__":
    main()
