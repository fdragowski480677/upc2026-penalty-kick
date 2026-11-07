"""Stage 3 verification: Magnus force, lift-curve models, spin-dependent drag, spin decay, and the spin fit."""
from dataclasses import replace

import numpy as np
import pytest

from penalty.coefficients import (CL_CURVES, LIFT_MODELS, SPIN_DECAY_K, ConstantCD, LinearCL, ReInterpCL,
                                  SaturatedCL, TabulatedCL)
from penalty.constants import G, P0, Air, Ball, Goal, Observation
from penalty.forces import AeroParams, drag, gravity, magnus, spin_parameter, spin_vector
from penalty.integrate import positions_at, simulate
from penalty.inverse import fit

BALL, AIR = Ball(), Air()
K = 0.5 * AIR.density * np.pi * BALL.radius**2 / BALL.mass
X = np.array([1.0, 0.0, 0.0])


def P(**kw):
    return replace(AeroParams(), **kw)


# --- force direction and magnitude ---------------------------------------------------------------------------------

def test_no_spin_no_magnus_and_stage2_unchanged():
    v = np.array([30.0, 8.0, 6.0])
    assert np.all(magnus(0, P0, v, AeroParams()) == 0)
    _, c2 = simulate(P0, v, [gravity, drag], AeroParams())
    _, c3 = simulate(P0, v, [gravity, drag, magnus], AeroParams())
    assert np.allclose(c2.position, c3.position, atol=1e-12)


def test_backspin_lifts_and_topspin_dips():
    v = 30 * X
    up = magnus(0, P0, v, P(spin=np.array([0, -40.0, 0])))   # ω = −ŷ for a ball moving +x: top surface moves backward
    down = magnus(0, P0, v, P(spin=np.array([0, 40.0, 0])))
    assert up[2] > 0 and down[2] < 0 and abs(up[0]) < 1e-12


def test_sidespin_curls_sideways():
    a = magnus(0, P0, 30 * X, P(spin=np.array([0, 0, 40.0])))  # counter-clockwise from above → curls to +y
    assert a[1] > 0 and abs(a[2]) < 1e-12


def test_magnus_perpendicular_to_v_and_spin():
    v, w = np.array([30.0, 8.0, 6.0]), np.array([3.0, -5.0, -35.0])
    a = magnus(0, P0, v, P(spin=w))
    _, w_perp = spin_parameter(v, P(spin=w))
    assert abs(a @ v) < 1e-10 and abs(a @ w_perp) < 1e-10


def test_spin_along_velocity_gives_no_force():
    v = np.array([30.0, 8.0, 6.0])
    assert np.allclose(magnus(0, P0, v, P(spin=2 * v)), 0)


def test_magnus_magnitude_uses_measured_cl():
    v, w = 31.0 * X, np.array([0, 0, 28.0])
    s = BALL.radius * 28.0 / 31.0
    expected = K * TabulatedCL().cl(s) * 31.0**2
    assert np.linalg.norm(magnus(0, P0, v, P(spin=w))) == pytest.approx(expected, rel=1e-12)
    assert TabulatedCL().cl(s) < 16 / 3 * s / 2  # far below the inviscid value used in the 2022 reports


def test_magnus_does_no_work():
    sol, _ = simulate(P0, np.array([30.0, 8.0, 6.0]), [gravity, magnus], P(spin=np.array([0, -10.0, -30.0])))
    E = 0.5 * np.sum(sol.y[3:6] ** 2, axis=0) + G * sol.y[2]
    assert np.ptp(E) < 1e-8 * E[0]


def test_pure_magnus_circular_orbit():
    """No gravity or drag, constant spin about z: the speed is constant, and the path is a circle of radius 1/(K C_L)."""
    v0, w = 30.0, 30.0
    p = P(spin=np.array([0, 0, w]))
    cl = TabulatedCL().cl(BALL.radius * w / v0)
    radius = 1.0 / (K * cl)
    sol, _ = simulate(np.zeros(3), np.array([v0, 0, 0]), [magnus], p, t_max=0.5, goal=Goal(x=1e9))
    r, v = sol.y[:3], sol.y[3:6]
    centre = np.array([0.0, radius, 0.0])
    assert np.allclose(np.linalg.norm(v, axis=0), v0, rtol=1e-9)
    assert np.allclose(np.linalg.norm(r.T - centre, axis=1), radius, rtol=1e-8)


# --- lift-curve models --------------------------------------------------------------------------------------------

