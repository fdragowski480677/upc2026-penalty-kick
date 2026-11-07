"""Physical constants, ball and goal geometry, and the competition test case.

Coordinates follow the problem statement: origin at the penalty mark, x towards the goal,
y lateral, z vertical (up). Units: SI (m, s, kg).
"""
from dataclasses import dataclass

import numpy as np

#: Standard gravitational acceleration [m/s^2] (the local value varies by about ±0.03 %; negligible here).
G = 9.81


@dataclass(frozen=True)
class Ball:
    """FIFA size-5 ball (IFAB Law 2: circumference 68-70 cm, mass 410-450 g)."""
    mass: float = 0.43    # kg, mid-range of Law 2
    radius: float = 0.11  # m, circumference 69.1 cm


@dataclass(frozen=True)
class Air:
    """Still air at about 20 °C and sea level. Wind is neglected (problem statement: none given)."""
    density: float = 1.20               # kg/m^3
    kinematic_viscosity: float = 1.5e-5  # m^2/s (μ ≈ 1.81e-5 Pa·s)


@dataclass(frozen=True)
class Goal:
    """Goal frame (IFAB Law 1). Dimensions are measured between the inner edges of the posts
    and to the lower edge of the crossbar. Posts and bar are at most 12 cm wide."""
    x: float = 11.0           # m, goal plane (problem statement)
    half_width: float = 3.66  # m
    height: float = 2.44      # m
    frame_width: float = 0.12  # m, Law 1 maximum post/bar width


@dataclass(frozen=True)
class Observation:
    """A measured ball-centre position at time t, with isotropic standard deviation sigma per coordinate."""
    t: float
    position: np.ndarray
    sigma: float


#: Initial ball-centre position at t = 0 (problem statement). Treated as exact in Stages 1-3.
P0 = np.array([0.0, 0.0, 0.11])

#: Measurement noise per coordinate [m] (team decision, see docs/roadmap.md).
SIGMA_OBS = 0.01

#: Competition test case.
TEST_CASE = (
    Observation(0.05, np.array([1.50, 0.45, 0.44]), SIGMA_OBS),
    Observation(0.10, np.array([2.96, 0.86, 0.74]), SIGMA_OBS),
)
