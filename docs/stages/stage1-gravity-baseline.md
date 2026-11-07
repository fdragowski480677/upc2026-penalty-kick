# Stage 1: gravity-only baseline

## Physics [theory]
Point-mass projectile in uniform gravity:

$$\ddot{\vec r} = -g\,\hat z,\qquad \vec r(0)=P_0=(0,0,0.11)\ \text{m},\qquad \vec v(0)=\vec v_0 \ (\text{unknown}).$$

Neglected on purpose (added in later stages): drag (Stage 2), Magnus/lift (Stage 3), spin decay and frame collisions (Stage 5).
Buoyancy is 0.16 % of g, so it is neglected permanently.

## Inverse method
- **Unknowns:** $\vec v_0$ (3). **Data:** positions at 0.05 s and 0.10 s (6 numbers), with independent Gaussian noise of σ = 1 cm
  per coordinate (team decision). $P_0$ is exact (team decision).
- **Estimator:** weighted least squares, which is maximum likelihood for Gaussian noise. The covariance is $(J^\top W J)^{-1}$.
  The goodness of fit is $\chi^2$ with 6 − 3 = 3 degrees of freedom.
- **Prediction:** integrate to the event x = 11 m (DOP853, rtol 1e-10). The (y, z) covariance comes from linear propagation, $J C_{v_0} J^\top$.
- **Outcome:** clean entry / frame contact / miss, using the IFAB-based definition in `docs/roadmap.md` (open decision 5).

Code: `src/penalty/` (`forces.gravity`, `integrate.simulate`, `inverse.fit_launch_velocity`, `predict.predict`, `outcome.classify`).

## Verification (`tests/test_stage1_gravity.py`, 18 tests, all passing)
- The integrator reproduces the analytic parabola to < 1e-9 m. The crossing time is exact to 1e-10 s. Energy is conserved to 1e-8.
- The fit recovers v₀ exactly from noise-free data. It matches the closed-form linear least squares, and its covariance equals σ²/Σt².
- χ² is calibrated: the Monte Carlo mean is ≈ 3 = dof with the correct model.
- The linearised entry-point σ matches a 300-sample Monte Carlo to within 15 %.
- Outcome classification is checked at the posts, the bar and the corners.

## Result for the test case

| Quantity | Value |
|---|---|
| v₀ | (29.68, 8.68, 6.80) m/s, \|v₀\| = 31.66 m/s, σ = 0.09 m/s per component |
| Launch angles | elevation 12.4°, azimuth 16.3° |
| Residuals (model − data) | t = 0.05 s: (−1.6, −1.6, −0.2) cm; t = 0.10 s: (+0.8, +0.8, +0.1) cm |
| χ² / dof | 6.5 / 3 (p = 0.09) |
| Flight time to goal plane | 0.371 s |
| **Entry point (y, z)** | **(3.217, 1.957) m ± (0.035, 0.033) m** (1σ, measurement noise only) |
| Outcome | clean entry (≈ 33 cm inside the post) |

## Interpretation [ours]
1. **Gravity alone is *not* statistically rejected at σ = 1 cm (p = 0.09).** The extra acceleration the data suggests,
   $\bar a - \vec g \approx (-16, -16, -2)$ m/s², has an uncertainty of $\sqrt5\,\sigma/\Delta t^2 \approx 9$ m/s² per component
   (three points, $P_0$ exact). So the sideways component is only ≈ 1.8σ. **This corrects §5 of
   `research/2022-reports-analysis.md`**, which used rounding-only noise (σ ≈ 2.9 mm) and called the spin signal 4–5σ.
2. **Physics, not just the data, must therefore decide the model.** Drag at 32 m/s is physically certain: C_D ≈ 0.22 gives
   ≈ 12 m/s² [lit: Alam 2010 and others]. The preliminary drag + lift fit predicts y ≈ 2.65 m. **The model-choice difference
   (≈ 0.57 m) is ≈ 15× the noise-only σ.** The uncertainty budget of this problem is dominated by physics/model
   uncertainty, which makes Stages 2–4 essential rather than refinements.
3. **This is a baseline, not an answer.** It is biased toward the far post, because it ignores both the drag-induced loss of
   lateral speed and the curl back toward the centre.

## Reproduce
```bash
.venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python scripts/run_stage1.py
```
