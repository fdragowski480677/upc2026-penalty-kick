"""Force models, written as accelerations a = F/m.

Every force has the same signature, ``accel(t, r, v, params, path=0.0) -> ndarray(3)``, so the dynamics
module can sum any selection of them (``path`` = arc length flown, used for spin decay).
Stage 1: gravity. Stage 2: aerodynamic drag. Stage 3: Magnus/lift and spin-dependent drag.

Writing accelerations, not forces, avoids mixing force and acceleration terms in one equation
(the unit error found in the 2022 report B-358; see docs/research/2022-reports-analysis.md §3.4).
"""
from dataclasses import dataclass, field

import numpy as np

from .coefficients import SPIN_DRAG_SLOPES, ConstantCD, TabulatedCL
from .constants import G, Air, Ball

_GRAVITY = np.array([0.0, 0.0, -G])


def gravity(t, r, v, params, path=0.0):
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
    # --- Stage 3 (all inactive while spin = 0, so Stages 1-2 are unchanged) ---
    spin: np.ndarray = field(default_factory=lambda: np.zeros(3))   # initial spin vector ω₀ [rad/s], axis fixed in space
    lift_model: object = field(default_factory=TabulatedCL)         # anything with .cl(S, re, speed)
    spin_drag_slope: float = SPIN_DRAG_SLOPES["asai2007"]           # k_s in C_D = C_D0 + k_s·S
    spin_decay_k: float = 0.0                                       # k in dω/dt = −k ω |v| / R
    # --- Stage 4 nuisance: steady seam/orientation side force, coefficients along e1 = ẑ×v̂ and e2 = v̂×e1 ---
    seam_coeffs: tuple = (0.0, 0.0)
    # --- Stage 6: steady, uniform wind (ground frame) [m/s]; the aerodynamic forces act on the air-relative velocity v − w ---
    wind: np.ndarray = field(default_factory=lambda: np.zeros(3))


def reynolds(speed, params):
    """Re = v·D/ν, with D = 2R."""
    return speed * 2.0 * params.ball.radius / params.air.kinematic_viscosity


def _air_relative(v, params):
    """Velocity of the ball relative to the air, v − w [theory]. All aerodynamic forces, Re and S use it (Stage 6)."""
    w = params.wind
    return v if not np.any(w) else v - w


def drag(t, r, v, params, path=0.0):
    """Quadratic aerodynamic drag [theory]:  a = −(ρ C_D A / 2m) |v| v,  with A = πR².

    The velocity is relative to the air (no wind). C_D comes from params.drag_model at the instantaneous Re,
    so a speed-dependent model is evaluated along the trajectory, not frozen at v₀ (the B-471 issue).
    With wind (Stage 6), v is the air-relative velocity.
    """
    v = _air_relative(v, params)
    speed = float(np.sqrt(v @ v))
    if speed == 0.0:
        return np.zeros(3)
    b, air = params.ball, params.air
    k = 0.5 * air.density * np.pi * b.radius**2 / b.mass
    cd = params.drag_model.cd(reynolds(speed, params)) + params.spin_drag_slope * spin_parameter(v, params, path)[0]
    return -k * cd * speed * v


def spin_vector(params, path=0.0):
    """ω(s) = ω₀ exp(−k s / R): the exact solution of dω/dt = −k ω |v| / R with a fixed axis (s = arc length)."""
    if params.spin_decay_k == 0.0:
        return params.spin
    return params.spin * np.exp(-params.spin_decay_k * path / params.ball.radius)


def spin_parameter(v, params, path=0.0):
    """Return (S, ω⊥): S = R|ω⊥|/|v|, where ω⊥ is the spin component perpendicular to v (only it produces a force)."""
    w = spin_vector(params, path)
    vv = v @ v
    if vv == 0.0 or not np.any(w):
        return 0.0, np.zeros(3)
    w_perp = w - (w @ v) / vv * v
    return params.ball.radius * float(np.sqrt(w_perp @ w_perp)) / float(np.sqrt(vv)), w_perp


def magnus(t, r, v, params, path=0.0):
    """Magnus (lift) force [theory + lit]:  a = (ρ A / 2m) C_L(S, Re) |v|² (ω⊥ × v̂)/|ω⊥|.

    The direction is ω × v (backspin gives lift up; spin about +z curves a +x-moving ball towards +y). The magnitude uses a
    measured C_L(S), never the inviscid (16/3)S, which overestimates it by about 4× (docs/research/2022-reports-analysis.md §3.2).
    """
    v = _air_relative(v, params)
    s, w_perp = spin_parameter(v, params, path)
    if s == 0.0:
        return np.zeros(3)
    speed = float(np.sqrt(v @ v))
    b, air = params.ball, params.air
    k = 0.5 * air.density * np.pi * b.radius**2 / b.mass
    cl = params.lift_model.cl(s, reynolds(speed, params), speed)
    direction = np.cross(w_perp, v) / (float(np.sqrt(w_perp @ w_perp)) * speed)
    return k * cl * speed**2 * direction


def seam_force(t, r, v, params, path=0.0):
    """Steady seam/orientation side force [lit: Barber 2009; Kray 2014]: a = (ρA/2m) v² (c1 ê1 + c2 ê2).

    ê1 = ẑ×v̂/|ẑ×v̂| (horizontal ⊥ v) and ê2 = v̂×ê1. At ≥ 3 rev/s, spin averages the orientation-dependent part, so only a
    small steady residual remains (|C_S| ≲ 0.03–0.05). This is a Stage 4 uncertainty term; it is zero by default.
    """
    c1, c2 = params.seam_coeffs
    if c1 == 0.0 and c2 == 0.0:
        return np.zeros(3)
    v = _air_relative(v, params)
    speed = float(np.sqrt(v @ v))
    vh = v / speed
    e1 = np.cross([0.0, 0.0, 1.0], vh)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(vh, e1)
    b, air = params.ball, params.air
    k = 0.5 * air.density * np.pi * b.radius**2 / b.mass
    return k * speed**2 * (c1 * e1 + c2 * e2)
