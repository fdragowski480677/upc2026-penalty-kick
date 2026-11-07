"""Equations of motion: assemble the first-order ODE  d/dt (r, v, s) = (v, Σ a_i, |v|).

State: position r (3), velocity v (3) and arc length s travelled (1). The arc length is needed for spin decay
(Stage 3): with dω/dt = −k ω |v| / R the spin depends only on the distance flown, ω = ω₀ exp(−k s / R), exactly.
The spin axis is fixed in space (gyroscopic stability; the aerodynamic torque only reduces |ω|).
"""
import numpy as np


def make_rhs(forces, params=None):
    """Return f(t, y) for scipy.integrate.solve_ivp, with state y = [x, y, z, vx, vy, vz, s].

    forces: sequence of acceleration functions accel(t, r, v, params, path=s) (see forces.py).
    params: an object passed unchanged to every force (coefficients, ball properties, …).
    """
    forces = tuple(forces)

    def rhs(t, y):
        r, v, path = y[:3], y[3:6], y[6]
        a = np.zeros(3)
        for f in forces:
            a = a + f(t, r, v, params, path=path)
        return np.concatenate((v, a, [np.sqrt(v @ v)]))

    return rhs
