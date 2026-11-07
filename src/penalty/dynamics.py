"""Equations of motion: assemble the first-order ODE  d/dt (r, v) = (v, Σ a_i(t, r, v)).

The ball is treated as a point mass with no translational-rotational coupling in Stage 1.
The spin vector will enter as a parameter of the Magnus force in Stage 3.
"""
import numpy as np


def make_rhs(forces, params=None):
    """Return f(t, s) for scipy.integrate.solve_ivp, with state s = [x, y, z, vx, vy, vz].

    forces: sequence of acceleration functions accel(t, r, v, params) (see forces.py).
    params: an object passed unchanged to every force (coefficients, ball properties, …).
    """
    forces = tuple(forces)

    def rhs(t, s):
        r, v = s[:3], s[3:]
        a = np.zeros(3)
        for f in forces:
            a = a + f(t, r, v, params)
        return np.concatenate((v, a))

    return rhs
