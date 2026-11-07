"""Stage 1 (gravity only): fit the test case and predict the goal-entry point.

Usage:  .venv/bin/python scripts/run_stage1.py
"""
import numpy as np

from penalty.constants import P0, TEST_CASE
from penalty.forces import gravity
from penalty.inverse import fit_launch_velocity
from penalty.predict import predict

FORCES = [gravity]


def main():
    fit = fit_launch_velocity(TEST_CASE, FORCES)
    pred = predict(fit, FORCES)
    v = fit.v0
    speed = np.linalg.norm(v)
    print("Stage 1 - gravity only (P0 exact, sigma = 1 cm)")
    print(f"  v0          = ({v[0]:.3f}, {v[1]:.3f}, {v[2]:.3f}) m/s   |v0| = {speed:.3f} m/s")
    print(f"  sigma(v0)   = {np.sqrt(np.diag(fit.cov)).round(3)} m/s")
    print(f"  elevation   = {np.degrees(np.arcsin(v[2] / speed)):.2f} deg, azimuth = {np.degrees(np.arctan2(v[1], v[0])):.2f} deg")
    print(f"  residuals   = {(fit.residuals * 100).round(2).tolist()} cm")
    print(f"  chi2/dof    = {fit.chi2:.1f} / {fit.dof}   p = {fit.p_value:.2e}")
    print(f"  t_goal      = {pred.t:.4f} s, speed at goal {pred.speed_at_goal:.2f} m/s")
    print(f"  entry (y,z) = ({pred.yz[0]:.3f}, {pred.yz[1]:.3f}) m  +- ({pred.sigma_yz[0]:.3f}, {pred.sigma_yz[1]:.3f}) m (1 sigma, noise only)")
    print(f"  outcome     = {pred.outcome}")


if __name__ == "__main__":
    main()
