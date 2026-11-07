"""Force models, written as accelerations a = F/m.

Every force has the same signature, ``accel(t, r, v, params) -> ndarray(3)``, so the dynamics
module can sum any selection of them. Stage 1 has gravity only. Drag (Stage 2) and Magnus/lift
(Stage 3) will be added here as further functions with the same signature.

Writing accelerations, not forces, avoids mixing force and acceleration terms in one equation
(the unit error found in the 2022 report B-358; see docs/research/2022-reports-analysis.md §3.4).
"""
import numpy as np

from .constants import G

_GRAVITY = np.array([0.0, 0.0, -G])


def gravity(t, r, v, params):
    """Uniform gravitational acceleration, -g ẑ [theory].

    Buoyancy (ρ_air·V/m ≈ 0.16 % of g for a football) is neglected; it is far below the
    measurement uncertainty.
    """
    return _GRAVITY
