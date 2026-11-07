"""Vectorised fixed-step RK4 integrator for many trajectories at once (Stage 4 posterior sampling).

It implements exactly the same physics as ``forces.py`` (gravity, drag with spin term, Magnus with any lift model,
spin decay, seam side force), but with every walker or sample as a row of a NumPy array. Equivalence with the reference
DOP853 integrator is enforced by tests (< 1e-6 m in position at 0.05/0.10 s and at the goal-plane crossing).

Per-trajectory parameters (arrays of length N): v0 (N,3), spin (N,3), cd0 (N), rho (N), seam (N,2), and optionally
mass (N), radius (N), nu (N) (Stage 4 Monte Carlo over the ball and the climate; defaults come from Settings), and wind (N,3)
(Stage 6; default 0).
Shared settings: lift model, spin-drag slope, spin-decay k, default ball, default kinematic viscosity.
"""
from dataclasses import dataclass

import numpy as np

from .coefficients import CL_CURVES, LinearCL, ReInterpCL, SaturatedCL, TabulatedCL
from .constants import G, Air, Ball, Goal

_Z = np.array([0.0, 0.0, 1.0])


def cl_vectorised(model, S, Re, speed):
    if isinstance(model, TabulatedCL):
        pts = CL_CURVES[model.curve][1]
        return np.interp(S, pts[:, 0], pts[:, 1])
    if isinstance(model, ReInterpCL):
        lo, hi = CL_CURVES[model.low], CL_CURVES[model.high]
        w = np.clip((Re - lo[0]) / (hi[0] - lo[0]), 0.0, 1.0)
        return (1 - w) * np.interp(S, lo[1][:, 0], lo[1][:, 1]) + w * np.interp(S, hi[1][:, 0], hi[1][:, 1])
    if isinstance(model, LinearCL):
        return model.slope * S
    if isinstance(model, SaturatedCL):
        return model.slope * S * speed / model.v_ref
    raise TypeError(f"no vectorised form for {model!r}")


@dataclass
class Settings:
    lift_model: object
    spin_drag_slope: float = 0.47
    spin_decay_k: float = 0.0
    ball: Ball = Ball()
    air: Air = Air()  # only the kinematic viscosity is used here; ρ is per trajectory


def _unit(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def accel(V, path, spin0, cd0, rho, seam, mass, radius, nu, wind, st):
    V = V - wind                                   # air-relative velocity (Stage 6; wind = 0 by default)
    speed = np.linalg.norm(V, axis=1)
    Re = speed * 2 * radius / nu
    K = 0.5 * rho * np.pi * radius**2 / mass
    w = spin0 if st.spin_decay_k == 0.0 else spin0 * np.exp(-st.spin_decay_k * path / radius)[:, None]
    w_perp = w - (np.sum(w * V, axis=1) / speed**2)[:, None] * V
    wn = np.linalg.norm(w_perp, axis=1)
    S = radius * wn / speed
    cd = cd0 + st.spin_drag_slope * S
    a = -(K * cd * speed)[:, None] * V
    cl = cl_vectorised(st.lift_model, S, Re, speed)
    with np.errstate(invalid="ignore", divide="ignore"):
        direction = np.cross(w_perp, V) / (wn * speed)[:, None]
    direction[wn == 0.0] = 0.0
    a += (K * cl * speed**2)[:, None] * direction
    vh = V / speed[:, None]
    e1 = _unit(np.cross(_Z, vh))
    e2 = np.cross(vh, e1)
    a += (K * speed**2)[:, None] * (seam[:, :1] * e1 + seam[:, 1:2] * e2)
    a[:, 2] -= G
    return a


def _deriv(Y, p, st):
    V = Y[:, 3:6]
    return np.concatenate((V, accel(V, Y[:, 6], *p, st), np.linalg.norm(V, axis=1)[:, None]), axis=1)


def _rk4(Y, h, p, st):
    k1 = _deriv(Y, p, st)
    k2 = _deriv(Y + 0.5 * h * k1, p, st)
    k3 = _deriv(Y + 0.5 * h * k2, p, st)
    k4 = _deriv(Y + h * k3, p, st)
    return Y + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def _params(v0, spin, cd0, rho, seam, mass, radius, nu, wind, st):
    n = v0.shape[0]
    full = lambda x, d: np.full(n, d) if x is None else np.asarray(x, dtype=float)
    w = np.zeros((n, 3)) if wind is None else np.asarray(wind, dtype=float)
    return (spin, cd0, rho, seam, full(mass, st.ball.mass), full(radius, st.ball.radius), full(nu, st.air.kinematic_viscosity), w)


def _initial(r0, v0):
    n = v0.shape[0]
    return np.concatenate((np.broadcast_to(r0, (n, 3)), v0, np.zeros((n, 1))), axis=1)


def positions(r0, v0, spin, cd0, rho, seam, st, times=(0.05, 0.10), dt=1e-3, mass=None, radius=None, nu=None, wind=None):
    """Positions at the given times (which must be multiples of dt), shape (N, len(times), 3)."""
    Y = _initial(r0, v0)
    p = _params(v0, spin, cd0, rho, seam, mass, radius, nu, wind, st)
    out, t, k = [], 0.0, 0
    for target in times:
        nsteps = int(round((target - t) / dt))
        for _ in range(nsteps):
            Y = _rk4(Y, dt, p, st)
        t = target
        out.append(Y[:, :3].copy())
    return np.stack(out, axis=1)


def crossings(r0, v0, spin, cd0, rho, seam, st, goal=Goal(), dt=5e-4, t_max=1.5, mass=None, radius=None, nu=None, wind=None):
    """Goal-plane crossing (t, y, z) for every trajectory; NaN if the ball lands (centre at z = R) or never arrives."""
    n = v0.shape[0]
    Y = _initial(r0, v0)
    p = _params(v0, spin, cd0, rho, seam, mass, radius, nu, wind, st)
    res = np.full((n, 3), np.nan)
    active = np.ones(n, dtype=bool)
    t = 0.0
    while active.any() and t < t_max:
        Yn = _rk4(Y, dt, p, st)
        hit = active & (Y[:, 0] < goal.x) & (Yn[:, 0] >= goal.x)
        if hit.any():
            # crossing time by linear interpolation in x, then cubic Hermite for y, z (error ≪ 1 µm at dt = 0.5 ms)
            x0, x1 = Y[hit, 0], Yn[hit, 0]
            s = (goal.x - x0) / (x1 - x0)
            d0 = _deriv(Y[hit], tuple(q[hit] for q in p), st)[:, 1:3] * dt
            d1 = _deriv(Yn[hit], tuple(q[hit] for q in p), st)[:, 1:3] * dt
            h00, h10, h01, h11 = 2*s**3 - 3*s**2 + 1, s**3 - 2*s**2 + s, -2*s**3 + 3*s**2, s**3 - s**2
            yz = (h00[:, None] * Y[hit, 1:3] + h10[:, None] * d0 + h01[:, None] * Yn[hit, 1:3] + h11[:, None] * d1)
            res[hit] = np.column_stack((t + s * dt, yz))
            active &= ~hit
        landed = active & (Yn[:, 2] < p[5])
        active &= ~landed
        Y, t = Yn, t + dt
    return res
