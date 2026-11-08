"""Stage 6: steady uniform wind. Aerodynamic forces act on the air-relative velocity v − w."""
from dataclasses import replace

import numpy as np
import pytest

from penalty.coefficients import LIFT_MODELS, ConstantCD
from penalty.constants import P0, Air, Goal
from penalty.fastsim import Settings, crossings, positions
from penalty.forces import AeroParams, drag, gravity, magnus, seam_force
from penalty.integrate import positions_at, simulate

FORCES = [gravity, drag, magnus, seam_force]
W = np.array([-2.0, 1.5, 0.0])
BASE = replace(AeroParams(), spin=np.array([3.0, -4.0, -30.0]), seam_coeffs=(0.02, -0.01))


def test_zero_wind_is_unchanged():
    v0 = np.array([30.0, 9.0, 7.0])
    a = positions_at(P0, v0, (0.05, 0.1, 0.3), FORCES, BASE)
    b = positions_at(P0, v0, (0.05, 0.1, 0.3), FORCES, replace(BASE, wind=np.zeros(3)))
    assert np.array_equal(a, b)


def test_galilean_invariance():
    """Uniform wind w: r(t) = r_still(t; v0 − w) + w t, exactly, because gravity is frame-independent and the air moves uniformly.
    (Spin decay uses the ground path length, so it is switched off here; see forces.py.)"""
    v0 = np.array([30.0, 9.0, 7.0])
    ts = (0.05, 0.10, 0.25, 0.4)
    windy = positions_at(P0, v0, ts, FORCES, replace(BASE, wind=W))
    still = positions_at(P0, v0 - W, ts, FORCES, BASE)
    assert np.allclose(windy, still + np.outer(ts, W), atol=1e-9)


def test_headwind_shortens_tailwind_lengthens_flight_time():
    v0 = np.array([30.0, 0.0, 6.0])
    _, head = simulate(P0, v0, FORCES, replace(BASE, wind=np.array([-5.0, 0, 0])))
    _, tail = simulate(P0, v0, FORCES, replace(BASE, wind=np.array([5.0, 0, 0])))
    _, calm = simulate(P0, v0, FORCES, BASE)
    assert head.t > calm.t > tail.t


def test_crosswind_drifts_downwind():
    v0 = np.array([30.0, 0.0, 6.0])
    p = replace(AeroParams(), wind=np.array([0.0, 4.0, 0.0]))
    _, c = simulate(P0, v0, [gravity, drag], p)
    assert c.position[1] > 0.01


def test_fastsim_matches_reference_with_wind():
    rng = np.random.default_rng(4)
    n = 5
    v0 = np.column_stack((rng.uniform(27, 33, n), rng.uniform(5, 11, n), rng.uniform(5, 8, n)))
    spin, cd0 = rng.normal(0, 30, (n, 3)), rng.uniform(0.15, 0.3, n)
    rho, seam = rng.uniform(0.9, 1.25, n), rng.normal(0, 0.03, (n, 2))
    wind = np.column_stack((rng.normal(0, 2, n), rng.normal(0, 2, n), np.zeros(n)))
    st = Settings(LIFT_MODELS["kray2014_re462"], 0.47, 0.0)
    fast = positions(P0, v0, spin, cd0, rho, seam, st, wind=wind)
    cr = crossings(P0, v0, spin, cd0, rho, seam, st, wind=wind)
    for i in range(n):
        p = replace(AeroParams(), spin=spin[i], drag_model=ConstantCD(cd0[i]), air=Air(density=rho[i]),
                    lift_model=LIFT_MODELS["kray2014_re462"], seam_coeffs=tuple(seam[i]), wind=wind[i])
        assert np.max(np.abs(fast[i] - positions_at(P0, v0[i], (0.05, 0.10), FORCES, p))) < 1e-6
        _, c = simulate(P0, v0[i], FORCES, p)
        assert np.max(np.abs(cr[i, 1:] - c.position[1:])) < 1e-6
