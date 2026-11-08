"""Robustness to the definition of t = 0: an uncertain launch point and a delayed start of free flight.

Usage:  PYTHONPATH=src .venv/bin/python scripts/launch_point_test.py [--procs 6] [--nsteps 5000]

The problem fixes the ball centre at (0, 0, 0.11) m at t = 0, but foot contact lasts 9-12 ms and compresses the ball by several cm,
so t = 0 need not be the exact start of free flight from that point. Final model, kick prior, Kray C_L curve, main case (rounding
noise), on the given test case:
  baseline   launch point exact, free flight from t = 0;
  r0_5mm     launch point uncertain: three extra parameters dr0 ~ N(0, (5 mm)^2) per coordinate, sampled with the rest;
  r0_10mm    the same with 1 cm;
  tau_m5     free flight starts 5 ms BEFORE t = 0 at (0, 0, 0.11) (observations at 0.055 / 0.105 s of free flight);
  tau_p5     free flight starts 5 ms AFTER t = 0 at (0, 0, 0.11) (observations at 0.045 / 0.095 s);
  tau_p10    the same with 10 ms, the full foot-contact time.
Recorded: median entry point, 68 % half-widths, best and median chi^2 (sigma = 2.9 mm) and the posterior of dr0.
Also a fine profile chi^2(tau) for -6 ... +6 ms (least squares: launch velocity and spin axis refitted at 5 rev/s, Stage 3 forces,
reference integrator, sigma = 2.9 mm), which shows how tightly the data themselves fix the start of free flight.
Writes results/final/launch_point_test.json.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import json
from multiprocessing import Pool
from pathlib import Path

import emcee
import numpy as np

from penalty.bayes import TWO_PI, Priors, initial_walkers, log_prior, physics, sample, unpack
from penalty.bayes import LIKELIHOOD_DT
from penalty.coefficients import LIFT_MODELS
from penalty.constants import P0, TEST_CASE, Observation
from penalty.fastsim import Settings, crossings, positions

ROOT = Path(__file__).resolve().parents[1]
CURVE = "kray2014_re462"
SIG = 0.01 / np.sqrt(12)
OBS = tuple(Observation(o.t, o.position, SIG) for o in TEST_CASE)
DATA = np.array([o.position for o in OBS])


def sample_free_r0(st, sd, kw, seed=21, pr=Priors(spin_prior="kick")):
    """Final-model posterior with the launch point as three extra parameters, dr0 ~ N(0, sd^2) per coordinate."""
    def lp(theta):
        theta = np.atleast_2d(theta)
        base, dr = theta[:, :14], theta[:, 14:17]
        out = log_prior(base, pr) - np.sum(dr ** 2, axis=1) / (2 * sd ** 2)
        good = np.isfinite(out)
        if good.any():
            th = base[good]
            pos = positions(P0 + dr[good], *unpack(th), st, times=(0.05, 0.10), dt=LIKELIHOOD_DT, **physics(th))
            out[good] -= 0.5 * np.sum(((pos - DATA) / SIG) ** 2, axis=(1, 2))
        return out
    rng = np.random.default_rng(seed)
    p0 = np.column_stack((initial_walkers(kw["nwalkers"], rng, OBS, pr), rng.normal(0, sd / 3, (kw["nwalkers"], 3))))
    sampler = emcee.EnsembleSampler(kw["nwalkers"], 17, lp, vectorize=True,
                                    moves=[(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)])
    sampler.random_state = np.random.mtrand.RandomState(seed).get_state()
    sampler.run_mcmc(p0, kw["nsteps"], progress=False)
    ch = sampler.get_chain(discard=kw["burn"], thin=kw["thin"], flat=True)
    en = crossings(P0 + ch[:, 14:17], *unpack(ch[:, :14]), st, **physics(ch[:, :14]))
    return ch, en, sampler.get_autocorr_time(discard=kw["burn"], quiet=True)


def tau_profile():
    from dataclasses import replace
    from scipy.optimize import least_squares
    from penalty.forces import AeroParams, drag, gravity, magnus
    from penalty.integrate import positions_at
    from penalty.inverse import spin_basis
    F, W = [gravity, drag, magnus], TWO_PI * 5.0
    rows = []
    for tau in np.round(np.r_[np.arange(-0.006, -0.0019, 0.001), np.arange(-0.002, 0.00201, 0.00025), np.arange(0.003, 0.00601, 0.001)], 5):
        ts = [0.05 - tau, 0.10 - tau]

        def res(q):
            e1, e2 = spin_basis(q[:3])
            p = replace(AeroParams(), spin=W * (np.cos(q[3]) * e1 + np.sin(q[3]) * e2))
            return ((positions_at(P0, q[:3], ts, F, p) - DATA) / SIG).ravel()
        r = min((least_squares(res, [30.3, 9.2, 6.9, ph], method="lm") for ph in (-1.4, -1.7, 1.4)), key=lambda r: r.cost)
        rows.append({"tau_ms": float(1000 * tau), "chi2": float(2 * r.cost), "speed": float(np.linalg.norm(r.x[:3]))})
    c = np.array([r["chi2"] for r in rows]); t = np.array([r["tau_ms"] for r in rows])
    ok = c - c.min() <= 1.0
    return {"rows": rows, "best_tau_ms": float(t[c.argmin()]), "tau_1sigma_ms": [float(t[ok].min()), float(t[ok].max())],
            "dof": 2}


def run(args):
    case, kw = args
    st = Settings(LIFT_MODELS[CURVE])
    pr = Priors(spin_prior="kick")
    dr_stats = None
    if case.startswith("r0_"):
        sd = {"r0_5mm": 0.005, "r0_10mm": 0.010}[case]
        ch, en, tau = sample_free_r0(st, sd, kw)
        th, r0 = ch[:, :14], P0 + ch[:, 14:17]
        dr_stats = {ax: [float(v) for v in np.percentile(100 * ch[:, 14 + k], [16, 50, 84])] for k, ax in enumerate("xyz")}
        times = (0.05, 0.10)
    else:
        tau0 = {"baseline": 0.0, "tau_m5": -0.005, "tau_p5": 0.005, "tau_p10": 0.010}[case]
        times = tuple(round(o.t - tau0, 3) for o in OBS)
        obs = tuple(Observation(t, o.position, SIG) for t, o in zip(times, OBS))
        post = sample(st, case, observations=obs, seed=21, priors=pr, **kw)
        th, en, tau, r0 = post.samples, post.entries, post.tau, P0
    pos = positions(r0, *unpack(th), st, times=times, dt=LIKELIHOOD_DT, **physics(th))
    chi2 = np.sum(((pos - DATA) / SIG) ** 2, axis=(1, 2))
    ok = np.all(np.isfinite(en), axis=1)
    e = en[ok]
    q = lambda x: [float(v) for v in np.percentile(x, [16, 50, 84])]
    return {"case": case, "y": q(e[:, 1]), "z": q(e[:, 2]), "t_goal": q(e[:, 0]),
            "speed": q(np.linalg.norm(th[:, :3], axis=1)), "spin_rev": q(np.hypot(th[:, 3], th[:, 4]) / TWO_PI),
            "chi2_min": float(chi2.min()), "chi2_median": float(np.median(chi2)), "dr0_cm": dr_stats, "max_tau": float(np.max(tau))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--nsteps", type=int, default=5000)
    ap.add_argument("--burn", type=int, default=1500)
    a = ap.parse_args()
    kw = dict(nwalkers=64, nsteps=a.nsteps, burn=a.burn, thin=10)
    cases = ["r0_10mm", "r0_5mm", "tau_p10", "tau_p5", "tau_m5", "baseline"]
    with Pool(a.procs) as pool:
        rows = pool.map(run, [(c, kw) for c in cases], chunksize=1)
    prof = tau_profile()
    rep = {"curve": CURVE, "noise": "rounding", "sigma_m": SIG, "chains": kw, "rows": rows, "tau_profile": prof}
    print("tau profile: best", prof["best_tau_ms"], "ms, Delta chi2 <= 1 for", prof["tau_1sigma_ms"], "ms;",
          [(r["tau_ms"], round(r["chi2"], 1)) for r in prof["rows"]])
    (ROOT / "results" / "final" / "launch_point_test.json").write_text(json.dumps(rep, indent=1))
    b = next(r for r in rows if r["case"] == "baseline")
    for r in rows:
        print(f"{r['case']:9s} y {r['y'][1]:.3f} [{r['y'][0]:.3f},{r['y'][2]:.3f}] dy {100 * (r['y'][1] - b['y'][1]):+.1f} cm  "
              f"z {r['z'][1]:.3f} dz {100 * (r['z'][1] - b['z'][1]):+.1f} cm  chi2 {r['chi2_min']:.2f}/{r['chi2_median']:.2f}  "
              f"v {r['speed'][1]:.2f}  dr0 {r['dr0_cm']}  tau {r['max_tau']:.0f}")


if __name__ == "__main__":
    main()
