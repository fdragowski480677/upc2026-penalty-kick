"""Stage 2 (gravity + drag): fit the test case and predict the entry point for each C_D setting.

Usage:  PYTHONPATH=src .venv/bin/python scripts/run_stage2.py [--cd PRESET | --logistic]
Without arguments: the default (fixed C_D = 0.22) plus a comparison over all switches.
"""
import argparse

import numpy as np

from penalty.coefficients import LITERATURE_CD, ConstantCD, LogisticCD
from penalty.constants import TEST_CASE
from penalty.forces import AeroParams, drag, gravity, reynolds
from penalty.inverse import fit_launch_velocity
from penalty.predict import predict

FORCES = [gravity, drag]


def run(model):
    params = AeroParams(drag_model=model)
    fit = fit_launch_velocity(TEST_CASE, FORCES, params)
    return fit, predict(fit, FORCES, params), params


def report(model):
    fit, pred, params = run(model)
    v = fit.v0; s = np.linalg.norm(v)
    print(f"Stage 2 - gravity + drag, C_D model: {model.label} (P0 exact, sigma = 1 cm)")
    print(f"  v0          = ({v[0]:.3f}, {v[1]:.3f}, {v[2]:.3f}) m/s   |v0| = {s:.3f} m/s   Re0 = {reynolds(s, params):.3g}")
    print(f"  residuals   = {(fit.residuals * 100).round(2).tolist()} cm")
    print(f"  chi2/dof    = {fit.chi2:.2f} / {fit.dof}   p = {fit.p_value:.3f}")
    print(f"  t_goal      = {pred.t:.4f} s, speed at goal {pred.speed_at_goal:.2f} m/s (Re {reynolds(pred.speed_at_goal, params):.3g})")
    print(f"  entry (y,z) = ({pred.yz[0]:.3f}, {pred.yz[1]:.3f}) m  +- ({pred.sigma_yz[0]:.3f}, {pred.sigma_yz[1]:.3f}) m (1 sigma, noise only)")
    print(f"  outcome     = {pred.outcome}")


def comparison():
    print("\nSwitch comparison (C_D value | chi2 | entry y, z | shift vs default):")
    _, base, _ = run(ConstantCD())
    models = [ConstantCD.from_literature(n) for n in LITERATURE_CD] + [LogisticCD()]
    for m in models:
        fit, pred, _ = run(m)
        cd = m.cd(4.6e5)
        d = (pred.yz - base.yz) * 100
        print(f"  {m.label:26s} {cd:.3f} | {fit.chi2:5.2f} | {pred.yz[0]:.3f}, {pred.yz[1]:.3f} | {d[0]:+5.1f}, {d[1]:+5.1f} cm")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--cd", choices=sorted(LITERATURE_CD), help="use a literature C_D preset")
    g.add_argument("--logistic", action="store_true", help="use the speed-dependent C_D(Re) model")
    a = ap.parse_args()
    if a.cd:
        report(ConstantCD.from_literature(a.cd))
    elif a.logistic:
        report(LogisticCD())
    else:
        report(ConstantCD())
        comparison()
