"""Stage 4 validation: are the stated credible regions calibrated? (simulation-based coverage test)

For each trial: draw a 'true' penalty (v0 near the test case; spin, C_D0, ρ, T, ball mass/size, seam from the priors), simulate the positions at
0.05 and 0.10 s, add noise, run the Bayesian pipeline, and record whether the true entry point lies inside the 68 % / 95 %
highest-density regions. With a correct and well-sampled model, the coverage fractions should be ≈ 0.68 and ≈ 0.95,
within binomial scatter.

Usage:  PYTHONPATH=src .venv/bin/python scripts/validate_stage4_coverage.py --noise tracking --trials 24 --procs 11
        [--spin-prior kick] [--start 100] [--tag primus]
--spin-prior: the spin prior used BOTH to draw the true shots and in the inference (self-consistent test of that model).
--start: first trial index (trial i uses random seed 1000 + i), so batches run on different machines never repeat a trial.
--tag: suffix of the output file, results/final/coverage_<noise>[_<spin prior>][_<tag>].json; batches are merged afterwards.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import json
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from penalty.bayes import Priors, density_prior, kick_prior, physics, sample, summarise, unpack
from penalty.coefficients import LIFT_MODELS
from penalty.constants import P0, Observation
from penalty.fastsim import Settings, crossings, positions

ROOT = Path(__file__).resolve().parents[1]
NOISE = {"tracking": 0.01, "rounding": 0.01 / np.sqrt(12)}


def draw_truth(rng, pr=Priors()):
    """v0 scattered around the test case; nuisance parameters drawn from their priors (a self-consistent test)."""
    v0 = np.array([30.2, 8.8, 6.9]) + rng.normal(0, [1.5, 1.5, 1.0])
    if pr.spin_prior == "kick":                    # spin magnitude from p(Omega | |v0|) of the kick-mechanics model
        kp = kick_prior()
        i = int(np.argmin(abs(kp.vb - np.linalg.norm(v0))))
        c = np.cumsum(np.exp(kp.logp[i])); c /= c[-1]
        W = 2 * np.pi * max(float(np.interp(rng.uniform(), c, kp.w)), 0.05)
    else:
        W = 2 * np.pi * pr.spin_median_rev * np.exp(pr.spin_sigma_ln * rng.standard_normal())
    phi = rng.uniform(0, 2 * np.pi)
    while True:
        cd0 = rng.normal(pr.cd0_mean, pr.cd0_sd)
        if pr.cd0_bounds[0] < cd0 < pr.cd0_bounds[1]:
            break
    rho = rng.choice(density_prior().samples)
    return np.array([*v0, W * np.cos(phi), W * np.sin(phi), cd0, rho, rng.uniform(*pr.t_bounds), rng.uniform(*pr.mass_bounds),
                     rng.uniform(*pr.circ_bounds), *rng.normal(0, pr.seam_sd, 2), *rng.normal(0, pr.wind_sd, 2)])


def trial(args):
    i, noise, lift, kw, spin_prior = args
    rng = np.random.default_rng(1000 + i)
    st = Settings(LIFT_MODELS[lift])
    pr = Priors(spin_prior=spin_prior)
    th = draw_truth(rng, pr)[None, :]
    true_entry = crossings(P0, *unpack(th), st, **physics(th))[0]
    if not np.all(np.isfinite(true_entry)):
        return None
    pos = positions(P0, *unpack(th), st, **physics(th))[0]
    sig = NOISE[noise]
    obs = tuple(Observation(t, p + rng.normal(0, sig, 3), sig) for t, p in zip((0.05, 0.10), pos))
    post = sample(st, f"cov{i}", observations=obs, seed=i, priors=pr, **kw)
    s = summarise(post.entries)
    d = float(s.kde(true_entry[1:3][:, None])[0])
    return {"trial": i, "true_yz": true_entry[1:3].tolist(), "mode_yz": s.mode.tolist(),
            "in68": d >= s.levels[0.68], "in95": d >= s.levels[0.95], "true_spin_rev": float(np.hypot(*th[0, 3:5]) / (2 * np.pi))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--noise", choices=sorted(NOISE), default="tracking")
    ap.add_argument("--trials", type=int, default=24)
    ap.add_argument("--procs", type=int, default=11)
    ap.add_argument("--nsteps", type=int, default=5000)
    ap.add_argument("--burn", type=int, default=1500)
    ap.add_argument("--spin-prior", choices=("lognormal", "kick"), default="lognormal")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    kw = dict(nwalkers=64, nsteps=a.nsteps, burn=a.burn, thin=10)
    jobs = [(i, a.noise, "kray2014_re462", kw, a.spin_prior) for i in range(a.start, a.start + a.trials)]
    with Pool(a.procs) as pool:
        rows = [r for r in pool.imap_unordered(trial, jobs) if r is not None]
    n = len(rows)
    c68 = sum(r["in68"] for r in rows) / n
    c95 = sum(r["in95"] for r in rows) / n
    se68, se95 = np.sqrt(0.68 * 0.32 / n), np.sqrt(0.95 * 0.05 / n)
    out = {"noise": a.noise, "spin_prior": a.spin_prior, "first_trial": a.start, "n_trials": n, "coverage68": c68, "binomial_se68": se68, "coverage95": c95,
           "binomial_se95": se95, "chains": kw, "trials": sorted(rows, key=lambda r: r["trial"])}
    # The default priors are the final unified model (with wind); Stage 4 coverage results stay in results/stage4/.
    suffix = ("" if a.spin_prior == "lognormal" else f"_{a.spin_prior}") + (f"_{a.tag}" if a.tag else "")
    path = ROOT / "results" / "final" / f"coverage_{a.noise}{suffix}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2))
    print(f"{a.noise}: n = {n}, coverage 68 % = {c68:.2f} ± {se68:.2f}, coverage 95 % = {c95:.2f} ± {se95:.2f}")


if __name__ == "__main__":
    main()
