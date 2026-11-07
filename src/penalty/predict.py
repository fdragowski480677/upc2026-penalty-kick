"""Forward prediction of the goal-plane crossing from a fit, with linearised uncertainty propagation.

The entry-point covariance is C_yz = J C_θ Jᵀ, where J = ∂(y, z)_cross / ∂θ (central finite differences over all fitted
parameters: v0 and, in Stage 3, the spin components).
This propagates measurement noise only. Model uncertainty (missing physics, uncertain coefficients) is not
included; Stage 4 adds it.
"""
from dataclasses import dataclass

import numpy as np

from .constants import P0, Ball, Goal
from .integrate import simulate
from .inverse import unpack
from .outcome import classify


@dataclass
class Prediction:
    t: float                 # flight time to the goal plane [s]
    yz: np.ndarray           # predicted entry point (y, z) [m]
    cov_yz: np.ndarray       # 2×2 covariance of (y, z) [m^2]
    outcome: str             # outcome class of the nominal prediction
    speed_at_goal: float     # [m/s]

    @property
    def sigma_yz(self):
        return np.sqrt(np.diag(self.cov_yz))


def _cross(theta, fit_spin, forces, params, r0, goal):
    v0, p = unpack(theta, params, fit_spin)
    _, c = simulate(r0, v0, forces, p, goal=goal, dense=False)
    if c is None:
        raise ValueError("trajectory does not reach the goal plane")
    return c


def predict(fit, forces, params=None, r0=P0, goal=Goal(), ball=Ball(), h=None):
    theta = fit.theta
    c = _cross(theta, fit.fit_spin, forces, params, r0, goal)
    J = np.zeros((2, theta.size))
    for i in range(theta.size):
        d = np.zeros(theta.size)
        d[i] = h if h is not None else 1e-5 * max(1.0, abs(theta[i]))
        yp = _cross(theta + d, fit.fit_spin, forces, params, r0, goal).position[1:]
        ym = _cross(theta - d, fit.fit_spin, forces, params, r0, goal).position[1:]
        J[:, i] = (yp - ym) / (2 * d[i])
    yz = c.position[1:]
    return Prediction(c.t, yz, J @ fit.cov @ J.T, classify(*yz, ball=ball, goal=goal), float(np.linalg.norm(c.velocity)))
