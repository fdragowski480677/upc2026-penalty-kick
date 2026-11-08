"""Stage 5: impact of the spinning ball on the goal frame (posts and crossbar).

Physics [theory + lit]:
* Rigid-body impact of a sphere (mass m, radius R, I = α m R², thin shell α ≈ 2/3) on a fixed, round frame member (cylinder of
  radius r_p = 0.06 m, i.e. a 120 mm round post; IFAB Law 1 maximum). The normal n points from the member axis to the ball centre.
* Normal: v_n' = −e_n v_n, with the speed-dependent coefficient of restitution of an elite match ball measured on a rigid plate,
  e_n(v) ≈ 0.95 − 0.0072 |v_n| [ours, a fit to Price et al. 2007, Fig. 4; 0.89 at 9 m/s to 0.72 at 32 m/s].
* Tangential: the contact point either grips (tangential COR e_x; the contact-point tangential velocity becomes −e_x v_t) or slides
  throughout (Coulomb, J_t = μ J_n), whichever needs the smaller impulse [lit: Cross 2002, 2005 (Brody/Cross bounce model)].
  For a sphere the tangential effective mass is m/(1 + 1/α), so the grip impulse is J_t = m (1 + e_x) |v_t| / (1 + 1/α).
* The normal force acts through the centre (offset D = 0; Cross 2005 finds D ≈ 0 near normal incidence, and 2–3 mm when oblique, a second-order effect).
* Fixed geometry assumption: the goal plane x = 11 m is the front face of the goal line and the frame. Member axes are at x = 11 + r_p,
  posts at y = ±(3.66 + r_p), and the bar at z = 2.44 + r_p. The whole ball is over the line once its centre passes x = 11 + 2 r_p + R.
Uncertain parameters (no football-on-goalpost data in our sources): e_x, μ, and the e_n offset are Monte Carlo inputs (Stage 5 priors).
"""
from dataclasses import dataclass, replace

import numpy as np
from scipy.integrate import solve_ivp

from .constants import Ball, Goal
from .dynamics import make_rhs
from .integrate import ATOL, RTOL

CLEAN_GOAL, GOAL_OFF_FRAME, MISS_OFF_FRAME, MISS = "clean goal", "goal off the frame", "miss off the frame", "miss"


@dataclass(frozen=True)
class FrameImpact:
    alpha: float = 2.0 / 3.0       # I = α m R² (thin spherical shell)
    e_x: float = 0.1               # tangential COR when gripping (Cross: 0.05–0.2 for tennis balls; football unknown)
    mu: float = 0.5                # sliding friction ball–post (unknown for football on painted aluminium)
    e_n_offset: float = 0.0        # additive shift of Price's e_n(v), for ball-to-ball and pressure scatter
    post_radius: float = 0.06      # m, round 120 mm profile


def e_normal(vn, imp=FrameImpact()):
    return float(np.clip(0.95 - 0.0072 * abs(vn) + imp.e_n_offset, 0.5, 0.97))


def bounce(v, w, n, ball=Ball(), imp=FrameImpact()):
    """Post-impact (v', ω') for a sphere hitting a fixed surface with outward unit normal n (pointing to the ball centre)."""
    m, R = ball.mass, ball.radius
    I = imp.alpha * m * R**2
    r = -R * n                                  # centre → contact point
    vn = float(v @ n)
    if vn >= 0.0:                               # separating: no impact
        return v.copy(), w.copy()
    vc = v + np.cross(w, r)
    vt = vc - (vc @ n) * n
    s = float(np.linalg.norm(vt))
    Jn = -m * (1.0 + e_normal(vn, imp)) * vn
    J = Jn * n
    if s > 1e-12:
        t_hat = vt / s
        Jt = min(m * (1.0 + imp.e_x) * s / (1.0 + 1.0 / imp.alpha), imp.mu * Jn)
        J = J - Jt * t_hat
    return v + J / m, w + np.cross(r, J) / I


def _members(goal=Goal(), rp=0.06):
    """Frame members as segments (P, Q) of their axes."""
    xa, a, h = goal.x + rp, goal.half_width + rp, goal.height + rp
    return [(np.array([xa, a, 0.0]), np.array([xa, a, h])),       # right post
            (np.array([xa, -a, 0.0]), np.array([xa, -a, h])),     # left post
            (np.array([xa, -a, h]), np.array([xa, a, h]))]        # crossbar