def test_tabulated_curves_hit_nodes_and_are_zero_without_spin():
    for name, (_, pts, src) in CL_CURVES.items():
        m = TabulatedCL(name)
        assert m.cl(0.0) == 0.0 and src
        assert all(m.cl(s) == pytest.approx(c) for s, c in pts)
        assert m.cl(1.0) == pts[-1, 1] <= 0.35  # plateau, Kray p. 52


def test_re_interpolation_bounds():
    m = ReInterpCL()
    lo, hi = TabulatedCL("kray2014_re342"), TabulatedCL("kray2014_re462")
    assert m.cl(0.1, 3.0e5) == pytest.approx(lo.cl(0.1))
    assert m.cl(0.1, 5.0e5) == pytest.approx(hi.cl(0.1))
    assert m.cl(0.1, 4.02e5) == pytest.approx(0.5 * (lo.cl(0.1) + hi.cl(0.1)))


@pytest.mark.parametrize("model,n", [(LinearCL(), 1.0), (SaturatedCL(), 2.0)])
def test_limit_models_give_force_power_law(model, n):
    """At constant ω, F_L ∝ v^n: n = 1 for C_L ∝ S, and n = 2 for a saturated C_L."""
    p = P(spin=np.array([0, 0, 30.0]), lift_model=model)
    f1, f2 = (np.linalg.norm(magnus(0, P0, u * X, p)) for u in (30.0, 24.0))
    assert np.log(f1 / f2) / np.log(30 / 24) == pytest.approx(n, rel=1e-9)


def test_all_lift_models_registered():
    for m in LIFT_MODELS.values():
        assert 0.0 <= m.cl(0.1, 4.5e5, 30.0) <= 0.35


# --- spin-dependent drag and spin decay -----------------------------------------------------------------------------

def test_spin_raises_drag_linearly():
    v, w = 31.0 * X, np.array([0, 0, 28.0])
    s = BALL.radius * 28 / 31
    for ks in (0.0, 0.47, 0.74):
        a = drag(0, P0, v, P(spin=w, spin_drag_slope=ks))
        assert np.linalg.norm(a) == pytest.approx(K * (0.22 + ks * s) * 31.0**2, rel=1e-12)


def test_default_spin_drag_is_asai():
    assert AeroParams().spin_drag_slope == 0.47


def test_spin_decay_exponential_in_path_length():
    k = SPIN_DECAY_K["james_subcritical"]
    p = P(spin=np.array([0, 0, 40.0]), spin_decay_k=k)
    _, c = simulate(P0, np.array([30.0, 8.0, 6.0]), [gravity, drag, magnus], p)
    assert np.linalg.norm(spin_vector(p, c.path)) == pytest.approx(40.0 * np.exp(-k * c.path / BALL.radius))
    assert c.path > 11.0  # arc length exceeds the straight-line distance in x


def test_spin_decay_matches_ode_form():
    """dω/dt = −k ω |v| / R: at constant speed, ω(t) = ω₀ exp(−k v t / R)."""
    k, v0, t = 2e-3, 30.0, 0.4
    p = P(spin=np.array([0, 0, 40.0]), spin_decay_k=k)
    assert np.linalg.norm(spin_vector(p, v0 * t)) == pytest.approx(40.0 * np.exp(-k * v0 * t / BALL.radius))


def test_asai2020_decay_is_small_over_a_penalty():
    """The free-flight-derived k gives ≈ 1.5 % spin loss over ≈ 11.3 m (spin-decay-and-free-flight.md)."""
    loss = 1 - np.exp(-SPIN_DECAY_K["asai2020"] * 11.3 / BALL.radius)
    assert 0.01 < loss < 0.02


# --- inverse problem with spin -----------------------------------------------------------------------------------

@pytest.mark.parametrize("lift", ["kray2014_re462", "asai2007_re455", "limit_linear"])
def test_fit_recovers_v0_and_spin(lift):
    forces = [gravity, drag, magnus]
    e_true = np.array([30.0, 8.5, 6.8])
    base = P(lift_model=LIFT_MODELS[lift])
    from penalty.inverse import spin_basis
    e1, e2 = spin_basis(e_true)
    w_true = -3.0 * e1 - 30.0 * e2
    pts = positions_at(P0, e_true, (0.05, 0.10), forces, replace(base, spin=w_true))
    obs = [Observation(t, q, 0.01) for t, q in zip((0.05, 0.10), pts)]
    f = fit(obs, forces, base, fit_spin=True, spin_guess=(0.0, -20.0))
    assert np.allclose(f.v0, e_true, atol=1e-6)
    assert np.allclose(f.spin, w_true, atol=1e-3)
    assert f.dof == 1 and f.chi2 < 1e-10
