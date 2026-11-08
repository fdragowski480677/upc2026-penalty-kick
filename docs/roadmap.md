# Preliminary development roadmap (UPC 2026, Problem B)

Guiding rule (CLAUDE.md §3): add one physical effect at a time. Each stage keeps a **fixed interface**
(observations in → entry-point estimate + uncertainty out), so all stages can be compared on the same
test case and on synthetic data. Each stage is merged and tagged only after its tests pass and it has been reviewed.

Proposed package layout, introduced as it is needed:
```
src/penalty/
  constants.py      # ball, air, goal geometry (with sources)
  forces.py         # gravity, drag, magnus — each a separate function
  coefficients.py   # C_D(Re), C_L(S) models
  dynamics.py       # ODE right-hand side assembled from selected forces
  integrate.py      # solve_ivp wrapper + goal-plane event
  inverse.py        # fitting/inference from observations
  uncertainty.py    # noise models, Monte Carlo / posterior sampling
tests/              # analytic-limit and regression tests
docs/               # physics notes per stage
```

| Stage | Physics added | Inverse method | Key question answered | Tag |
|---|---|---|---|---|
| **1. Vacuum baseline** | gravity only | exact/least-squares fit of v₀ to P₁, P₂ (P₀ fixed) | How far does simple kinematics get us? (test case: y ≈ 3.22 m) | `v0.1-gravity-baseline` |
| **2. Drag** | quadratic drag, constant $C_D$, then $C_D(Re)$ from ball data | fit v₀ (+ $C_D$) | How much does drag shift the entry point? Is $C_D$ identifiable? | `v0.2-aerodynamic-drag` |
| **3. Spin / Magnus** | $\vec F_L$ with measured-type $C_L(S)$, arbitrary ω⊥ | fit v₀, $C_D$, ω⊥ (just determined) | Does the data show spin? (preliminary: yes, ≈ 11 m/s² lateral) | `v0.3-magnus-effect` |
| **4. Uncertainty** | noise model for the positions, priors on $C_D$, $C_L$, m, R, ρ | Monte Carlo + Bayesian posterior (MCMC or importance sampling) | Most likely entry point + credible region; which parameters dominate the error? | `v0.4-uncertainty-model` |
| **5. Refinements** (each optional, only if relevant) | spin decay; t = 0 contact issue; ball-radius goal definition; C_D/C_L uncertainty per ball type | model comparison | Which neglected effects actually matter? | `v0.5-…` |
| **6. Interpretation** | goalkeeper information budget | sequential updating | How early is the prediction good enough to act on? | `v1.0-final-model` |

