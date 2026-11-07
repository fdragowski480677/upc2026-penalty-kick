"""Classification of the goal-plane crossing (team definition, docs/roadmap.md, open decision 5).

Geometry (2-D approximation in the plane x = goal.x): the posts are rectangles
y ∈ ±[w/2… w/2 + f], z ∈ [0, h + f], and the crossbar is z ∈ [h, h + f], |y| ≤ w/2 + f, with
w/2 = half_width, h = height and f = frame_width. The ball is a disc of radius R centred at the crossing point.
Approximations: the frame's depth and round cross-section, and the ball's obliquity through the plane, are ignored
(all are effects of ≲ 1 cm).
"""
import numpy as np

from .constants import Ball, Goal

CLEAN, FRAME, MISS = "clean entry", "frame contact", "miss"


def _dist_to_rect(y, z, y0, y1, z0, z1):
    dy = max(y0 - y, 0.0, y - y1)
    dz = max(z0 - z, 0.0, z - z1)
    return float(np.hypot(dy, dz))


def distance_to_frame(y, z, goal=Goal()):
    """Shortest distance from the ball centre (y, z) to the goal frame, in the goal plane [m]."""
    a, h, f = goal.half_width, goal.height, goal.frame_width
    return min(
        _dist_to_rect(y, z, a, a + f, 0.0, h + f),     # right post
        _dist_to_rect(y, z, -a - f, -a, 0.0, h + f),   # left post
        _dist_to_rect(y, z, -a - f, a + f, h, h + f),  # crossbar
    )


def classify(y, z, ball=Ball(), goal=Goal()):
    """Return CLEAN, FRAME or MISS for a ball centre crossing the goal plane at (y, z)."""
    if distance_to_frame(y, z, goal) < ball.radius:
        return FRAME
    inside = abs(y) < goal.half_width and z < goal.height
    return CLEAN if inside else MISS
