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
1. Ball parameters (m, R): FIFA ranges (410–450 g, 68–70 cm circumference) used as priors or fixed?
2. ~~Which wind-tunnel dataset for $C_D(Re)$ and $C_L(S)$?~~ **Proposed** (literature pass, see `research/literature/README.md`):
   C_D prior 0.22 ± 0.04 (Alam 2010, Asai 2007) plus a spin term; C_L(S) from Kray 2014 at Re 4.6×10⁵. Still open: the
   Asai/Kray spin-drag contradiction and a spin-decay source.
3. Noise model for the given positions: rounding only (σ ≈ 2.9 mm) or realistic tracking noise (cm-level)?
4. ~~Is P₀ = (0, 0, 0.11) at t = 0 treated as exact?~~ **Decided:** exact in Stages 1–3; bias tested in Stage 5 (the
   test-case interval lengths already argue against a contact lag, see `research/literature/kick-keeper.md`).
5. Definition of "enters the goal": centre crossing x = 11 m, or the whole ball over the line?
