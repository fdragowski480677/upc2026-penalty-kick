"""Force models, written as accelerations a = F/m.

Every force has the same signature, ``accel(t, r, v, params) -> ndarray(3)``, so the dynamics
module can sum any selection of them. Stage 1: gravity. Stage 2: aerodynamic drag.
Magnus/lift (Stage 3) will be added as a further function with the same signature.

Writing accelerations, not forces, avoids mixing force and acceleration terms in one equation
(the unit error found in the 2022 report B-358; see docs/research/2022-reports-analysis.md §3.4).
"""
from dataclasses import dataclass, field

import numpy as np

from .coefficients import ConstantCD
from .constants import G, Air, Ball

_GRAVITY = np.array([0.0, 0.0, -G])


def gravity(t, r, v, params):
    """Uniform gravitational acceleration, -g ẑ [theory].

    Buoyancy (ρ_air·V/m ≈ 0.16 % of g for a football) is neglected; it is far below the
    measurement uncertainty.
    """
    return _GRAVITY


@dataclass(frozen=True)
class AeroParams:
    """Parameters shared by the aerodynamic forces."""
    ball: Ball = field(default_factory=Ball)
    air: Air = field(default_factory=Air)
    drag_model: object = field(default_factory=ConstantCD)  # anything with .cd(re)


def reynolds(speed, params):
    """Re = v·D/ν, with D = 2R."""
    return speed * 2.0 * params.ball.radius / params.air.kinematic_viscosity


def drag(t, r, v, params):
    """Quadratic aerodynamic drag [theory]:  a = −(ρ C_D A / 2m) |v| v,  with A = πR².

    The velocity is relative to the air (no wind). C_D comes from params.drag_model at the instantaneous Re,
    so a speed-dependent model is evaluated along the trajectory, not frozen at v₀ (the B-471 issue).
    """
    speed = float(np.sqrt(v @ v))
    if speed == 0.0:
        return np.zeros(3)
    b, air = params.ball, params.air
    k = 0.5 * air.density * np.pi * b.radius**2 / b.mass
    return -k * params.drag_model.cd(reynolds(speed, params)) * speed * v
