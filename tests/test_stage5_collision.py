"""Stage 5: frame-impact model (bounce law against Cross 2005 closed forms; geometry; goal or miss)."""
from dataclasses import replace

import numpy as np
import pytest

from penalty.collision import (CLEAN_GOAL, GOAL_OFF_FRAME, MISS, MISS_OFF_FRAME, FrameImpact, bounce, e_normal,
                               frame_gap, resolve)
from penalty.constants import Ball, Goal
from penalty.forces import AeroParams, drag, gravity, magnus

BALL = Ball()
Z = np.array([0.0, 0.0, 1.0])


def energy(v, w, alpha=2 / 3):
    return 0.5 * BALL.mass * v @ v + 0.5 * alpha * BALL.mass * BALL.radius**2 * w @ w


def test_head_on_impact_reverses_with_price_cor():
    v, w = np.array([0, 0, -20.0]), np.zeros(3)
    v2, w2 = bounce(v, w, Z)
    assert v2[2] == pytest.approx(20.0 * e_normal(20.0))
    assert np.allclose(w2, 0) and np.allclose(v2[:2], 0)


def test_price_cor_values():
    assert e_normal(9.0) == pytest.approx(0.885, abs=0.02)
    assert e_normal(32.0) == pytest.approx(0.72, abs=0.03)


def test_glancing_impact_slides_coulomb():
    v = np.array([20.0, 0, -1.0])
    v2, _ = bounce(v, np.zeros(3), Z, imp=FrameImpact(mu=0.3))
    jn = (1 + e_normal(1.0)) * 1.0
    assert v2[0] == pytest.approx(20.0 - 0.3 * jn)            # pure sliding: Δv_t = μ (1 + e_n) |v_n|


@pytest.mark.parametrize("ex", [0.0, 0.1, 0.2])
@pytest.mark.parametrize("ratio", [-1.0, 0.0, 0.5, 2.0])
def test_grip_matches_cross_2005_closed_form(ex, ratio):
    """Cross 2005, Eqs 3-4: v_x2/v_x1 = (1 − α e_x)/(1 + α) + α (1 + e_x)/(1 + α) · Rω1/v_x1 (grip, high friction)."""
    a = 2 / 3
    vx1 = 5.0
    w1 = ratio * vx1 / BALL.radius
    v, w = np.array([vx1, 0, -5.0]), np.array([0, w1, 0])     # contact velocity v_x − Rω_y, as in Cross's notation
    v2, w2 = bounce(v, w, Z, imp=FrameImpact(mu=10.0, e_x=ex, alpha=a))
    expect_v = ((1 - a * ex) / (1 + a) + a * (1 + ex) / (1 + a) * ratio) * vx1
    assert v2[0] == pytest.approx(expect_v, rel=1e-9, abs=1e-9)
    if ratio != 0:
        expect_w = ((a - ex) / (1 + a) + (1 + ex) / (1 + a) / ratio) * w1
        assert w2[1] == pytest.approx(expect_w, rel=1e-9)
    # the contact-point tangential velocity is reversed by e_x
    vc1, vc2 = vx1 - BALL.radius * w1, v2[0] - BALL.radius * w2[1]
    assert vc2 == pytest.approx(-ex * vc1, abs=1e-9)


def test_impact_never_creates_energy():
    rng = np.random.default_rng(0)
    for _ in range(200):
        v, w = rng.normal(0, 15, 3), rng.normal(0, 40, 3)
        n = rng.normal(size=3); n /= np.linalg.norm(n)
        if v @ n > 0:
            v = -v
        v2, w2 = bounce(v, w, n, imp=FrameImpact(e_x=rng.uniform(0, 0.2), mu=rng.uniform(0.2, 0.8)))
        assert energy(v2, w2) <= energy(v, w) + 1e-9


def test_frame_gap_geometry():
    g, rp, R = Goal(), 0.06, BALL.radius
    # centre exactly touching the inside of the right post at mid-height
    p = np.array([g.x + rp, g.half_width - R, 1.0])
    gap, n = frame_gap(p)
    assert gap == pytest.approx(0.0, abs=1e-12) and n == pytest.approx([0, -1, 0])
    assert frame_gap(np.array([g.x, 0.0, 1.0]))[0] > 1.0          # centre of the goal mouth: far from the frame


SHOT = dict(forces=[gravity], params=AeroParams())   # vacuum flight: exact aiming for the geometry tests


def _launch_to(y, z, speed=30.0):
    """A no-spin straight-ish launch aimed so the centre passes near (11, y, z) (gravity compensated)."""
    t = 11.0 / speed
    return np.array([speed, y / t, (z - 0.11 + 0.5 * 9.81 * t**2) / t])


def test_clean_goal_and_clean_miss():
    p0 = np.array([0, 0, 0.11])
    out, info = resolve(p0, _launch_to(1.0, 1.2), **SHOT)
    assert out == CLEAN_GOAL and info["impacts"] == 0
    out, _ = resolve(p0, _launch_to(5.0, 1.2), **SHOT)
    assert out == MISS


def test_inside_of_post_deflects_in_and_outside_deflects_out():
    """Glancing contacts (contact distance R + r_p = 0.17 m): inside at 0.16 m from the axis, outside at 0.14 m."""
    p0 = np.array([0, 0, 0.11])
    axis_y = Goal().half_width + 0.06
    out_in, info_in = resolve(p0, _launch_to(axis_y - 0.16, 1.0), **SHOT)    # clips the inside of the post
    out_out, info_out = resolve(p0, _launch_to(axis_y + 0.14, 1.0), **SHOT)  # clips the outside of the post (outward-moving shot)
    assert info_in["impacts"] >= 1 and out_in == GOAL_OFF_FRAME
    assert info_out["impacts"] >= 1 and out_out == MISS_OFF_FRAME


def test_near_head_on_post_rebounds_out():
    p0 = np.array([0, 0, 0.11])
    out, info = resolve(p0, _launch_to(Goal().half_width + 0.06 - 0.03, 1.0), **SHOT)
    assert info["impacts"] >= 1 and out == MISS_OFF_FRAME


def test_full_on_crossbar_rebounds_out():
    p0 = np.array([0, 0, 0.11])
    out, info = resolve(p0, _launch_to(0.0, Goal().height + 0.06), **SHOT)
    assert info["impacts"] >= 1 and out == MISS_OFF_FRAME
