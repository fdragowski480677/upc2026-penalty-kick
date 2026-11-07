# Stage 3 design notes: Magnus/lift force, spin-dependent drag, spin decay

These are design decisions and the physics justification, written before the implementation (CLAUDE.md: explain the motivation before
adding a feature). Sources: `docs/research/literature/` (in particular `spin-decay-and-free-flight.md`).

## Force model [theory]
$$\vec a_L = \frac{\rho A}{2m}\,C_L(S, Re)\,|\vec v|^2\,\frac{\vec\omega_\perp\times\vec v}{|\vec\omega_\perp\times\vec v|},\qquad
S = \frac{R|\vec\omega_\perp|}{|\vec v|},\qquad \vec\omega_\perp = \vec\omega - \frac{(\vec\omega\cdot\vec v)}{|\vec v|^2}\vec v .$$
Only the spin component perpendicular to the velocity produces a force; the component along $\vec v$ ("rifle spin") does not.
This matches Hörzer 2010. The spin axis is fixed in space, since gyroscopic stability makes precession negligible over 0.4 s.

**Unknowns (team decision):** v₀ (3) plus the 2 components of ω perpendicular to v₀, i.e. 5 parameters from 6 data, leaving 1 dof.

## Q1: is interpolating C_L between Kray's Re curves physically correct? [ours]
**Not as a physical law.** The evidence:
1. Kray has only two supercritical Re points (3.42 and 4.62×10⁵), and he says the curves differ most for 0.025 < S < 0.15, which is our range.
   The difference comes from the boundary-layer state on the side moving with the flow, a residue of the critical-regime (negative-Magnus) mechanism.
   That is a regime-transition effect, so it is not expected to be linear in Re.
2. Asai 2007 Fig. 9 measures five Re values inside our range (3.3–4.6×10⁵), and at low S its Re trend is **the opposite** of Kray's
   (C_s falls with Re in Asai's data, rises in Kray's). The low-S Re dependence is therefore specific to the ball and the rig.
3. So linear interpolation in Re is an *empirical* choice with no physical justification. A physically defensible statement is weaker:
   **C_L rises with S and saturates at 0.25–0.35** (all sources agree: Kray, Asai 2007, Asai 2020 free flight, Bray & Kerwin).

> **Correction (after implementation, see `stage3-magnus-effect.md`):** the argument below holds only *at fixed lift magnitude*. At σ = 1 cm the
> data do **not** fix the lift magnitude (the profile χ² is flat over 0.5–15 rev/s), and the entry y then ranges from 2.45 to 3.08 m. The curve shape
> matters at the ±2.5 cm level; the spin magnitude dominates.

**Why this matters less than it seems (at fixed lift).** The data already fix the lift during the observed window (0–0.1 s). The C_L(S, Re) curve only sets
**how the lift evolves** as the ball slows from 32 to 28 m/s. At constant ω, S ∝ 1/v, so locally $F_L \propto v^{\,n}$ with
$n = 2 - \partial\ln C_L/\partial\ln S + \partial\ln C_L/\partial\ln Re$. The physical limits are clear:
- saturated C_L (C_L independent of S): $F_L\propto v^2$ (n = 2);
- linear regime (C_L ∝ S): $F_L \propto v$ (n = 1).
Every measured curve lies between these limits at our S.

**Scratch sensitivity test** (5-parameter fit to the test case, C_D = 0.22, σ = 1 cm; to be reproduced in the Stage 3 code):

| C_L model | Inferred spin | S₀ | χ² (dof 1) | Entry y | Entry z |
|---|---|---|---|---|---|
| Kray, Re 4.62×10⁵ curve | 4.5 rev/s | 0.097 | 0.86 | 2.631 | 1.991 |
| Kray, linear interpolation in Re | 4.6 rev/s | 0.098 | 0.86 | 2.659 | 1.987 |
| Asai 2007, Re 4.55×10⁵ curve | 6.8 rev/s | 0.145 | 0.86 | 2.635 | 1.990 |
| Asai 2007, interpolation in Re | 6.8 rev/s | 0.145 | 0.86 | 2.625 | 1.991 |
| limit: C_L ∝ S (F ∝ v) | 4.3 rev/s | 0.093 | 0.86 | 2.621 | 1.992 |
| limit: C_L const (F ∝ v²) | (undetermined) | — | 0.86 | 2.672 | 1.986 |

**Conclusions:**
- **The entry point is robust to the C_L-curve choice:** the full physical envelope (n = 1…2) is y = 2.62–2.67 m (±2.5 cm), below the noise σ.
- **The inferred spin rate is not robust:** 4.3–6.8 rev/s depending on the curve. The spin is a *derived, model-dependent* quantity;
  the lift force is what the data measure.
- Compared with Stage 2 (y = 3.217 m), the lift moves the prediction ≈ 0.59 m toward the centre.

**Design:** nominal C_L = Kray 2014 Re 4.62×10⁵ curve, measured at our Re on the rig with the least support interference. Switches:
Kray Re-interpolation, Asai 2007 curves (fixed and interpolated), and the two physical limits (n = 1, n = 2). All are tested.
Stage 4 treats the spread as model uncertainty.

## Q3: spin-dependent drag (team: "important to consider")
Supported by Asai 2007 (C_D ≈ 0.15 + 0.47 S, independent of Re over 3.3–4.6×10⁵; verified) and Kray 2014 (slope ≈ 0.74 for S ≤ 0.1;
verified), and indirectly by Bray & Kerwin. Hörzer's 0.80 slope is rejected (it is inconsistent with Asai's figure). Form:
$C_D = C_{D0} + k_s S$, with C_D0 from the Stage 2 setting. Switch values: k_s ∈ {0, 0.47 (Asai), 0.74 (Kray)}. **Default: k_s = 0.47 (Asai 2007), team decision.**

## Q4: spin decay
Model $\dot\omega = -k\,\omega\,|\vec v|/R$ (Smits & Smith, via James & Haake 2008), i.e. τ = R/(k v). Presets: none (default) /
golf_like 2×10⁻⁵ / asai2020 1.4×10⁻⁴ (best free-flight evidence: ≈ 1.5 % loss over our flight) / goff_carre 5×10⁻⁴ (second-hand) /
james_subcritical 2×10⁻³ (upper bound). This requires ω in the ODE state, so the state grows from 6 to 9 components.
