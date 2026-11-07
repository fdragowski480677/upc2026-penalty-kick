"""Stage 3 (gravity + drag + Magnus, spin-dependent drag): fit v0 and spin to the test case and predict the entry point.

Usage:  PYTHONPATH=src .venv/bin/python scripts/run_stage3.py
Prints the default result, the sensitivity to every Stage 3 switch, and a plausibility check of the inferred values.
"""
from dataclasses import replace

import numpy as np
from scipy.optimize import least_squares

from penalty.coefficients import LIFT_MODELS, SPIN_DECAY_K, SPIN_DRAG_SLOPES, ConstantCD
from penalty.constants import P0, TEST_CASE
from penalty.forces import AeroParams, drag, gravity, magnus, reynolds, spin_parameter
from penalty.integrate import positions_at, simulate
from penalty.inverse import fit, spin_basis
from penalty.predict import predict

FORCES = [gravity, drag, magnus]
DEFAULT = AeroParams()  # C_D0 = 0.22, k_s = 0.47 (Asai), C_L = Kray Re 4.62e5, no spin decay


def run(params):
    f = fit(TEST_CASE, FORCES, params, fit_spin=True, spin_guess=(0.0, -30.0))
    p = replace(params, spin=f.spin)
    return f, predict(f, FORCES, params), p


def describe(f, pred, p):
    v = f.v0; speed = np.linalg.norm(v)
    s0, _ = spin_parameter(v, p)
    w = np.linalg.norm(f.spin)
    cl0 = p.lift_model.cl(s0, reynolds(speed, p), speed)
    cd0 = p.drag_model.cd(reynolds(speed, p)) + p.spin_drag_slope * s0
    return dict(speed=speed, w=w, rev=w / (2 * np.pi), S0=s0, CL0=cl0, CD0=cd0, chi2=f.chi2, y=pred.yz[0], z=pred.yz[1],
                sy=pred.sigma_yz[0], sz=pred.sigma_yz[1], t=pred.t, vgoal=pred.speed_at_goal, out=pred.outcome,
                axis=f.spin / w if w else np.zeros(3))


def profile_spin(params, revs=(0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15)):
    """Profile likelihood: fix |ω| and fit v0 plus the spin-axis angle in the plane ⊥ v0. Returns rows (rev/s, chi2, y, z, v_goal/v0)."""
    data = np.array([o.position for o in TEST_CASE]); ts = [o.t for o in TEST_CASE]
    rows = []
    for rev in revs:
        W = 2 * np.pi * rev
        def spin_of(q):
            e1, e2 = spin_basis(q[:3]); return W * (np.cos(q[3]) * e1 + np.sin(q[3]) * e2)
        def res(q):
            return ((positions_at(P0, q[:3], ts, FORCES,
                                  replace(params, spin=spin_of(q))) - data) / 0.01).ravel()
        best = min((least_squares(res, [30.3, 9.2, 6.9, ph], method="lm") for ph in (-1.4, -1.7)), key=lambda r: r.cost)
        _, c = simulate(P0, best.x[:3], FORCES, replace(params, spin=spin_of(best.x)))
        rows.append((rev, 2 * best.cost, c.position[1], c.position[2], np.linalg.norm(c.velocity) / np.linalg.norm(best.x[:3])))
    return rows


