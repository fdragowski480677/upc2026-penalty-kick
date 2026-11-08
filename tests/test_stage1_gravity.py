"""Stage 1 verification: analytic limits of the gravity-only model, the inverse fit and outcome classification."""
import numpy as np
import pytest

from penalty.constants import G, P0, Ball, Goal, Observation
from penalty.forces import gravity
from penalty.integrate import positions_at, simulate
from penalty.inverse import fit_launch_velocity
from penalty.outcome import CLEAN, FRAME, MISS, classify, distance_to_frame
from penalty.predict import predict

V0 = np.array([30.0, 8.0, 6.0])
GVEC = np.array([0.0, 0.0, -G])


def parabola(t, r0=P0, v0=V0):
    return r0 + v0 * t + 0.5 * GVEC * t**2


def test_gravity_points_down():
    """Sign check; the B-358 class of bug."""
    a = gravity(0.0, P0, V0, None)
    assert a[2] == pytest.approx(-G) and a[0] == 0 and a[1] == 0


def test_vacuum_parabola_exact():
    ts = np.linspace(0.01, 0.3, 7)
    num = positions_at(P0, V0, ts, [gravity])
    assert np.max(np.abs(num - np.array([parabola(t) for t in ts]))) < 1e-9


def test_goal_crossing_time_and_point():
    _, c = simulate(P0, V0, [gravity])
    t_exact = (Goal().x - P0[0]) / V0[0]
    assert c.t == pytest.approx(t_exact, abs=1e-10)
    assert np.allclose(c.position, parabola(t_exact), atol=1e-9)


def test_energy_conserved():
    sol, _ = simulate(P0, V0, [gravity])
    E = 0.5 * np.sum(sol.y[3:6] ** 2, axis=0) + G * sol.y[2]
    assert np.ptp(E) < 1e-8 * E[0]


def test_ground_event_stops_low_shot():
    _, c = simulate(P0, np.array([10.0, 0.0, 1.0]), [gravity])
    assert c is None  # lands before reaching x = 11 m


def test_fit_recovers_v0_noise_free():
    obs = [Observation(t, parabola(t), 0.01) for t in (0.05, 0.10)]
    fit = fit_launch_velocity(obs, [gravity])
    assert np.allclose(fit.v0, V0, atol=1e-8)
    assert fit.chi2 < 1e-12 and fit.dof == 3


def test_fit_matches_closed_form_linear_least_squares():
    """The gravity-only model is linear in v0: v0 = Σ t_i (P_i − r0 − g t_i²/2) / Σ t_i² (per component)."""
    rng = np.random.default_rng(1)
    ts = (0.05, 0.10)
    obs = [Observation(t, parabola(t) + rng.normal(0, 0.01, 3), 0.01) for t in ts]
    fit = fit_launch_velocity(obs, [gravity])
    num = sum(t * (o.position - P0 - 0.5 * GVEC * t**2) for t, o in zip(ts, obs))
    closed = num / sum(t**2 for t in ts)
    assert np.allclose(fit.v0, closed, atol=1e-9)
    # covariance: σ² / Σ t² on the diagonal
    assert np.allclose(np.diag(fit.cov), 0.01**2 / sum(t**2 for t in ts), rtol=1e-6)


def test_chi2_calibration_monte_carlo():
    """With the correct model, χ²/dof ≈ 1 on average (checks the noise weighting)."""
    rng = np.random.default_rng(2)
    chis = []
    for _ in range(200):
        obs = [Observation(t, parabola(t) + rng.normal(0, 0.01, 3), 0.01) for t in (0.05, 0.10)]
        chis.append(fit_launch_velocity(obs, [gravity]).chi2)
    assert np.mean(chis) == pytest.approx(3.0, rel=0.2)


def test_prediction_uncertainty_against_monte_carlo():
    """Linearised entry-point σ agrees with brute-force Monte Carlo (the model is linear in v0 under gravity)."""
    rng = np.random.default_rng(3)
    clean = [Observation(t, parabola(t), 0.01) for t in (0.05, 0.10)]
    pred = predict(fit_launch_velocity(clean, [gravity]), [gravity])
    samples = []
    for _ in range(300):
        obs = [Observation(o.t, o.position + rng.normal(0, 0.01, 3), 0.01) for o in clean]
        _, c = simulate(P0, fit_launch_velocity(obs, [gravity]).v0, [gravity], dense=False)
        samples.append(c.position[1:])
    assert np.allclose(np.std(samples, axis=0), pred.sigma_yz, rtol=0.15)


@pytest.mark.parametrize("y,z,expected", [
    (0.0, 1.0, CLEAN),
    (3.66 - 0.11 - 0.01, 1.0, CLEAN),   # just clears the post
    (3.66 - 0.05, 1.0, FRAME),          # clips the inside of the post
    (3.66 + 0.06, 1.0, FRAME),          # hits the face of the post (frame width 0.12 m)
    (3.66 + 0.12 + 0.12, 1.0, MISS),    # wide, clears the outer edge of the post
    (0.0, 2.44 - 0.05, FRAME),          # hits the crossbar
    (0.0, 2.44 + 0.12 + 0.2, MISS),     # over the bar
    (3.70, 2.50, FRAME),                # corner
])
def test_classify(y, z, expected):
    assert classify(y, z) == expected


def test_distance_to_frame_inside_goal():
    assert distance_to_frame(0.0, 1.0) == pytest.approx(min(3.66, 2.44 - 1.0))
