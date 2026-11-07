# Comparative analysis of the 2022 UPC Problem B gold-medal reports

**Purpose.** Pull out of the three 2022 reports (Teams 358, 471, 480) the physics, the mathematics and the
numerical methods that matter for our 2026 problem. We evaluate them critically. We are not copying them.

**Source tags used throughout**

| Tag | Meaning |
|---|---|
| **[theory]** | Established physics / textbook result |
| **[B-358] / [B-471] / [B-480]** | Idea, equation or value taken from that 2022 report |
| **[lit]** | External literature the reports cite. *Values still to be checked in our literature pass* |
| **[ours]** | Our own analysis, critique or proposal |

> **Important difference between the problems [ours].**
> 2022: *forward design*. Which (v₀, ω₀) put the ball in an upper corner and beat the keeper?
> 2026: *inverse prediction with uncertainty*. From the ball positions at t = 0, 0.05 and 0.10 s, infer where
> the ball will most likely cross x = 11 m and how uncertain that is.
> So the 2022 trajectory models are a useful **forward model** inside our method. Their search and optimisation
> layers and their goalkeeper models matter much less to us.

---

## 1. Summary of each report

### 1.1 Team 358: "The Best Strategy for Penalty Kicks" (24 pp., Python/`odeint`)
- **Forces:** gravity, buoyancy, quadratic drag with constant $C_a = 0.4$, and Magnus force from the Kutta–Joukowski
  formula $\vec F_M = \tfrac{8}{3}\pi r^3 \rho\, (\vec\omega\times\vec v)$ (eq. 7; written there with a minus sign, see §3).
- **Spin decay:** they argue $\dot\omega = -k\omega$, estimate $k\sim10^{-3}$ s⁻¹, and conclude the spin is constant during the flight.
- **Method:** fix |v₀| = 25 m/s and ω = 15 k̂ rad/s, then sweep the launch angles (θ, φ) to find the upper-corner window.
  They also find the minimum speed v₀,min ≈ 20.17 m/s.
- **Goalkeeper:** body proportions → reach; a "vertical" and a "diving" save model (a projectile shoulder path with an
  optimised take-off angle α); a Monte-Carlo "defence probability" map (a 2-D Gaussian weighted by how many
  defence modes overlap); a "dead-angle" region (≈ triangles at the upper corners).
- **Strengths:** a full 3-D vector ODE that works for any spin axis; a clear structure; Monte Carlo over the goal face.
- **Weaknesses:** a constant $C_D$; the Magnus magnitude is far too large (§3.2); the probability map is assumed
  (a Gaussian) rather than derived; no validation and no sensitivity analysis; the appendix code has unit and
  coefficient errors (§3.4).

### 1.2 Team 471: "Analysis of Shooting Strategy in Penalty Kick" (44 pp., MATLAB, improved Euler)
- **Forces:** gravity, drag with a **speed-dependent $C_D$** (a table taken from Asai et al.'s smooth-sphere
  $C_D(Re)$ curve, interpolated with pchip; §2 Table 2), and the Magnus force $L=\tfrac{8}{3}\pi\rho\omega a^3 v$.
- **Kinematics:** spin only about the vertical axis. Because the Magnus force is then horizontal and
  perpendicular to $v_{xy}$, the heading turns at a constant rate, $\dot\theta = G\omega/m$ with $G=\tfrac{8}{3}\pi\rho a^3$ (eq. 1).
  The vertical motion and the horizontal speed are integrated separately, with a **fixed pitch angle α** (eq. 12).
- **Method:** a 4-dimensional grid search (v₀, α, θ₀, ω) with coarse-to-fine variable steps that minimises the
  distance to the corner target.
- **Goalkeeper:** a time-to-reach model (lowering the centre of mass by free fall, then a dive at constant speed
  $v_s=\sqrt{2g\cdot0.5}$ m/s). A shot is feasible if $t_{\text{ball}} < t_{\text{keeper}}$. This gives 1108 feasible strategies.
