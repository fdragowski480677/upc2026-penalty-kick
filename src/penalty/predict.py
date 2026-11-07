"""Forward prediction of the goal-plane crossing from a fit, with linearised uncertainty propagation.

The entry-point covariance is C_yz = J C_v0 Jᵀ, where J = ∂(y, z)_cross / ∂v0 (central finite differences).
This propagates measurement noise only. Model uncertainty (missing physics, uncertain coefficients) is not
included; Stage 4 adds it.
"""
from dataclasses import dataclass

import numpy as np

from .constants import P0, Ball, Goal
from .integrate import simulate
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


def _cross_yz(v0, forces, params, r0, goal):
    _, c = simulate(r0, v0, forces, params, goal=goal, dense=False)
    if c is None:
        raise ValueError("trajectory does not reach the goal plane")
    return c


def predict(fit, forces, params=None, r0=P0, goal=Goal(), ball=Ball(), h=1e-4):
    c = _cross_yz(fit.v0, forces, params, r0, goal)
    J = np.zeros((2, 3))
    for i in range(3):
        dv = np.zeros(3); dv[i] = h
        yp = _cross_yz(fit.v0 + dv, forces, params, r0, goal).position[1:]
        ym = _cross_yz(fit.v0 - dv, forces, params, r0, goal).position[1:]
        J[:, i] = (yp - ym) / (2 * h)
    yz = c.position[1:]
    return Prediction(c.t, yz, J @ fit.cov @ J.T, classify(*yz, ball=ball, goal=goal), float(np.linalg.norm(c.velocity)))