## Verification strategy (applies from Stage 1)
- **Analytic limits:** vacuum parabola; 1-D quadratic drag (closed form); pure Magnus circular motion
  (B-471's $\dot\theta=G\omega/m$ is a useful check, with a correct $C_L$); drag always reduces the energy.
- **Synthetic recovery:** simulate a known shot, sample positions at 0.05/0.10 s with noise, run the
  inverse method, and check that the true entry point falls inside the credible region at the stated rate (coverage test).
- **Convergence:** integrator tolerance study; results independent of the step size.
- **Regression:** every stage reports the test-case prediction in a comparison table (`results/stage_comparison.md`).

## Open decisions (to be agreed before the relevant stage)
1. ~~Ball parameters (m, R)?~~ **Revised (team decision):** sampled within IFAB Law 2 in the Stage 4 Monte Carlo, with m ~ U(410, 450 g)
   and circumference ~ U(68, 70 cm). To be tightened to FIFA Quality PRO limits once the test manual is available. (Earlier decision: fixed.)
6. **Decided (Stage 3):** spin-raised drag on by default, C_D = C_D0 + 0.47·S (Asai 2007), with switches 0 and 0.74 (Kray);
   C_L(S) nominal = Kray Re 4.62×10⁵ curve, with the other curves and the n = 1/2 limits as switches; spin decay off by default,
   with switches (`docs/stages/stage3-design.md`).
7. **Revised (Stage 4):** air density from a climate/venue Monte Carlo over the FIFA World Cup 2026 stadiums (altitude 3–2240 m,
   T 12–35 °C, RH 20–90 %, moist-air ideal gas + ISA pressure) → ρ ≈ 0.83–1.28 kg/m³; viscosity from Sutherland's law. (Earlier: U(1.10, 1.29).)
   Otherwise unchanged:
   still air (wind neglected, stated assumption); the steady seam side force (|C_S| ≲ 0.03–0.05) as an uncertainty term.
8. **Decided (Stage 4 noise):** report both noise models. *Rounding only*: the given values are exact up to their 2-decimal rounding
   (uniform ±5 mm, approximated by a Gaussian of equal variance, σ = 2.9 mm). *Tracking*: σ = 1 cm. Isotropic and independent in both cases.
9. **Decided (Stage 5):** the flight model stays rigid. In-flight deformation is of order 0.1 mm (aerodynamic load ≈ 5–12 N against an internal
   overpressure of ≈ 60–110 kPa), and the post-kick shell vibrations are damped within ≈ 10–20 ms, before the first observation at 0.05 s.
   This is a stated and checked assumption. Stage 5 adds (a) an **oblique impact of the spinning ball on a post/crossbar** (restitution
   depending on pressure, Coulomb friction, rotational inertia ⅔mR²) for the frame-contact samples, giving P(goal) including "in off the
   frame"; and (b) a **Hertz foot–ball contact model** (Ishii 2012) as a consistency check that the inferred v0 and spin are achievable.
   Needs literature: ball–rigid-surface impact versus pressure, oblique spinning impacts (Cross), FIFA Quality Programme ball tests.
2. ~~Which wind-tunnel dataset for $C_D(Re)$ and $C_L(S)$?~~ **Proposed** (literature pass, see `research/literature/README.md`):
   C_D prior 0.22 ± 0.04 (Alam 2010, Asai 2007) plus a spin term; C_L(S) from Kray 2014 at Re 4.6×10⁵. Still open: a spin-decay
   source. The main Stage 3 uncertainty is C_L(S, Re) between Kray's two supercritical curves.
3. ~~Noise model for the given positions?~~ **Decided:** realistic tracking noise, σ = 1 cm per coordinate (isotropic,
   independent) for the observations at 0.05 s and 0.10 s. Rounding (σ ≈ 2.9 mm) is negligible next to it.
4. ~~Is P₀ = (0, 0, 0.11) at t = 0 treated as exact?~~ **Decided:** exact in Stages 1–3; bias tested in Stage 5 (the
   test-case interval lengths already argue against a contact lag, see `research/literature/kick-keeper.md`).
5. ~~Definition of "enters the goal"?~~ **Decided** (team decision, following IFAB Laws of the Game, Law 1 and Law 10):
   - A goal is scored when the **whole ball** passes over the goal line between the posts and under the crossbar. The goal
     dimensions (7.32 × 2.44 m) are measured between the **inner edges** of the posts and to the lower edge of the bar.
   - **Predicted entry point** = the ball-centre position (y, z) where the trajectory crosses the plane x = 11 m (the problem's
     goal plane).
   - **Outcome classes** at that crossing, for a ball of radius R:
     - *clean entry*: |y| ≤ 3.66 − R and z ≤ 2.44 − R. The ball passes without touching the frame.
     - *frame contact*: the centre comes within R of a post or the bar. The ball touches the frame and may rebound out
       or deflect in (for example with spin, "in off the post"). **Not modelled in Stages 1–4**; reported as a separate
       probability. An optional Stage 5 collision model (restitution, friction, spin) could decide in/out.
     - *miss*: the crossing is outside the frame.
   - The whole ball is over the line after about R/v_x ≈ 4 ms more of flight, a lateral shift of ≈ 1–2 cm. This is
     neglected in the entry point and noted as a systematic.

10. **Decided (Stage 5):** derive a speed-dependent spin prior from the foot–ball contact model (Asai 2002 speed–spin trade-off;
    Ishii 2012), because a 32.6 m/s shot is more plausibly low-spin. Stage 4 keeps the log-normal prior and reports a log-uniform sensitivity case.
