# Stage 3: Magnus effect, spin-dependent drag, spin decay

Design and physics justification: `stage3-design.md`. Values and sources: `../values-audit.md`.

## Implementation
- `forces.magnus`: $\vec a_L = \frac{\rho A}{2m} C_L(S,Re)\,v^2\,\frac{\vec\omega_\perp\times\vec v}{|\vec\omega_\perp||\vec v|}$, using a measured C_L (never 16/3·S).
- `forces.drag`: $C_D = C_{D0}(Re) + k_s S$, with k_s = 0.47 by default (Asai 2007). This is inactive while there is no spin, so Stages 1–2 are unchanged.
- Spin decay: $\vec\omega = \vec\omega_0\,e^{-k s/R}$, the exact solution of $\dot\omega = -k\omega|v|/R$. The arc length s is a 7th state variable;
  the axis is fixed. The default is k = 0.
- `coefficients`: lift models (Kray 4.62/3.42×10⁵, Kray Re-interpolation, Asai 4.55×10⁵, Asai Re-interpolation, the limits n = 1 and n = 2);
  `SPIN_DRAG_SLOPES`; `SPIN_DECAY_K`.
- `inverse.fit(..., fit_spin=True)`: θ = (v0, a, b), with ω = a·e1 + b·e2 ⊥ v0. That is 5 parameters for 6 data, so dof = 1.

## Verification (`tests/test_stage3_magnus.py`, 21 tests; suite total 55, all passing)
- Direction: backspin lifts, topspin dips, sidespin about +z curls a +x ball toward +y. The force is ⊥ v and ⊥ ω⊥. Spin ∥ v gives no force.
- Magnitude equals K·C_L(S)·v². The Magnus force does no work (energy conserved with gravity).
- Pure Magnus at constant spin traces a **circle of radius 1/(K C_L)** at constant speed (to 1e-8). This is the analytic limit B-471 used, but with a correct C_L.
- The curves reproduce the digitised nodes; C_L(0) = 0; there is a plateau; the Re-interpolation bounds hold; the limit models give F ∝ v¹ and v² exactly.
- Spin drag is linear in S. Spin decay equals exp(−k s/R) in arc length, and exp(−k v t/R) at constant speed. The Asai 2020 k gives a 1–2 % loss.
- The fit recovers v0 and ω exactly from noise-free synthetic data (three lift models). The Stage 2 result is reproduced exactly with no spin.

## Result for the test case
### Unconstrained least squares (default model)
| Quantity | Value | Plausibility |
|---|---|---|
| \|v0\| | 32.58 m/s | OK (25–36) |
| Spin | **15.4 rev/s**, axis 16° from vertical (sidespin) | **OUT**: real curve kicks are ≤ 10 rev/s (Asai 2007), typically 2–8 |
| S, C_L, C_D at launch | 0.33, 0.285, **0.373** | S beyond Kray's measured range (0.23); C_D **OUT** (0.25–0.30) |
| Speed loss to goal | **23 %** | **OUT** (≈ 10 %, Wesson 2002) |
| χ² / dof | 0.19 / 1 | — |
| Entry (y, z) | (2.448, 1.979) m; linearised σ (0.07, 0.45) m | **σ not meaningful** (see below) |

### Profile likelihood in spin rate: the key result
At each fixed |ω|, refit v0 and the spin-axis angle:

| rev/s | 0.5 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| χ² | 1.73 | 1.22 | 0.83 | 0.62 | 0.48 | 0.39 | 0.35 | 0.31 | 0.27 | 0.23 | 0.19 |
| entry y (m) | 3.083 | 2.950 | 2.831 | 2.747 | 2.668 | **2.600** | 2.552 | 2.485 | 2.451 | 2.448 | 2.448 |
| entry z (m) | 1.931 | 1.947 | 1.961 | 1.969 | 1.977 | 1.984 | 1.988 | 1.991 | 1.991 | 1.987 | 1.980 |

(With k_s = 0 the χ² is equally flat, 0.86–1.05, and y is the same to within 3 mm at each spin rate.)

## Interpretation [ours]
1. **The data cannot determine the spin.** Δχ² < 1.6 across 0.5–15 rev/s. With two positions at σ = 1 cm, the sideways acceleration is
   known only to ≈ ±9 m/s² (Stage 1), so the curl is barely detected.
2. **The lateral entry point is controlled by the spin rate**, i.e. by prior knowledge: y ≈ 2.83 m at 2 rev/s, 2.60 m at 5 rev/s, and 2.45 m at
   ≥ 10 rev/s (where C_L saturates and y plateaus). The vertical entry point is robust: z ≈ 1.93–1.99 m.
3. The unconstrained fit runs to large spin because, with spin-raised drag, spin also explains a slightly larger deceleration that is in fact noise
   (C_D is constrained only to about ±0.1). The **plausibility checks catch this**, and it is the reason we must not report the unconstrained fit.
4. **Correction to `stage3-design.md`:** the statement that "the data already fix the lift during the observed window" is true only at the best
   fit. The ±2.5 cm robustness to the C_L-curve choice holds *at fixed lift*. The dominant uncertainty is the lift (spin) *magnitude*, not the curve shape.
5. The linearised σ is invalid here: at the C_L plateau, ∂y/∂ω ≈ 0. **Stage 4 must sample the posterior (e.g. MCMC) with a literature prior on spin**,
   rather than linearise.
6. Consequence for the competition answer: "the point at which the ball is most likely to enter" is a **posterior** quantity. It requires stating
   a prior on spin (from measured real kicks). This is a genuine physics insight to report, not a deficiency to hide.

## Status
Code verified. The physical point estimate is pending the team decision on how to constrain spin (prior / MAP / Stage 4). Not merged yet.
