"""Stage 4: Bayesian inference of the goal-entry point.

Parameters θ (9): v0 (3), spin components (a, b) ⊥ v0 [rad/s], C_D0, ρ, seam coefficients (c1, c2).
Likelihood: independent Gaussian position errors, σ = 1 cm, at 0.05 s and 0.10 s (P0 exact).
Priors (team decisions; sources in docs/stages/stage4-uncertainty.md):

* |ω|: log-normal, median 5 rev/s, σ_ln = 0.41 (95 % ≈ 2.2–11 rev/s). The axis angle in the plane ⊥ v0 is uniform.
  In (a, b) coordinates the density is p(a, b) = LN(|ω|) / (2π|ω|) (polar Jacobian).
* C_D0 ~ N(0.22, 0.04²), truncated to [0.12, 0.35].
* ρ ~ U(1.10, 1.29) kg/m³.
* c1, c2 ~ N(0, 0.03²).
* v0: flat for 10 < |v0| < 45 m/s.

The lift-curve model is a discrete model uncertainty: one chain per curve, pooled with equal weights.
"""
from dataclasses import dataclass

import emcee
import numpy as np
from scipy.stats import gaussian_kde

from .constants import P0, TEST_CASE
from .fastsim import Settings, crossings, positions
from .outcome import classify

TWO_PI = 2 * np.pi


@dataclass(frozen=True)
class Priors:
    spin_median_rev: float = 5.0
    spin_sigma_ln: float = 0.41
    cd0_mean: float = 0.22
    cd0_sd: float = 0.04
    cd0_bounds: tuple = (0.12, 0.35)
    rho_bounds: tuple = (1.10, 1.29)
    seam_sd: float = 0.03
    speed_bounds: tuple = (10.0, 45.0)
    spin_prior: str = "lognormal"          # or "loguniform" (sensitivity): p(|ω|) ∝ 1/|ω| on spin_bounds_rev
    spin_bounds_rev: tuple = (1.0, 10.0)


def spin_basis_vec(v0):
    vh = v0 / np.linalg.norm(v0, axis=1, keepdims=True)
    e1 = np.cross(np.array([0.0, 0.0, 1.0]), vh)
    e1 /= np.linalg.norm(e1, axis=1, keepdims=True)
    return e1, np.cross(vh, e1)


def unpack(theta):
    v0 = theta[:, :3]
    e1, e2 = spin_basis_vec(v0)
    spin = theta[:, 3:4] * e1 + theta[:, 4:5] * e2
    return v0, spin, theta[:, 5], theta[:, 6], theta[:, 7:9]


def log_prior(theta, pr=Priors()):
    speed = np.linalg.norm(theta[:, :3], axis=1)
    W = np.hypot(theta[:, 3], theta[:, 4])
    cd0, rho, seam = theta[:, 5], theta[:, 6], theta[:, 7:9]
    ok = ((speed > pr.speed_bounds[0]) & (speed < pr.speed_bounds[1]) & (W > 0)
          & (cd0 > pr.cd0_bounds[0]) & (cd0 < pr.cd0_bounds[1]) & (rho > pr.rho_bounds[0]) & (rho < pr.rho_bounds[1]))
    with np.errstate(divide="ignore"):
        w_rev = W / TWO_PI
        if pr.spin_prior == "lognormal":
            lp_spin = -2 * np.log(W) - np.log(w_rev / pr.spin_median_rev) ** 2 / (2 * pr.spin_sigma_ln**2)
        else:
            lo, hi = pr.spin_bounds_rev
            ok &= (w_rev > lo) & (w_rev < hi)
            lp_spin = -2 * np.log(W)
        lp = (lp_spin - (cd0 - pr.cd0_mean) ** 2 / (2 * pr.cd0_sd**2) - np.sum(seam**2, axis=1) / (2 * pr.seam_sd**2))
    return np.where(ok, lp, -np.inf)


#: Fixed RK4 step for the likelihood: error ≈ 1e-7 m, five orders below σ = 1 cm (test_stage4_fastsim.py).
LIKELIHOOD_DT = 5e-3


