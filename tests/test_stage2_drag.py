"""Stage 2 verification: the drag force, the C_D switches, and the fit with drag."""
import numpy as np
import pytest

from penalty.coefficients import LITERATURE_CD, ConstantCD, LogisticCD
from penalty.constants import G, P0, Air, Ball, Observation
from penalty.forces import AeroParams, drag, gravity, reynolds
from penalty.integrate import positions_at, simulate
from penalty.inverse import fit_launch_velocity

BALL, AIR = Ball(), Air()
K = 0.5 * AIR.density * np.pi * BALL.radius**2 / BALL.mass  # a_drag = K·C_D·v²
DEFAULT = AeroParams()


def test_default_is_fixed_022():
    assert DEFAULT.drag_model.cd(1e3) == DEFAULT.drag_model.cd(1e6) == 0.22


def test_drag_magnitude_and_direction():
    """|a| = K·C_D·v², opposite to v. At 31.5 m/s with C_D = 0.22 this is ≈ 11.6 m/s² (drag.md §10.2)."""
    v = np.array([30.0, 8.0, 6.0]) * 31.5 / np.linalg.norm([30.0, 8.0, 6.0])
    a = drag(0, P0, v, DEFAULT)
    assert np.linalg.norm(a) == pytest.approx(K * 0.22 * 31.5**2, rel=1e-12)
    assert np.linalg.norm(a) == pytest.approx(11.6, abs=0.1)
    assert np.allclose(np.cross(a, v), 0, atol=1e-12) and a @ v < 0


def test_zero_velocity_no_drag():
    assert np.all(drag(0, P0, np.zeros(3), DEFAULT) == 0)


def test_one_dimensional_drag_analytic():
    """Pure drag along x: v(t) = v0/(1 + c v0 t), x(t) = ln(1 + c v0 t)/c, with c = K·C_D."""
    v0, c = 32.0, K * 0.22
    ts = np.linspace(0.02, 0.4, 6)
    num = positions_at(np.zeros(3), np.array([v0, 0, 0]), ts, [drag], DEFAULT)
    assert np.allclose(num[:, 0], np.log1p(c * v0 * ts) / c, atol=1e-9)


def test_terminal_velocity():
    """Vertical fall with gravity + drag tends to v_t = sqrt(g / (K C_D))."""
    vt = np.sqrt(G / (K * 0.22))
    sol, _ = simulate(np.array([0, 0, 5000.0]), np.zeros(3), [gravity, drag], DEFAULT, t_max=60.0)
    assert -sol.y[5, -1] == pytest.approx(vt, rel=1e-4)


def test_drag_dissipates_energy():
    sol, _ = simulate(P0, np.array([30.0, 8.0, 6.0]), [gravity, drag], DEFAULT)
    E = 0.5 * np.sum(sol.y[3:6] ** 2, axis=0) + G * sol.y[2]
    assert np.all(np.diff(E) < 0)


def test_cd_zero_reduces_to_stage1():
    p0 = AeroParams(drag_model=ConstantCD(0.0))
    _, c1 = simulate(P0, np.array([30.0, 8.0, 6.0]), [gravity])
    _, c2 = simulate(P0, np.array([30.0, 8.0, 6.0]), [gravity, drag], p0)
    assert np.allclose(c1.position, c2.position, atol=1e-10)


def test_reynolds_number():
    assert reynolds(31.5, DEFAULT) == pytest.approx(31.5 * 0.22 / 1.5e-5)


# --- C_D switches -----------------------------------------------------------------------------------------------

def test_literature_presets_load_and_are_plausible():
    for name, (value, source) in LITERATURE_CD.items():
        m = ConstantCD.from_literature(name)
        assert m.cd(4.6e5) == value and m.label == name and source
        assert 0.12 <= value <= 0.30  # supercritical football range, drag.md §9


def test_unknown_preset_raises():
    with pytest.raises(KeyError):
        ConstantCD.from_literature("smooth_sphere")


def test_logistic_limits_and_monotonic():
    m = LogisticCD()
    assert m.cd(1e3) == pytest.approx(m.c_sub, abs=1e-6)
    assert m.cd(1e8) == pytest.approx(m.c_sup, abs=1e-6)
    assert m.cd(m.re_c) == pytest.approx(0.5 * (m.c_sub + m.c_sup))
    res = np.logspace(4, 7, 200)
    assert np.all(np.diff([m.cd(r) for r in res]) <= 0)


def test_logistic_is_supercritical_for_a_penalty():
    """Along a penalty (Re ≈ 4.0–4.8×10⁵) the logistic model is within 0.005 of C_sup (drag.md §10.1)."""
    m = LogisticCD()
    for re in (4.0e5, 4.8e5):
        assert abs(m.cd(re) - m.c_sup) < 0.005


def test_logistic_is_evaluated_along_trajectory():
    """A slow shot crosses the drag crisis: the logistic model must give more drag than constant C_sup."""
    v0 = np.array([12.0, 0.0, 6.0])  # Re ≈ 1.8e5 ≈ Re_c; lofted so it reaches the goal plane
    _, c_log = simulate(P0, v0, [gravity, drag], AeroParams(drag_model=LogisticCD()))
    _, c_sup = simulate(P0, v0, [gravity, drag], AeroParams(drag_model=ConstantCD(LogisticCD().c_sup)))
    assert c_log.t > c_sup.t


# --- inverse problem with drag -----------------------------------------------------------------------------------

@pytest.mark.parametrize("model", [ConstantCD(), ConstantCD.from_literature("asai2007_teamgeist"), LogisticCD()])
def test_fit_recovers_v0_with_drag(model):
    params = AeroParams(drag_model=model)
    v0 = np.array([30.0, 8.0, 6.5])
    pts = positions_at(P0, v0, (0.05, 0.10), [gravity, drag], params)
    obs = [Observation(t, p, 0.01) for t, p in zip((0.05, 0.10), pts)]
    fit = fit_launch_velocity(obs, [gravity, drag], params)
    assert np.allclose(fit.v0, v0, atol=1e-7) and fit.chi2 < 1e-10