- **Extras:** a one-at-a-time **sensitivity analysis** (Fig. 20); a "model correction" for **spin decay** ($\omega=\omega_0e^{-9\pi\eta a t/m}$);
  a case study (Messi's saved penalties fall outside the "dead zone").
- **Strengths:** the only team to make $C_D$ depend on speed and to acknowledge the drag crisis; it has a
  sensitivity analysis and an explicit time-race keeper model; it improves the model iteratively (close in
  spirit to our staged philosophy).
- **Weaknesses:** the fixed-α decomposition is not physically consistent; the smooth-sphere $C_D$ table is not
  representative of footballs; $C_D$ is evaluated only at v₀, not along the path; the spin-decay correction uses
  Stokes' law far outside its validity range (§3.3); the Magnus magnitude has the same problem as 358.

### 1.3 Team 480: "Analysis of the optimal initial velocities and spins…" (19 pp., MATLAB, explicit Euler)
- **Forces:** gravity, quadratic drag ($c=0.5$), Magnus $\tfrac{8}{3}\pi\rho r^3\,\vec\omega\times\vec V$, and an **arbitrary spin axis with
  exponential spin decay** $I\dot{\vec\omega}=-\eta\vec\omega\Rightarrow\vec\omega=\vec\omega_0e^{-\mu t}$ with $\mu = 0.1$ s⁻¹ (assumed).
- **Method:** a brute-force 6-D grid over (v₀ components, ω₀ components) within ranges "from papers and videos".
  It finds about 600 upper-corner solutions, visualised as a 6-D scatter.
- **Goalkeeper:** a take-off kinematics model (a = 34.3 m/s², t_a = 0.181 s, optimal α ≈ 57.5°) and an ellipsoidal reach volume.
  The conclusion is that **bottom corners** are preferable, supported by World-Cup 2002–2018 statistics.
- **Strengths:** a general 3-D spin vector with decay; empirical penalty statistics; an honest discussion of the
  uncertain spin ranges.
- **Weaknesses:** μ is not justified; $C_D$ is constant; the integrator is first order; the appendix code flips the
  drag sign for descending balls (§3.4); there is no sensitivity analysis or validation; the "best kick" depends
  strongly on the chosen grid.

---

## 2. Side-by-side comparison

| Aspect | B-358 | B-471 | B-480 |
|---|---|---|---|
| Coordinates | y toward goal, x lateral | y toward goal | y toward goal |
| Gravity | ✓ (+ buoyancy) | ✓ | ✓ |
| Drag | quadratic, $C_D=0.4$ const | quadratic, $C_D(v)$ table (smooth sphere), fixed per shot | quadratic, $C_D=0.5$ const |
| Magnus | $\tfrac83\pi\rho r^3\,\omega\times v$, any axis | same magnitude, vertical axis only | same, any axis |
| Spin decay | argued negligible | Stokes-based "correction" | $e^{-\mu t}$, μ = 0.1 s⁻¹ assumed |
| Integrator | `odeint` (LSODA, adaptive) | improved Euler, Δt = 1e-3/1e-4 | explicit Euler, Δt = 1e-4 |
| Search | 2-D angle sweep at fixed v₀, ω | 4-D coarse-to-fine grid | 6-D brute-force grid |
| Goalkeeper | reach geometry + MC probability map | time-to-reach race | take-off kinematics, reach ellipsoid |
| Uncertainty | MC over the goal face (assumed Gaussian) | one-at-a-time sensitivity | none |
| Validation | none | case study (qualitative) | World-Cup statistics (qualitative) |
| Foot–ball impact / elasticity | — | — | — |
| Ground / bounce | — | excluded | — |

None of the three models the foot–ball impact, the ball's elasticity or its deformation, which our CLAUDE.md lists
as relevant. None treats measurement noise or the inverse problem.

---

## 3. Critical review of the shared physics

### 3.1 Drag [theory] + [lit] + [ours]
$\vec F_D = -\tfrac12\rho C_D A\,|\vec v|\,\vec v,\quad A=\pi R^2$ [theory]. All three teams use this form.

- **Reynolds number** for a penalty: $Re=\rho v D/\mu \approx 1.2\cdot 30\cdot0.22/1.8\times10^{-5}\approx 4\text{–}5\times10^5$ [ours].
  That is around or above the **drag crisis**, so $C_D$ really does depend on speed in our range.
- B-471 is the only team to model the crisis. Its table falls to $C_D=0.06$ at 30 m/s, a **smooth-sphere** value.
  Wind-tunnel data for real panelled balls has the crisis at a lower $Re_{crit}\approx1.2$–$3.1\times10^5$ and a
  supercritical (non-spinning) $C_D\approx0.15$–$0.25$. Measured directly at 30.6–33.3 m/s, the value is 0.22–0.24, against
  0.073 for a smooth sphere in the same tunnel [lit: Asai et al. 2007; Carré et al. 2005; Alam et al. 2010; Oggiano &
  Sætran 2010, verified, see `literature/drag.md`]. The smooth-sphere minimum, ≈ 0.07 at $Re\approx3.7\times10^5$
  [lit: Achenbach 1972], is exactly the origin of B-471's 0.06, and it sits right at our operating point. With $C_D=0.06$ the
  ball keeps almost all its speed. **This is a significant flaw [ours].**
- Constant $C_D=0.4$–$0.5$ (B-358, B-480) is subcritical. That overestimates the drag at 25–32 m/s.

### 3.2 Magnus / lift force [theory] + [ours]
General form: $\vec F_L = \tfrac12\rho C_L A |\vec v|^2\,\dfrac{\vec\omega\times\vec v}{|\vec\omega\times\vec v|}$, with $C_L = C_L(S, Re)$ and spin parameter $S=R\omega/v$ [theory].

All three reports use the inviscid circulation result $\vec F = \tfrac{8}{3}\pi\rho R^3\,\vec\omega\times\vec v$. Comparing with the general
form gives **$C_L = \tfrac{16}{3}S \approx 5.3\,S$** [ours]. At $S=0.2$ that is $C_L\approx1.07$, while a football measured in a wind tunnel at
$Re=4.6\times10^5$ (our regime) gives $C_L\approx0.27$ [lit: Kray et al. 2014, Fig. 9]. Free-kick trajectory fits give
0.23–0.29 [lit: Bray & Kerwin 2003] (verified, see `literature/lift-spin.md`). **So the 2022 models overestimate the curl by about
4× at S = 0.2.** The error grows with S: about 1.3× at S = 0.03 and 2.6× at S = 0.1. The measured $C_L(S)$ saturates; a good
fit at our Re is $C_L\approx0.29\,(1-e^{-S/0.072})$ [ours, fitted to Kray Fig. 9].
Each team then compensates by finding a small ω (≈ 15 rad/s) in its search. The trajectories look plausible,
but the fitted spin is not physical. For us this matters a great deal: we will be **inferring** spin from data, so
a wrong $C_L$ model would give wrong spin estimates and wrong uncertainty [ours].

### 3.3 Spin decay [theory] + [ours]
- B-358 calls it negligible but gives no real estimate. B-480 assumes μ = 0.1 s⁻¹. B-471 uses Stokes' law, $F=6\pi\eta a v$,
  which applies to *translational* creeping flow ($Re\ll1$), not to a rotating ball at $Re\sim10^5$. Their
  decay time $m/(9\pi\eta a)\approx 7\times10^3$ s means the "correction" changes essentially nothing. Yet they report
  a different optimum, which points to grid or search effects rather than physics [ours].
- Physically, the aerodynamic torque is $\tau = \tfrac12\rho C_M A R v^2$. Measured spin decay over a ~0.4 s penalty flight is
  **still unsourced**. None of the 20 reference papers measures ω(t) or a torque coefficient $C_M$. A bracketing
  estimate with $C_M\approx0.005$–$0.02$ gives a 2–9 % spin loss over 0.4 s [ours]. For now this is a ±5 % systematic,
  and it needs a dedicated source (open item). For our 0.4 s flight it is likely a second-order effect, but it should be
  *tested*, not assumed.

### 3.4 Numerical and implementation issues found in the appendices [ours]
These matter as lessons for our own code and its tests:
- **B-358 code:** acceleration and force terms are mixed. `−m*g` appears in an equation where the drag and Magnus
  terms are not divided by m, and m = 0.4 there. The effective gravity in the code is ≈ 3.9 m/s². The buoyancy
  term uses `3/4` instead of `4/3`. r = 0.108 in the text but 0.11 in the code. The printed Magnus sign is opposite
  to the physical direction $\vec\omega\times\vec v$.
- **B-480 code:** `if v_z <= 0` flips the sign of the z-drag, so the drag *accelerates* a descending ball downward.
  The text has the typo $R=-kV^2\vec V$.
- **B-471:** the pitch angle α is never updated, so gravity cannot bend the velocity direction consistently.
  $C_D$ is evaluated once at v₀.
- **General:** first-order Euler with Δt = 10⁻⁴ s is adequate but wasteful. An adaptive RK45/DOP853 with an
  event detection at x = 11 m (as B-358 started to do with `odeint`) is more accurate and much cheaper.

**→ Lesson [ours]:** unit tests against analytic limits (vacuum parabola, pure-drag 1-D solution, pure Magnus
circular motion, energy monotonicity with drag) would have caught every one of these.

### 3.5 Goalkeeper models
All three are heuristic: body proportions, rigid take-off kinematics, an assumed Gaussian (B-358).
They are relevant to 2026 only indirectly. Our problem gives the keeper's information budget explicitly
(observations up to 0.10 s), so a goalkeeper analysis could be an **interpretation layer** on top of our prediction
(see §5), not a core component.

---

## 4. What carries over to 2026

| Element | Use in 2026 | Source |
|---|---|---|
| 3-D vector ODE with gravity + drag + Magnus | Core forward model | [theory], structure as in [B-358]/[B-480] |
| Speed-dependent $C_D$ (drag crisis) | Needed at v ≈ 30 m/s; use ball data, not a smooth sphere | idea from [B-471], data [lit] |
| Arbitrary spin axis | Needed: the data shows lateral and slight vertical curl | [B-480] |
| Spin decay | Test whether it matters over 0.4 s | [B-471]/[B-480] idea, proper torque model [ours] |
| Sensitivity analysis | Basis of the uncertainty budget | [B-471] |
| Monte Carlo over the goal face | Propagate uncertainty to an entry-point distribution | idea from [B-358], applied to a posterior [ours] |
| Event-based termination at the goal plane | Stopping condition x = 11 m | [B-358]/[B-471] |
| Coarse-to-fine search | Less relevant: we fit to data (least squares / Bayesian) instead of searching | [B-471] |

---

## 5. A first look at the 2026 test case [ours, preliminary scratch calculation]

Data: $P_0=(0,0,0.11)$ at t = 0, $P_1=(1.50,0.45,0.44)$ at 0.05 s, $P_2=(2.96,0.86,0.74)$ at 0.10 s.

- **Finite differences:** $\bar v(0.025)=(30.0, 9.0, 6.6)$, $\bar v(0.075)=(29.2, 8.2, 6.0)$ m/s, so |v| ≈ 31.5 m/s.
  The launch is ≈ 12° up and ≈ 17° to the side (+y).
- **Mean acceleration:** $\bar a=(-16,-16,-12)$ m/s². With 0.01 m rounding of the given positions,
  $\sigma_a\approx2.6$ m/s² per component (rounding only; real tracking noise would be larger).
  > **Correction (Stage 1):** with the adopted σ = 1 cm noise, $\sigma_a\approx9$ m/s² per component, so the lateral
  > signal below is only ≈ 1.8σ and gravity alone is not rejected (χ²/dof = 6.5/3). Spin is physically plausible but
  > *not* demonstrated by the data alone. See `docs/stages/stage1-gravity-baseline.md`.
- **Decomposition:** subtract gravity $(0,0,-9.81)$ and project onto $\hat v$ and the perpendicular plane:
  - Component along $-\hat v$ → drag → $C_D\approx0.35$ (taking m = 0.43 kg, R = 0.11 m, ρ = 1.2 kg/m³). The noise is
    large: the difference between $C_D$ = 0.22 and 0.35 is only ≈ 17 mm in the second difference of position.
    *Literature check:* this is high for a non-spinning ball (prior ≈ 0.22 ± 0.04) but consistent with **spin-enhanced drag**
    at our Re ($C_D\approx0.25+0.74S$ ≈ 0.32 at S ≈ 0.1 [lit: Kray 2014]). Asai 2007's weaker spin dependence
    (0.15 + 0.45 S) differs; Kray attributes such differences to ball design and support interference, so we treat it as model uncertainty, not a contradiction to resolve.
  - Perpendicular component ≈ 11 m/s², mostly toward −y → **a strong sideways Magnus force**, $C_L\approx0.2$.
    *Literature check (corrected):* at our Re the measured $C_L(S)$ curve gives **S ≈ 0.09 (0.06–0.12), i.e. ω ≈ 26–40 rad/s
    (4–6 rev/s)** [lit: Kray 2014]. My first estimate of S ≈ 0.2–0.3 assumed too low a $C_L$ slope. The spin axis is mostly along −z.
    The ball is heading toward +y and curling back toward the centre.
  - *Sensitivity check (scratch fit with gravity + drag + a constant-coefficient lift force, $C_D$ held fixed):* for $C_D$ from 0.15 to
    0.35 the fitted lift stays at $C_L\approx0.21$ and the entry point stays at **y ≈ 2.645 m**. Only z changes, from 2.01 to 1.97 m. The fitted
    launch velocity absorbs the drag difference, so **the predicted entry point is insensitive to $C_D$**. The spin and lift
    model dominates the prediction.
- **Why model choice matters:**
  - Gravity only (v₀ fitted): entry at **y ≈ 3.22 m, z ≈ 1.96 m**, close to the post (the ball edge reaches the post at y = 3.55 m).
  - Constant-acceleration extrapolation: entry at **y ≈ 2.49 m, z ≈ 1.92 m**.
  - **The 0.7 m spread is larger than the goalkeeper's hand. Physics choices change the answer at a decision-relevant level.**

**Key structural insight [ours].** Three positions with $P_0$ treated as exact fix $\vec r_0$, $\vec v_0$ and one
*mean* acceleration vector, which is 3 numbers. A physically structured model has exactly three unknown
aerodynamic quantities at the leading order: $C_D$ (along $\hat v$) and the two components of the Magnus force
perpendicular to $\hat v$. Spin along $\hat v$ ("rifle spin") produces no force and is unobservable, but it is also
irrelevant. So the problem is **just determined**: the data fixes the aerodynamics, *but with large noise*. Priors on
$C_D$ and $C_L(S)$ from wind-tunnel literature are what turn this into a well-posed estimate with honest
uncertainty. That is the natural place for a Bayesian treatment.

*(These numbers come from a scratch calculation. They will be recomputed properly and under version control in
Stage 1–2. They are not results yet.)*

---

## 6. Limitations shared by all 2022 reports [ours]
1. Magnus magnitude: inviscid $C_L=\tfrac{16}{3}S$ in place of measured $C_L(S)$.
2. No validation against measured trajectories.
3. No error or uncertainty propagation (except B-471's one-at-a-time sensitivity).
4. No foot–ball contact model, so the meaning of "t = 0" is never questioned.
5. No consideration of the ball's surface or panel design (modern balls differ: Jabulani, Brazuca, etc.).
6. Weak numerical verification (the code bugs above).

## 7. Ideas that go beyond the 2022 reports [ours]
Ranked by expected value for the 2026 problem. Each still needs a relevance check before we build it.
1. **Bayesian inverse problem.** Posterior over (v₀, C_D, ω⊥) given the noisy positions and literature priors,
   pushed forward to an entry-point distribution on the goal plane. "Most likely point" = the posterior mode
   (MAP) of the entry-point density, plus a 68 %/95 % credible region. *This directly answers the question.*
2. **Identifiability analysis.** Which parameters can 3 points constrain? A Fisher-information / covariance study
   versus the sampling interval and the noise level. When does adding drag or spin stop changing the prediction?
3. **Model-hierarchy comparison.** The predicted entry point and its uncertainty under each stage (vacuum → drag →
   drag + Magnus → + C_D(Re), C_L(S) → + spin decay). It answers "does complexity help?" quantitatively. This makes the
   staged development part of the science, as CLAUDE.md asks.
4. **Drag crisis near 30 m/s.** Show how $C_D(Re)$ uncertainty (ball type) feeds into the entry-point error.
5. **The meaning of t = 0.** Foot contact lasts 8.8–12.0 ms (means 9.6–10.7 ms) and the ball deforms by 29–65 mm
   [lit: Ishii et al. 2012, verified]. *Note:* the test-case interval lengths (1.600 m, then 1.546 m) match drag alone, which rules out
   a ≈ 5 ms contact lag [ours, see `literature/kick-keeper.md`]. So t = 0 behaves as an effective free-flight origin. If the ball is still accelerating
   at t ≈ 0, treating $P_0$ as a free-flight point biases the fit. Test this by fitting only $P_1$ and $P_2$ with free
   $\vec r_0$ against fitting with $P_0$ fixed.
6. **Goalkeeper information budget.** At t = 0.10 s about 0.27–0.30 s of flight remain, comparable to a keeper's
   reaction and movement time. How fast does the posterior uncertainty shrink with each new observation, and when is
   the prediction "good enough" to act on? This links the prediction quality to save probability and reuses the
   2022 keeper reach ideas in a more principled way.
7. **Effect of the ball radius.** The ball "enters" the goal when its centre crosses x = 11 m inside the frame
   minus R, or with the full ball across the line (Law 10). Define this explicitly; it moves the effective goal edges by 0.11 m.
8. **Elasticity / ball deformation.** Literature suggests the ball recovers its shape within milliseconds after
   contact. Probably irrelevant for the flight; keep it as a justified neglect unless point 5 shows otherwise.
