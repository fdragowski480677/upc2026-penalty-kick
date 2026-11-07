"""Inverse problem: infer the unknown initial conditions from the observed positions.

Stage 1 unknowns: the launch velocity v0 (3 components). P0 is fixed (exact, team decision).
Data: 2 observations × 3 coordinates = 6 numbers, so there are 6 − 3 = 3 degrees of freedom.

The estimator is weighted least squares. For Gaussian measurement noise this is the maximum-likelihood
estimate. The parameter covariance is (JᵀWJ)⁻¹ (linearised, measurement noise only).
The χ² of the fit tests whether the physical model is consistent with the data at the stated noise level.
"""
from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2_dist

from .constants import P0
from .integrate import positions_at


@dataclass
class Fit:
    v0: np.ndarray          # best-fit launch velocity [m/s]
    cov: np.ndarray         # 3×3 covariance of v0 [(m/s)^2]
    chi2: float             # Σ (residual/σ)²
    dof: int                # degrees of freedom
    p_value: float          # P(χ² ≥ observed | model correct)
    residuals: np.ndarray   # (n_obs, 3) model − data [m]


def _initial_guess(observations, r0):
    """Finite-difference velocity from P0 to the first observation (good enough to start the solver)."""
    o = observations[0]
    return (o.position - r0) / o.t


def fit_launch_velocity(observations, forces, params=None, r0=P0):
    """Weighted least-squares fit of v0, with r0 fixed."""
    times = [o.t for o in observations]
    data = np.array([o.position for o in observations])
    sig = np.array([o.sigma for o in observations])[:, None] * np.ones(3)

    def weighted_residuals(v0):
        return ((positions_at(r0, v0, times, forces, params) - data) / sig).ravel()

    res = least_squares(weighted_residuals, _initial_guess(observations, r0), method="lm", xtol=1e-14, ftol=1e-14)
    J = res.jac
    cov = np.linalg.inv(J.T @ J)
    chi2 = float(res.fun @ res.fun)
    dof = data.size - 3
    return Fit(res.x, cov, chi2, dof, float(chi2_dist.sf(chi2, dof)), (res.fun.reshape(data.shape) * sig))
