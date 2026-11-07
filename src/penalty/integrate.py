"""Numerical integration with event detection at the goal plane.

DOP853 (an 8th-order Runge-Kutta method with dense output) with tight tolerances, so the
integration error stays orders of magnitude below the 1 cm measurement noise. Using an exact
event for the crossing, rather than checking "has the ball passed x = 11 at this step" as the
2022 reports did, removes step-size bias in the entry point.
"""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from .constants import Ball, Goal
from .dynamics import make_rhs

RTOL = 1e-10
ATOL = 1e-12


@dataclass
class Crossing:
    t: float               # time of crossing [s]
    position: np.ndarray   # ball-centre position at the crossing [m]
    velocity: np.ndarray   # ball velocity at the crossing [m/s]
    path: float = 0.0      # arc length flown [m]


def simulate(r0, v0, forces, params=None, t_max=2.0, goal=Goal(), ball=Ball(), dense=True):
    """Integrate from (r0, v0) at t = 0 until the ball centre crosses x = goal.x, hits the ground plane, or t_max.

    Returns (solution, crossing), where crossing is None if the goal plane is never reached.
    """
    def plane(t, s):
        return s[0] - goal.x
    plane.terminal, plane.direction = True, 1.0

    def ground(t, s):  # ball touches the ground (centre at z = R): a bounce, not modelled in Stage 1
        return s[2] - ball.radius
    ground.terminal, ground.direction = True, -1.0

    sol = solve_ivp(make_rhs(forces, params), (0.0, t_max), np.concatenate((r0, v0, [0.0])),
                    method="DOP853", rtol=RTOL, atol=ATOL, events=(plane, ground), dense_output=dense)
    if not sol.success:
        raise RuntimeError(sol.message)
    if sol.t_events[0].size:
        s = sol.y_events[0][0]
        return sol, Crossing(sol.t_events[0][0], s[:3], s[3:6], s[6])
    return sol, None


def positions_at(r0, v0, times, forces, params=None):
    """Ball-centre positions at the given times (all before the goal plane is reached), shape (len(times), 3)."""
    sol = solve_ivp(make_rhs(forces, params), (0.0, max(times)), np.concatenate((r0, v0, [0.0])),
                    method="DOP853", rtol=RTOL, atol=ATOL, dense_output=True)
    return np.array([sol.sol(t)[:3] for t in times])
