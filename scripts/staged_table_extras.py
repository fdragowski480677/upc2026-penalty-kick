"""Extra columns of the staged-results table (Table 5) that are not part of the run summaries.

Usage:  PYTHONPATH=src .venv/bin/python scripts/staged_table_extras.py [--noise rounding]

For the Bayesian stages (4: Stage 4 chains; 5: kick prior without wind, Kray C_L; 6: final model, kick prior, four C_L pooled):
* launch speed |v0| and flight time to the goal plane t_goal: posterior median and 16-84 % interval;
* chi^2 of the given positions for the best posterior sample (maximum likelihood) and the posterior median chi^2, both with
  sigma = 1 cm so that they compare directly with the least-squares chi^2 of Stages 1-3.
For Stage 3 (spin fixed at 2 / 5 / 10 rev/s): the refitted |v0| and t_goal.
Writes results/final/staged_extras_<noise>.json.
"""
import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from penalty.bayes import physics, unpack
from penalty.coefficients import LIFT_MODELS
from penalty.constants import P0, TEST_CASE
from penalty.fastsim import Settings, positions
from penalty.forces import AeroParams, drag, gravity, magnus
from penalty.integrate import positions_at, simulate
from penalty.inverse import spin_basis

ROOT = Path(__file__).resolve().parents[1]
CURVES = ["kray2014_re462", "kray2014_re_interp", "asai2007_re455", "asai2007_re_interp"]
DATA = np.array([o.position for o in TEST_CASE])
SIGMA = 0.01


def chi2_of(path, curve):
    th = np.load(path)["samples"]
    pos = positions(P0, *unpack(th), Settings(LIFT_MODELS[curve]), times=(0.05, 0.10), dt=5e-3, **physics(th))
    return np.sum(((pos - DATA) / SIGMA) ** 2, axis=(1, 2))


def stage(files):
    th = np.concatenate([np.load(f)["samples"] for f, _ in files])
    en = np.concatenate([np.load(f)["entries"] for f, _ in files])
    chi = np.concatenate([chi2_of(f, c) for f, c in files])
    ok = np.all(np.isfinite(en), axis=1)
    q = lambda x: [float(v) for v in np.percentile(x, [16, 50, 84])]
    return {"speed": q(np.linalg.norm(th[:, :3], axis=1)), "t_goal": q(en[ok, 0]), "chi2_min": float(chi.min()),
            "chi2_median": float(np.median(chi)), "n": int(len(th))}


def stage3():
    F = [gravity, drag, magnus]
    ts = [o.t for o in TEST_CASE]
    out = {}
    for rev in (2.0, 5.0, 10.0):
        W = 2 * np.pi * rev

        def spin_of(q):
            e1, e2 = spin_basis(q[:3]); return W * (np.cos(q[3]) * e1 + np.sin(q[3]) * e2)

        def res(q):
            return ((positions_at(P0, q[:3], ts, F, replace(AeroParams(), spin=spin_of(q))) - DATA) / SIGMA).ravel()
        r = min((least_squares(res, [30.3, 9.2, 6.9, ph], method="lm") for ph in (-1.4, -1.7, 1.4)), key=lambda r: r.cost)
        _, c = simulate(P0, r.x[:3], F, replace(AeroParams(), spin=spin_of(r.x)))
        out[f"{rev:g}"] = {"speed": float(np.linalg.norm(r.x[:3])), "t_goal": float(c.t), "chi2": float(2 * r.cost),
                           "y": float(c.position[1]), "z": float(c.position[2])}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--noise", default="rounding")
    a = ap.parse_args()
    raw = ROOT / "results" / "raw"
    rep = {"noise": a.noise, "chi2_sigma_m": SIGMA,
           "stage3": stage3(),
           "stage4": stage([(raw / f"stage4_{a.noise}_{c}.npz", c) for c in CURVES]),
           "stage5": stage([(raw / f"stage4_{a.noise}_final_kick_no_wind.npz", "kray2014_re462")]),
           "stage6": stage([(raw / f"stage4_{a.noise}_final_kick_{c}.npz", c) for c in CURVES])}
    out = ROOT / "results" / "final" / f"staged_extras_{a.noise}.json"
    out.write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
