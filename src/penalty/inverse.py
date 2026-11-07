"""Inverse problem: infer the unknown initial conditions from the observed positions.

Unknowns θ:
* Stages 1–2: the launch velocity v0 (3 components).
* Stage 3 (``fit_spin=True``): v0 plus the two components of the spin perpendicular to v0, ω = a·e1 + b·e2, with
  e1 = ẑ×v̂0/|ẑ×v̂0| (horizontal; spin about it gives lift/dip) and e2 = v̂0×e1 (≈ vertical; spin about it gives sideways curl).
  The component along v0 produces no force and is unobservable, so it is set to 0.
P0 is fixed (exact, team decision). Data: 2 observations × 3 coordinates = 6 numbers; dof = 6 − dim θ.

The estimator is weighted least squares (maximum likelihood for Gaussian noise). The covariance is (JᵀWJ)⁻¹, linearised and
for measurement noise only. The χ² tests the consistency of the physical model with the data at the stated noise level.
"""
from dataclasses import dataclass, replace

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2_dist

from .constants import P0
from .integrate import positions_at


def spin_basis(v0):
    vh = v0 / np.linalg.norm(v0)
    e1 = np.cross([0.0, 0.0, 1.0], vh)
    e1 /= np.linalg.norm(e1)
    return e1, np.cross(vh, e1)


@dataclass
class Fit:
    theta: np.ndarray       # fitted parameters (v0[, a, b])
    cov: np.ndarray         # covariance of theta
    chi2: float
    dof: int
    p_value: float
    residuals: np.ndarray   # (n_obs, 3) model − data [m]
    fit_spin: bool = False

    @property
    def v0(self):
        return self.theta[:3]

    @property
    def spin(self):
        """Fitted initial spin vector [rad/s] (zero if spin is not fitted)."""
        if not self.fit_spin:
            return np.zeros(3)
        e1, e2 = spin_basis(self.v0)
        return self.theta[3] * e1 + self.theta[4] * e2


def unpack(theta, params, fit_spin):
    """Map the parameter vector to (v0, params with the spin set)."""
    v0 = np.asarray(theta[:3], dtype=float)
    if not fit_spin:
        return v0, params
    e1, e2 = spin_basis(v0)
    return v0, replace(params, spin=theta[3] * e1 + theta[4] * e2)


def fit(observations, forces, params=None, r0=P0, fit_spin=False, spin_guess=(0.0, 30.0)):
    times = [o.t for o in observations]
    data = np.array([o.position for o in observations])
    sig = np.array([o.sigma for o in observations])[:, None] * np.ones(3)

    def weighted_residuals(theta):
        v0, p = unpack(theta, params, fit_spin)
        return ((positions_at(r0, v0, times, forces, p) - data) / sig).ravel()

    o = observations[0]
    theta0 = (o.position - r0) / o.t
    if fit_spin:
        theta0 = np.concatenate((theta0, spin_guess))
    res = least_squares(weighted_residuals, theta0, method="lm", xtol=1e-14, ftol=1e-14, x_scale="jac")
    J = res.jac
    cov = np.linalg.pinv(J.T @ J)
    chi2 = float(res.fun @ res.fun)
    dof = data.size - theta0.size
    p = float(chi2_dist.sf(chi2, dof)) if dof > 0 else float("nan")
    return Fit(res.x, cov, chi2, dof, p, res.fun.reshape(data.shape) * sig, fit_spin)


def fit_launch_velocity(observations, forces, params=None, r0=P0):
    """Stages 1–2: weighted least-squares fit of v0 only."""
    return fit(observations, forces, params, r0, fit_spin=False)
