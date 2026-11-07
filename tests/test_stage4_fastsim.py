"""Stage 4: the vectorised integrator must reproduce the reference physics and integrator."""
from dataclasses import replace

import numpy as np
import pytest

from penalty.coefficients import LIFT_MODELS
from penalty.constants import P0
from penalty.fastsim import Settings, crossings, positions
from penalty.forces import AeroParams, drag, gravity, magnus, seam_force
from penalty.coefficients import ConstantCD
from penalty.integrate import positions_at, simulate
from penalty.constants import Air

FORCES = [gravity, drag, magnus, seam_force]
RNG = np.random.default_rng(7)


def cases(n=6):
    v0 = np.column_stack((RNG.uniform(27, 33, n), RNG.uniform(5, 11, n), RNG.uniform(5, 8, n)))
    spin = RNG.normal(0, 30, (n, 3))
    cd0 = RNG.uniform(0.15, 0.30, n)
    rho = RNG.uniform(1.10, 1.29, n)
    seam = RNG.normal(0, 0.03, (n, 2))
    return v0, spin, cd0, rho, seam


def reference_params(i, v0, spin, cd0, rho, seam, lift, ks, k):
    return replace(AeroParams(), spin=spin[i], drag_model=ConstantCD(cd0[i]), air=Air(density=rho[i]),
                   lift_model=lift, spin_drag_slope=ks, spin_decay_k=k, seam_coeffs=tuple(seam[i]))


@pytest.mark.parametrize("lift", list(LIFT_MODELS))
@pytest.mark.parametrize("ks,k", [(0.47, 0.0), (0.74, 2e-3)])
def test_positions_match_reference(lift, ks, k):
    v0, spin, cd0, rho, seam = cases()
    st = Settings(LIFT_MODELS[lift], ks, k)
    fast = positions(P0, v0, spin, cd0, rho, seam, st)
    for i in range(len(cd0)):
        ref = positions_at(P0, v0[i], (0.05, 0.10), FORCES, reference_params(i, v0, spin, cd0, rho, seam, LIFT_MODELS[lift], ks, k))
        assert np.max(np.abs(fast[i] - ref)) < 1e-6


@pytest.mark.parametrize("lift", ["kray2014_re462", "asai2007_re_interp"])
def test_crossings_match_reference(lift):
    v0, spin, cd0, rho, seam = cases()
    st = Settings(LIFT_MODELS[lift], 0.47, 1.4e-4)
    fast = crossings(P0, v0, spin, cd0, rho, seam, st)
    for i in range(len(cd0)):
        _, c = simulate(P0, v0[i], FORCES, reference_params(i, v0, spin, cd0, rho, seam, LIFT_MODELS[lift], 0.47, 1.4e-4))
        assert c is not None
        assert fast[i, 0] == pytest.approx(c.t, abs=1e-7)
        assert np.max(np.abs(fast[i, 1:] - c.position[1:])) < 1e-6


def test_landing_gives_nan():
    v0 = np.array([[10.0, 0.0, 1.0]])
    out = crossings(P0, v0, np.zeros((1, 3)), np.array([0.22]), np.array([1.2]), np.zeros((1, 2)),
                    Settings(LIFT_MODELS["kray2014_re462"]))
    assert np.all(np.isnan(out))


def test_likelihood_step_is_accurate():
    """The coarse step used in the likelihood (bayes.LIKELIHOOD_DT) stays within 1e-6 m of the reference integrator."""
    from penalty.bayes import LIKELIHOOD_DT
    v0, spin, cd0, rho, seam = cases()
    st = Settings(LIFT_MODELS["kray2014_re462"], 0.47, 0.0)
    fast = positions(P0, v0, spin, cd0, rho, seam, st, dt=LIKELIHOOD_DT)
    for i in range(len(cd0)):
        ref = positions_at(P0, v0[i], (0.05, 0.10), FORCES,
                           reference_params(i, v0, spin, cd0, rho, seam, LIFT_MODELS["kray2014_re462"], 0.47, 0.0))
        assert np.max(np.abs(fast[i] - ref)) < 1e-6


def test_spin_prior_is_normalised_lognormal():
    """Sampling the prior alone (no data) must reproduce the stated log-normal: median 5 rev/s, 95 % ≈ 2.2–11 rev/s."""
    import emcee
    from penalty.bayes import Priors, initial_walkers, log_prior
    rng = np.random.default_rng(3)
    p0 = initial_walkers(32, rng)
    sampler = emcee.EnsembleSampler(32, 9, lambda th: log_prior(th), vectorize=True)
    sampler.run_mcmc(p0, 3000, progress=False)
    ch = sampler.get_chain(discard=1000, flat=True)
    w = np.hypot(ch[:, 3], ch[:, 4]) / (2 * np.pi)
    assert np.median(w) == pytest.approx(5.0, rel=0.08)
    assert np.percentile(w, 2.5) == pytest.approx(5 * np.exp(-1.96 * 0.41), rel=0.15)
    assert np.percentile(w, 97.5) == pytest.approx(5 * np.exp(1.96 * 0.41), rel=0.15)