def _closest(p, P, Q):
    d = Q - P
    t = np.clip((p - P) @ d / (d @ d), 0.0, 1.0)
    return P + t * d


def frame_gap(p, ball=Ball(), goal=Goal(), rp=0.06):
    """Smallest (distance from the ball centre to a member axis) − (R + r_p), and the outward normal. Negative means overlap."""
    best, normal = np.inf, None
    for P, Q in _members(goal, rp):
        c = _closest(p, P, Q)
        d = float(np.linalg.norm(p - c))
        if d - (ball.radius + rp) < best:
            best, normal = d - (ball.radius + rp), (p - c) / d
    return best, normal


def resolve(r0, v0, forces, params, ball=Ball(), goal=Goal(), imp=FrameImpact(), t_max=1.5, max_impacts=3, record=False):
    """Fly from (r0, v0) with ``params.spin``, handling impacts on the frame, until the outcome is decided.

    Returns (outcome, info). Outcomes: CLEAN_GOAL / GOAL_OFF_FRAME (whole ball over the line inside the frame after ≥ 1 frame
    impact) / MISS_OFF_FRAME / MISS. info holds the impact count and the first impact's point and normal speed.
    """
    rp = imp.post_radius
    x_in = goal.x + 2 * rp + ball.radius
    p, t0, state = replace(params), 0.0, np.concatenate((r0, v0, [0.0]))
    impacts, first = 0, None
    segments, spins = [], [p.spin.copy()]      # recorded only if record=True (figures)

    def ev_contact(t, s):
        return frame_gap(s[:3], ball, goal, rp)[0]
    ev_contact.terminal, ev_contact.direction = True, -1.0

    def ev_over_line(t, s):
        return s[0] - x_in
    ev_over_line.terminal, ev_over_line.direction = True, 1.0

    def ev_back(t, s):                       # rebounded back into the field
        return s[0] - (goal.x - 1.0)
    ev_back.terminal, ev_back.direction = True, -1.0

    def ev_ground(t, s):
        return s[2] - ball.radius
    ev_ground.terminal, ev_ground.direction = True, -1.0

    while t0 < t_max:
        # max_step: events are only detected as sign changes between steps; the contact zone (≈ 2(R + r_p) ≈ 0.34 m along the
        # path) must never fit inside one step (at 30 m/s and 1 ms the ball moves 3 cm).
        sol = solve_ivp(make_rhs(forces, p), (t0, t_max), state, method="DOP853", rtol=RTOL, atol=ATOL, max_step=1e-3,
                        events=(ev_contact, ev_over_line, ev_back, ev_ground))
        hit = [len(te) > 0 for te in sol.t_events]
        if record:
            segments.append(sol.y[:3].copy())
        if hit[0] and impacts < max_impacts:
            s = sol.y_events[0][0]
            _, n = frame_gap(s[:3], ball, goal, rp)
            v_new, w_new = bounce(s[3:6], p.spin, n, ball, imp)
            if first is None:
                first = {"point": s[:3].tolist(), "vn": float(s[3:6] @ n), "t": float(sol.t_events[0][0])}
            impacts += 1
            p = replace(p, spin=w_new)
            spins.append(w_new.copy())
            # step slightly off the surface to avoid re-triggering the same contact event
            state = np.concatenate((s[:3] + 1e-6 * n, v_new, [s[6]]))
            t0 = float(sol.t_events[0][0])
            continue
        info = {"impacts": impacts, "first_impact": first}
        if record:
            info["path"], info["spins"] = segments, spins
            if hit[1]:
                info["final_state"] = sol.y_events[1][0].copy()     # state when the whole ball is over the line
        if hit[1]:
            y, z = sol.y_events[1][0][1:3]
            inside = abs(y) < goal.half_width and z < goal.height
            if inside:
                return (GOAL_OFF_FRAME if impacts else CLEAN_GOAL), info
            return (MISS_OFF_FRAME if impacts else MISS), info
        return (MISS_OFF_FRAME if impacts else MISS), info
    return (MISS_OFF_FRAME if impacts else MISS), {"impacts": impacts, "first_impact": first}