def make_log_posterior(settings, observations=TEST_CASE, priors=Priors(), r0=P0):
    times = tuple(o.t for o in observations)
    data = np.array([o.position for o in observations])
    sig = np.array([o.sigma for o in observations])[:, None]

    def log_post(theta):
        theta = np.atleast_2d(theta)
        lp = log_prior(theta, priors)
        good = np.isfinite(lp)
        out = np.full(theta.shape[0], -np.inf)
        if good.any():
            pos = positions(r0, *unpack(theta[good]), settings, times=times, dt=LIKELIHOOD_DT)
            chi2 = np.sum(((pos - data) / sig) ** 2, axis=(1, 2))
            out[good] = lp[good] - 0.5 * chi2
        return out

    return log_post


def initial_walkers(n, rng, observations=TEST_CASE, priors=Priors(), r0=P0):
    """Start from the finite-difference velocity, with the spin and nuisance parameters drawn from their priors."""
    o = observations[0]
    v_fd = (o.position - r0) / o.t
    if priors.spin_prior == "lognormal":
        W = TWO_PI * priors.spin_median_rev * np.exp(priors.spin_sigma_ln * rng.standard_normal(n))
    else:
        W = TWO_PI * np.exp(rng.uniform(*np.log(priors.spin_bounds_rev), n))
    phi = rng.uniform(0, TWO_PI, n)
    cd0 = np.clip(rng.normal(priors.cd0_mean, priors.cd0_sd, n), 0.13, 0.34)
    rho = rng.uniform(*priors.rho_bounds, n)
    seam = rng.normal(0, priors.seam_sd, (n, 2))
    v0 = v_fd + rng.normal(0, 0.3, (n, 3))
    return np.column_stack((v0, W * np.cos(phi), W * np.sin(phi), cd0, rho, seam))


@dataclass
class Posterior:
    label: str
    samples: np.ndarray     # (M, 9) θ samples
    entries: np.ndarray     # (M, 3) goal crossing (t, y, z); NaN if the ball never reaches the goal
    acceptance: float
    tau: np.ndarray         # integrated autocorrelation times per parameter


def sample(settings, label, nwalkers=48, nsteps=4000, burn=1500, thin=10, seed=0, observations=TEST_CASE, priors=Priors()):
    rng = np.random.default_rng(seed)
    lp = make_log_posterior(settings, observations, priors)
    p0 = initial_walkers(nwalkers, rng, observations, priors)
    sampler = emcee.EnsembleSampler(nwalkers, p0.shape[1], lp, vectorize=True,
                                    moves=[(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)])
    sampler.random_state = np.random.mtrand.RandomState(seed).get_state()  # reproducible chains
    sampler.run_mcmc(p0, nsteps, progress=False)
    chain = sampler.get_chain(discard=burn, thin=thin, flat=True)
    tau = sampler.get_autocorr_time(discard=burn, quiet=True)
    entries = crossings(P0, *unpack(chain), settings)
    return Posterior(label, chain, entries, float(np.mean(sampler.acceptance_fraction)), tau)


# ---------------------------------------------------------------------------------------------------------------
# Posterior summaries on the goal plane
# ---------------------------------------------------------------------------------------------------------------

@dataclass
class EntrySummary:
    mode: np.ndarray            # most probable entry point (KDE maximum) (y, z)
    mean: np.ndarray
    median: np.ndarray
    sd: np.ndarray
    p_reach: float              # fraction of samples reaching the goal plane
    p_outcome: dict             # P(clean entry / frame contact / miss), among those reaching the plane
    levels: dict                # KDE density thresholds enclosing 68 % and 95 % of the probability
    kde: object


def summarise(entries, grid=200):
    ok = np.all(np.isfinite(entries), axis=1)
    yz = entries[ok, 1:3]
    kde = gaussian_kde(yz.T)
    y = np.linspace(yz[:, 0].min(), yz[:, 0].max(), grid)
    z = np.linspace(yz[:, 1].min(), yz[:, 1].max(), grid)
    Y, Z = np.meshgrid(y, z)
    dens = kde(np.vstack((Y.ravel(), Z.ravel())))
    mode = np.array([Y.ravel()[dens.argmax()], Z.ravel()[dens.argmax()]])
    at_samples = np.sort(kde(yz.T))[::-1]
    levels = {q: float(at_samples[int(q * len(at_samples)) - 1]) for q in (0.68, 0.95)}
    labels = [classify(a, b) for a, b in yz]
    p_out = {k: labels.count(k) / len(labels) for k in sorted(set(labels))}
    return EntrySummary(mode, yz.mean(0), np.median(yz, 0), yz.std(0), float(ok.mean()), p_out, levels, kde)