def main():
    f, pred, p = run(DEFAULT)
    d = describe(f, pred, p)
    print("Stage 3 - gravity + drag (C_D0 0.22 + 0.47 S) + Magnus (Kray Re 4.62e5), constant spin; P0 exact, sigma = 1 cm")
    print(f"  v0          = {np.round(f.v0, 3).tolist()} m/s  |v0| = {d['speed']:.3f} m/s")
    print(f"  spin        = {np.round(f.spin, 2).tolist()} rad/s  |w| = {d['w']:.1f} rad/s = {d['rev']:.2f} rev/s, axis {np.round(d['axis'], 3).tolist()}")
    print(f"  at launch   : S = {d['S0']:.3f}, C_L = {d['CL0']:.3f}, C_D = {d['CD0']:.3f}")
    print(f"  sigma(theta)= {np.round(np.sqrt(np.diag(f.cov)), 3).tolist()}")
    print(f"  residuals   = {(f.residuals * 100).round(2).tolist()} cm")
    print(f"  chi2/dof    = {f.chi2:.2f} / {f.dof}   p = {f.p_value:.3f}")
    print(f"  t_goal      = {d['t']:.4f} s, speed at goal {d['vgoal']:.2f} m/s")
    print(f"  entry (y,z) = ({d['y']:.3f}, {d['z']:.3f}) m  +- ({d['sy']:.3f}, {d['sz']:.3f}) m (1 sigma, noise only)")
    print(f"  outcome     = {d['out']}")

    print("\nSensitivity (one switch at a time from the default):")
    print(f"  {'switch':34s} {'rev/s':>6s} {'S0':>6s} {'C_L':>6s} {'C_D':>6s} {'chi2':>6s} {'y':>7s} {'z':>7s} {'dy cm':>7s} {'dz cm':>7s}")
    cases = [(f"lift={n}", replace(DEFAULT, lift_model=m)) for n, m in LIFT_MODELS.items()]
    cases += [(f"spin_drag={n} ({k})", replace(DEFAULT, spin_drag_slope=k)) for n, k in SPIN_DRAG_SLOPES.items()]
    cases += [(f"decay={n}", replace(DEFAULT, spin_decay_k=k)) for n, k in SPIN_DECAY_K.items() if k]
    cases += [("C_D0=0.15 (Teamgeist)", replace(DEFAULT, drag_model=ConstantCD(0.15))),
              ("C_D0=0.255 (Kray S=0)", replace(DEFAULT, drag_model=ConstantCD(0.255)))]
    for name, params in cases:
        e = describe(*run(params))
        print(f"  {name:34s} {e['rev']:6.2f} {e['S0']:6.3f} {e['CL0']:6.3f} {e['CD0']:6.3f} {e['chi2']:6.2f} "
              f"{e['y']:7.3f} {e['z']:7.3f} {100 * (e['y'] - d['y']):+7.1f} {100 * (e['z'] - d['z']):+7.1f}")

    print("\nPlausibility check of inferred values against independent measurements:")
    checks = [
        ("launch speed [m/s]", d["speed"], 25, 36, "elite penalties: mean ~31, max ~36 (Wesson 2002); university 23.9 (R&L 2015)"),
        ("spin [rev/s]", d["rev"], 2, 8, "typical penalty/curve 2-8 (Wesson; Asai 2020 5.8; Hoerzer 8.5)"),
        ("C_L at launch", d["CL0"], 0.15, 0.30, "free flight 0.21-0.29 (Asai 2020); 0.23-0.29 (Bray & Kerwin 2003)"),
        ("C_D at launch", d["CD0"], 0.20, 0.32, "spinning kicks 0.25-0.30 (Bray & Kerwin); 0.15+0.47S (Asai 2007)"),
        ("speed loss to goal [%]", 100 * (1 - d["vgoal"] / d["speed"]), 7, 16, "~10 % for a penalty (Wesson 2002)"),
        ("flight time [s]", d["t"], 0.33, 0.45, "~1/3 s (Wesson 2002); keeper dives 0.22 s before contact (Hunter 2018)"),
    ]
    for name, val, lo, hi, src in checks:
        flag = "OK " if lo <= val <= hi else "OUT"
        print(f"  [{flag}] {name:24s} {val:7.3f}   expected {lo}-{hi}   ({src})")
    print(f"  [{'OK ' if d['S0'] <= 0.23 else 'OUT'}] S at launch within Kray Re 4.62e5 data (<= 0.23): {d['S0']:.3f}")
    print("  note: sigma from linearisation is unreliable here (see the profile below).")

    print("\nProfile likelihood in spin rate (default model; v0 and spin-axis angle refitted at each fixed |w|):")
    print(f"  {'rev/s':>6s} {'chi2':>6s} {'y':>7s} {'z':>7s} {'v_goal/v0':>9s}")
    for rev, c2, y, z, ratio in profile_spin(DEFAULT):
        print(f"  {rev:6.1f} {c2:6.2f} {y:7.3f} {z:7.3f} {ratio:9.3f}")
    print(f"  note: spin axis vertical component {d['axis'][2]:+.3f} (sidespin-dominated; tilt "
          f"{np.degrees(np.arccos(min(1, abs(d['axis'][2])))):.0f} deg from vertical; Hoerzer/Bray-Kerwin use 5-10 deg)")


if __name__ == "__main__":
    main()
