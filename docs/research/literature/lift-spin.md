# Literature cluster B: lift, Magnus effect, spin, erratic flight

Scope: UPC 2026 Problem B, a penalty kick at v ≈ 31.5 m/s (Re = vD/ν ≈ 4.6×10^5 for D = 0.22 m and ν = 1.5×10^-5 m²/s). The preliminary analysis infers a lateral acceleration a⊥ ≈ 11 m/s². With m = 0.43 kg, R = 0.11 m and ρ = 1.2 kg/m³ that gives C_L ≈ 0.2 (check: 0.2 × ½ρv²πR²/m = 10.5 m/s²).

Conventions: S = Rω/v (Kray uses the same definition and calls it SP). C_L = F_L / (½ρv²πR²). "(fig.)" marks values I digitised from a plot. Unless stated otherwise their precision is about ±0.01 in the coefficient and ±0.005 in S.

---

## 1. Cluster summary

- **The only systematic soccer-ball C_L(S) data in this set is Kray et al. 2014.** It is a wind-tunnel test on a 14-panel Teamgeist-type model, and it includes Re = 4.62×10^5, which matches our case exactly. At this Re the boundary layer is supercritical, the Magnus force is **positive** (no inverse Magnus), and C_L(S) is **strongly concave**: it rises steeply at small S, levels off near C_L ≈ 0.28–0.30, and reaches C_L ≈ 0.2 at **S ≈ 0.09** (fig.). The Re = 3.42×10^5 curve reaches C_L = 0.2 at S ≈ 0.14. So C_L(S) still depends on Re inside the supercritical range [Kray 2014, Fig. 9].
- **Drag rises with spin**: at Re = 4.62×10^5, C_D goes from 0.25 (S = 0) to 0.34 (S = 0.1) and 0.40 (S = 0.23) (fig.). A spinning penalty ball should therefore use C_D ≈ 0.33–0.38, not the non-spinning 0.25 [Kray 2014, Fig. 9].
- **Inverse Magnus** occurs only in the critical regime (Re ≈ 2×10^5, v ≈ 14 m/s), with C_L down to −0.09 at S ≈ 0.12 [Kray 2014, Fig. 7]. It is not relevant at 31.5 m/s.
- **Real-kick trajectory fits** (Bray & Kerwin 2003, v ≈ 23–28 m/s, sidespin free kicks) give C_L = 0.23–0.29 ± 0.05 and C_D = 0.25–0.30 ± 0.03. Spin was not measured. The model used was constant C_D and C_L, no spin decay, RK integration [Bray & Kerwin 2003, Table 1, Eqs. 1–6].
- **Wesson 2002** gives a linear model C_L = C_s·S with C_s ≈ ¼–1 (best guess ½), taken from non-soccer spheres. It also gives typical penalty speeds: about 70 mph mean and 80 mph maximum (31–36 m/s), a flight time of about ⅓ s, and about 10 % speed loss to drag [Wesson 2002, pp. 28, 58, 168–169].
- **Knuckle/erratic flight** matters only at spin below about 2 rev/s (S ≈ 0.05 at 30 m/s; see the coordinator check in §12). In that regime quasi-steady seam-induced side-force coefficients of about ±0.1 appear [Barber et al. 2009, Fig. 6, p. 1098], with wake-switching fluctuations at about 0.5–1 Hz [Kray 2014, p. 47; Watts & Sawyer 1975, p. 962].
- **Spin decay: no source in this cluster gives a measured decay rate or aerodynamic torque coefficient.** All the trajectory models here assume constant spin. Section 10 gives a bracketing estimate that I flag as my own.
- The *Engineering of Sport* (1996) preview contains **no soccer content** (see §8).

---

## 2. Kray, Franke & Frank 2014: Magnus effect on a rotating soccer ball at high Reynolds numbers

**Citation.** T. Kray, J. Franke, W. Frank, *J. Wind Eng. Ind. Aerodyn.* 124 (2014) 46–53. doi:10.1016/j.jweia.2013.10.010.

**Method.** Open-jet Göttingen wind tunnel (1.02 m × 1.02 m nozzle, 0.5 % turbulence, 4.8 % blockage). The model was split into two halves on a rear L-shaped sting, with a DC motor inside driving the halves up to 540 rpm (9 rev/s). This avoids the shaft-through-equator interference of earlier studies. A six-component balance averaged forces over 40 s, with 3–6 repeat runs, and aerosol smoke was used for flow visualisation. Uncertainties are 95 % coverage after Coleman & Steele [p. 48].

**Ball.** An aluminium 14-panel model with the Teamgeist (2006 WC) panel layout, D = 226 mm. Its grooves are about 1.6 mm deep and about 349 cm long in total, and the panels carry a pyramidal micro-texture (0.1–0.15 mm valleys) [p. 47]. The non-rotating C_D(Re) falls within the range of real balls [p. 48, Fig. 2].

**Sign convention.** The paper calls the Magnus coefficient C_M, with C_M = −C_L only because of the axis orientation in the tunnel. **C_M is a force coefficient, not a torque.** No torque was measured.

**Non-rotating data** [Fig. 2–3, p. 49]
- Subcritical C_D ≈ 0.5. Drag crisis at Re ≈ 1.7–2.3×10^5. Supercritical C_D ≈ 0.24–0.30.
- With S = 0, a non-zero lift and side force appears in the critical range: C_L up to about 0.11 and C_S up to about 0.10 at 1.66 < Re/10^5 < 2.34. In the supercritical range C_L stays non-zero because of the arbitrary seam orientation, and C_L jumps at Re ≈ 3.7–4.2×10^5 [p. 50].
- Supercritical separation angle θ ≈ 108 ± 2° at Re = 3.45×10^5 [p. 50].
- Other balls in the literature reach lateral force coefficients of 0.12 (Ito et al. 2012, 14- and 8-panel balls) and 0.14 (Rogers et al. 2010), depending on orientation [p. 50]. These are second-hand citations.

**Rotating data. C_L vs S** (C_M in the paper):

| Re | S → C_L | Source |
|---|---|---|
| 0.96×10^5 (subcritical) | 0 → 0; 0.25 → 0.16; 0.51 → ≈0 (minimum C_D = 0.33); 1.12 → 0.34 (C_D = 0.49) | text p. 50–51, Fig. 5 |
| 2.06×10^5 (critical) | 0 → 0.02; 0.06 → −0.08; **0.12 → −0.09 (inverse Magnus)**; 0.18 → −0.03; ≈0.22 → 0; 0.30 → 0.11; 0.35 → 0.16; 0.41 → 0.19; 0.47 → 0.21; 0.52 → 0.24 | text p. 51 + Fig. 7 (fig.) |
| 3.42×10^5 (supercritical) | 0 → −0.04 (±0.08); 0.036 → 0.00; 0.072 → 0.065; 0.107 → 0.15; 0.143 → 0.20; 0.18 → 0.23; 0.215 → 0.235; 0.248 → 0.27; 0.281 → 0.285; 0.314 → 0.297 (±0.015) | Fig. 9 (fig.) |
| **4.62×10^5 (supercritical, our case)** | 0 → −0.045; 0.026 → 0.11; 0.052 → 0.15; 0.079 → 0.185; 0.107 → 0.22; 0.13 → 0.24; 0.155 → 0.255; 0.18 → 0.27; 0.205 → 0.275; 0.23 → 0.285 (maximum S limited by motor power) | Fig. 9 (fig.) |

**C_D vs S** [Fig. 9 (fig.)]
- Re 4.62×10^5: 0.253 (S = 0), 0.275 (0.05), 0.31 (0.08), 0.34 (0.107), 0.362 (0.13), 0.376 (0.155), 0.384 (0.18), 0.39 (0.205), 0.40 (0.23). A linear fit gives C_D ≈ 0.248 + 0.74 S.
- Re 3.42×10^5: about 0.30 up to S = 0.07, then 0.32 (0.107), 0.35 (0.143), 0.376 (0.18), 0.40 (0.215), 0.42 (0.25), 0.443 (0.28–0.31). A linear fit gives C_D ≈ 0.265 + 0.60 S.
- At Re 2.06×10^5, C_D first *drops* with spin, to a minimum of 0.27 at S = 0.24, and then rises [p. 51, Fig. 7].

**Side force with spin.** In the supercritical range C_S ≈ 0–0.02 for all S [Fig. 9]. In the critical range C_S reaches −0.09 at S = 0.06 [p. 51].

**Leveling off.** The authors report that C_M levels off at 0.30–0.35 at high S [p. 52]. The two supercritical curves differ most at 0.025 < S < 0.15 [p. 52].

**Validity.** 0.96×10^5 < Re < 4.62×10^5 and S ≤ 1.12 (≤ 0.23 at the highest Re). The spin axis is perpendicular to the flow. Only time-averaged forces were measured, with no unsteady or knuckle forces. The authors recommend using the data only for spin rates **above 2 Hz** [p. 52]. They also note that Passmore et al. (2011) found superposed RMS lateral fluctuations to have a negligible trajectory effect [p. 52, second-hand]. There is no spin-decay or torque data.

**Relevance.** **This is the primary source for our C_L(S) and C_D(S).** The Re = 4.62×10^5 curve corresponds to v ≈ 31 m/s for a D = 0.22 m ball, which is our launch speed. The ball decelerates to about 28 m/s by the goal (Re ≈ 4.1×10^5), so it stays between the two supercritical curves. A caveat: this is one ball design (Teamgeist-like), with one arbitrary seam orientation and one spin axis.

---

## 3. Bray & Kerwin 2003: Modelling the flight of a soccer ball in a direct free kick

**Citation.** K. Bray, D. G. Kerwin, *J. Sports Sci.* 21 (2003) 75–85. doi:10.1080/0264041031000070994. (Scanned PDF; read as images.)

**Method.** One skilled left-footed player took 10 sidespin free kicks (simulated 18.3 m free kick) in an indoor sports hall, in still air. The kicks were filmed by 2 synchronised 50 Hz cameras with 1/1000 s shutters, and reconstructed by 12-parameter DLT in a calibrated 20 × 3 × 3.145 m volume. Reconstruction RMS was 0.008 m, and RMS on known points was 0.021/0.015/0.007 m in x/y/z [pp. 79–80]. Positions were fitted with 4th-order polynomials (Levenberg–Marquardt) and differentiated to get v at t = 0.1 s. γ, C_D and C_L were then iterated until the RMS misfit between the RK-integrated model and the data was minimal. The mean misfit was ε = 0.052 m over the 0.1–0.9 s window [p. 80]. Parameter errors came from a Monte-Carlo approach: coordinates were perturbed by rnd(1.96·s), with s_x = 0.017 m, s_y = 0.008 m and s_z = 0.010 m, over 50 replications. This gave γ ± 4°, C_D ± 0.03 and C_L ± 0.05 [pp. 80–81].

**Model** [p. 77–78, Eqs. 1–6]. The equation of motion is r̈ = g − k_d v² τ̂ + k_l v² (σ̂ × τ̂), with k_d = ρAC_d/2m and k_l = ρAC_l/2m. The spin axis σ̂ lies in the (x, z) plane at a fixed tilt γ from the horizontal, with **constant direction and no decay in spin rate** (an explicit assumption, p. 76). C_d and C_l are taken as constant, which the authors justify by post-critical Re throughout the flight [p. 78]. Integration is Runge–Kutta.

**Data** [Table 1, p. 80]. v_i is the speed at t = 0.1 s and v_f the speed at 0.9 s.

| v_i (m/s) | v_f | γ (°) ±4 | C_d ±0.03 | C_l ±0.05 |
|---|---|---|---|---|
| 23.0 | 17.9 | 71 | 0.27 | 0.29 |
| 26.3 | 19.8 | 95 | 0.29 | 0.29 |
| 26.8 | 20.1 | 96 | 0.30 | 0.28 |
| 24.8 | 19.6 | 83 | 0.25 | 0.23 |
| 24.2 | 19.1 | 71 | 0.28 | 0.27 |
| 25.7 | 18.4 | 66 | 0.28 | 0.25 |
| 25.1 | 19.4 | 77 | 0.27 | 0.29 |
| 24.9 | 18.6 | 61 | 0.28 | 0.23 |
| 24.4 | 19.1 | 83 | 0.28 | 0.24 |
| 28.3 | 20.4 | 80 | 0.27 | 0.26 |

The mean of the 10 kicks is C_l = 0.263 (s.d. 0.026) and C_d = 0.277. The representative values used are C_d = 0.28 and C_l = 0.26 [p. 81]. The lowest speed, 17.9 m/s, corresponds to Re = 2.5×10^5, which the authors treat as post-critical [p. 81]. **Spin rate was not measured** [pp. 81, 84]. The authors note that their C_d values exceed the commonly quoted 0.2 [p. 81].

**Simulations** [pp. 81–83, Figs. 6–7]. A free kick at 25 m/s from 18.3 m, with 16.5° elevation and pure sidespin, curves about 1–1.5 m laterally over 18 m (fig.). Changes of +1° in elevation, +1 m/s in speed, or −7° in spin-axis tilt each change the outcome as much as passing over or under the bar. The flight time from wall to goal is about 0.45 s.

**Validity.** v ≈ 18–28 m/s, Re ≈ 2.5–4.6×10^5, sidespin with γ = 61–96°, a single player, a 2002-era ball, and a 0.8 s flight.

**Relevance.** This is real-kick evidence that C_L ≈ 0.23–0.29 is typical for deliberately curled kicks at 23–28 m/s. Our C_L ≈ 0.2 sits at the low end of that range, as expected for a penalty that is not deliberately curled. The fitting method (polynomial fit, then ODE parameter fit by minimum RMS, then Monte-Carlo errors) is a direct template for our uncertainty analysis. Note that their 50 Hz sampling interval is 0.02 s and their fit window is 0.8 s, while we have 3 points over 0.1 s. Their ±0.05 in C_L came from about 40 points, so our uncertainty will be far larger.

---

## 4. Barber, Chin & Carré 2009: Sports ball aerodynamics: a numerical study of the erratic motion of soccer balls

**Citation.** S. Barber, S. B. Chin, M. J. Carré, *Computers & Fluids* 38 (2009) 1091–1100. doi:10.1016/j.compfluid.2008.11.001.

**Method.** FLUENT 6.2 steady RANS with realizable k-ε, enhanced wall treatment (y+ ≈ 1, first cell 0.01 mm) and hybrid meshes of about 9 M cells. Seven laser-scanned balls were modelled (32-panel stitched, 32-panel thermally bonded, 14-panel, and 20- and 26-panel variants). The flow was assumed fully turbulent (no transition modelling). The balls were non-spinning and rotated in 10° steps of orientation, mostly at Re = 1.0×10^6 (the viscosity was altered) [pp. 1092–1095].

**Key data**
- Laminar–turbulent transition for soccer balls occurs at Re ≈ 2–3×10^5 (v ≈ 11–20 m/s) [p. 1092, citing Barber et al.]. The **low-spin knuckle free kick is typically launched at 30–35 m/s** and slows to about 21 m/s by the end of its flight [p. 1092].
- C_D did not depend on orientation and did not differ much between balls. CFD under-predicts C_D by up to 25 % for the real ball. Skin-friction drag is 0.020–0.035 [pp. 1095, 1099].
- **The side-force coefficient C_S varies with orientation between about −0.11 and +0.10** (Ball 1, 32-panel stitched). The 14-panel Ball 3 varies between about −0.04 and +0.10 [Fig. 6, p. 1096 (fig.)]. The variation is "stepped", with jumps of about 0.15 within 10° (Ball 1 at 50–60°) as separation hops between seams [p. 1097]. CFD error on C_L and C_S is ±0.01 (mesh), ±0.02 (repeat scans) and ±0.02 (±2° alignment) [p. 1098].
- In the trajectory simulation of a 2006 Premiership-like kick (33 m from goal, 36 m/s, **¼ rev/s sidespin**), the 3 balls finish about 1 m apart laterally at the goal [Fig. 12 (fig.), p. 1098].
- **Threshold.** Pseudo-static seam forces dominate until the Magnus coefficient exceeds them. This happens at **S ≈ 0.1, ω ≈ 2 rev/s at 30 m/s**, according to Carré's C_M–S graph [p. 1098]. Erratic trajectories were found for spin below 2 rev/s [p. 1099].

**Validity.** No spin, steady RANS without unsteady shedding, and Re mainly 1×10^6 (above the real penalty Re). The results are qualitative and comparative.

**Relevance.** Even with no spin, the asymmetric seams can give a quasi-steady lateral force coefficient of about 0.05–0.1. That is **comparable to half our inferred C_L**, so the seam contribution is a systematic uncertainty on any spin we infer from C_L. Our three positions span only 0.1 s, so any slowly varying seam force in that window looks constant and cannot be told apart from Magnus lift. At ≥ 4 rev/s it should be averaged out (see claim 4).

---

## 5. Barber, Haake & Carré 2007: Using CFD to understand the effects of seam geometry on soccer ball aerodynamics

**Citation.** S. Barber, S. Haake, M. Carré, in *The Engineering of Sport 6*, Vol. 1, Springer (2006/2007), ch. 23, pp. 127–132. doi:10.1007/978-0-387-46051-2_23.

**Method.** A wind tunnel (ITF; 354 × 304 mm slotted test section, 0.3 % turbulence) tested a smooth sphere and a ⅓-scale model ball (Ball A). FLUENT 6.2 RANS was run with several turbulence models. Ball A was modified into B (2× seam width) and C (½ width, ½ depth), and a real ball (Ball D) was laser-scanned [pp. 128–131].

**Data** [pp. 128–131]
- Seams trip transition at lower Re and give a higher supercritical C_D than a smooth sphere, with no further C_D rise above critical.
- Standard k-ε was chosen. It over-predicts C_D by about 25 % because of over-predicted stagnation pressure. The other models were off by −50 % to +400 %.
- Real separation on Ball A is at about 110°.
- Seam *width* and sharpness matter more than depth. Ball D (narrow, shallow seams) has a markedly lower C_D.
- **A typical free kick starts at about 30 m/s and stays turbulent until it slows to about 8 m/s** [p. 129].
- There is **no spin, no lift data and no decay**.

**Relevance.** Low. It supports the claim that our ball stays supercritical throughout the flight, and that C_D (and hence C_L(S)) is ball-specific through the seam geometry. That ball-specificity is a reason for a ±0.03–0.05 prior width on the coefficients.

---

## 6. Watts & Sawyer 1975: Aerodynamics of a knuckleball

**Citation.** R. G. Watts, E. Sawyer, *Am. J. Phys.* 43 (1975) 960–963. doi:10.1119/1.10020. (Scanned PDF; read as images.)

**Method.** A standard **baseball** (2.88 in = 73 mm diameter) was mounted on a strain-gauge beam balance in a subsonic wind tunnel and rotated by hand about the vertical axis in steps of θ. The lateral force was recorded on a strip chart at 68 ft/s (20.7 m/s, Re ≈ 1×10^5) and at other speeds [pp. 960–961].

**Data** [Figs. 3–5, pp. 961–962]
- At fixed orientation the lateral force varies between about −0.1 lb and +0.1 lb (±0.45 N) depending on θ. Near θ = 140° and 220° there are almost discontinuous jumps from about +0.08 to −0.08 lb.
- At θ ≈ 52° and 310°, where a stitch sits at the separation point (about 105–115° from the stagnation point), the lateral force **alternates left–right with amplitude about 0.18 lb (0.8 N) at 0.5–1 Hz**.
- Wind-tunnel noise appeared at ≥ 10 Hz.
- **My own conversion, not given in the paper:** q·A ≈ 1.1 N at 20.7 m/s, so the ±0.1 lb steady lateral force corresponds to C_S ≈ ±0.4 and the fluctuation to about 0.7. These are much larger than for soccer balls, because the baseball's raised stitches are a strong, isolated roughness.
- Both the lateral-force range and the fluctuation magnitude grow roughly as v², over 40–70 ft/s (Fig. 4–5). The fluctuation frequency is roughly independent of speed.
- **Trajectory model.** The authors use small-deflection lateral dynamics, F = m ẍ. A periodic force F₀ sin ωt gives a displacement amplitude F₀/(mω²), so only forcing below about 0.2 Hz gives a deflection of 1 ft or more [Eq. 2]. A constant force gives X = ½(F₀/m)(D/V)², which is independent of speed if F ∝ v² [Eq. 5]. A constant lateral force perpendicular to v gives a path of constant curvature, κ = F₀/(mv²) [Eq. 6].
- A ball that turns through ¼ revolution on its way to the plate curves about 1 ft, while one that turns ½ revolution curves almost not at all [Fig. 6]. An effective knuckleball should rotate much less than once on its flight [abstract].

**Validity.** Baseball only, Re ≈ 0.5–1×10^5 (subcritical for the baseball), quasi-static orientations, no spin measurement.

**Relevance.** Qualitative only. It shows the two knuckle mechanisms: quasi-steady orientation-dependent force, and separation-point switching at 0.5–1 Hz. The Eq. 2 filtering argument applies to us directly. If the ball spins at f_spin, seam forces oscillate at about f_spin times the panel-pattern multiplicity, and their displacement contribution scales as 1/f². At 5–10 rev/s this is negligible.

---

## 7. Wesson 2002: The Science of Soccer (IOP, 189 pp.)

**Citation.** J. Wesson, *The Science of Soccer*, IOP Publishing, Bristol 2002. ISBN 0 7503 0813 3. Read: ch. 2 *The kick* (pp. 17–29), ch. 4 *The ball in flight* (pp. 43–68), ch. 5 *Penalties* (pp. 79–80) and ch. 10 §§4.1–4.6 (pp. 161–176). Page numbers are the printed ones.

**Method.** A popular-science book with an analytical appendix. The drag curve is based partly on the author's own measurements; the Magnus coefficient comes from other spheres.

**Numbers**
- **Penalty speeds.** At the England–Germany Euro 96 shoot-out, 12 penalties averaged **about 70 mph (31 m/s)**, and the fastest (Möller) was **about 80 mph (36 m/s)** [p. 28]. Penalty-takers reach up to 80 mph and the flight time is about ⅓ s [p. 58]. **Drag reduces the speed by about 10 % during a penalty** [p. 58]. A 10 mph side wind shifts a penalty by "a few inches" [p. 63].
- **Kick timing.** Foot swing takes about 0.1 s and impact about 0.01 s [p. 18].
- **Spin from a kick.** If 1 % of the energy of a 50 mph (22 m/s) kick goes into spin, the ball spins at 4 rev/s [p. 25]. With a hollow sphere (I = ⅔ma²), the spin energy fraction is E_R/E_K = 0.32 (f/V)² [p. 170]. Equivalently E_R/E_K = ⅔ S².
- **The crossbar can impart about 10 rev/s** to a ball hitting it at 30 mph [ch. 1].
- **Magnus model** [pp. 167–169]. C_L = C_s·(ωa/V), "provided ωa/V is not too large". Then F_L = ½C_sρAaωV = 2.6×10^-3 C_s ω V (N), and the radius of curvature is R_c = 26V/(C_s f) m. The lateral deviation is D = C_s L² f/(52V), or D/L = C_s n/52 for n revolutions in flight. The author states there is no direct measurement of C_s for footballs; other spheres give **C_s ≈ ¼ to 1**, and he takes C_s = ½.
- **Drag model** [pp. 163–165]. Wesson uses C_D = 0.2 (low, compared with the 0.25–0.30 above), α = ½C_DρA/m = 0.011 m⁻¹, and A = 0.039 m².
- **Kick mechanics** [pp. 173–175]. An oblique impact gives u = ⅔ωa (sideways velocity), with ω = (3/5)v_f θ/a and V = (1 + e)v_f.
- **Inverse Magnus** is described qualitatively: when only the upstream-moving side exceeds the critical speed, the force reverses. Beach balls show irregular sideways motion, while seams make a good football steadier [pp. 67–68].
- There is no spin-decay data.

**Relevance.** This is the best source here for **penalty speed priors** (31–36 m/s) and the ⅓ s flight time. It gives one more independent check on the inviscid 16/3 factor (claim 1): Wesson's C_s ≈ ½ is 10× smaller than 16/3. Even C_s = 1 is 5× smaller.

---

## 8. Haake (ed.) 1996: The Engineering of Sport (preview)

**Citation.** S. Haake (ed.), *The Engineering of Sport*, Proc. 1st Int. Conf., Sheffield, 2–4 July 1996, Balkema / Taylor & Francis. The preview is 36 pages (TOC, preface and the first aerodynamics papers).

**Content check.** The table of contents and the previewed pages have **no soccer or football ball-aerodynamics content**. The aerodynamics section covers general sports CFD (Hanna), cricket-ball swing by CFD (Penrose, Hose & Trowbridge) and cyclist drag (Zdravkovich et al.). The only soccer-related item, "The mechanical analysis of kicking during physical effort" (Waśkiewicz, p. 147), is biomechanics and is not in the preview. Only the cricket-swing paper bears on our topic, and only weakly (seam-induced asymmetric separation). **Not used.**

---

## 9. Consolidated table: C_L vs S (and Re)

| Source | Ball / method | Re (×10^5) | v (m/s, D = 0.22) | S | C_L | C_D | Notes |
|---|---|---|---|---|---|---|---|
| Kray 2014 Fig. 9 (fig.) | 14-panel model, wind tunnel | 4.62 | ≈31 | 0.026 / 0.052 / 0.079 / 0.107 / 0.13 / 0.155 / 0.18 / 0.205 / 0.23 | 0.11 / 0.15 / 0.185 / 0.22 / 0.24 / 0.255 / 0.27 / 0.275 / 0.285 | 0.25 → 0.40 | **matches our Re** |
| Kray 2014 Fig. 9 (fig.) | same | 3.42 | ≈23 | 0.036 / 0.072 / 0.107 / 0.143 / 0.18 / 0.215 / 0.248 / 0.281 / 0.314 | 0.00 / 0.065 / 0.15 / 0.20 / 0.23 / 0.235 / 0.27 / 0.285 / 0.297 | 0.30 → 0.44 | error bars ±0.01–0.03 |
| Kray 2014 Fig. 7, text | same | 2.06 (critical) | ≈14 | 0.06 / 0.12 / 0.22 / 0.30 / 0.41 / 0.52 | −0.08 / **−0.09** / 0 / 0.11 / 0.19 / 0.24 | 0.27 (minimum) → 0.41 | inverse Magnus |
| Kray 2014 Fig. 5, text | same | 0.96 (subcritical) | ≈6.5 | 0.25 / 0.51 / 1.12 | 0.16 / ≈0 / 0.34 | ≈0.5 / 0.33 / 0.49 | |
| Kray 2014 p. 52 | same | 0.96–4.62 | | high S | plateau 0.30–0.35 | | |
| Bray & Kerwin 2003 Table 1 | real kicks, video + ODE fit | ≈2.5–4.6 | 18–28 | not measured | 0.23–0.29 (mean 0.26) ± 0.05 | 0.25–0.30 ± 0.03 | sidespin free kicks |
| Wesson 2002 p. 169 | other spheres (no soccer data) | — | — | small S | C_s·S, C_s = ¼–1 (½ suggested) | 0.2 used | linear model |
| Barber 2009 Fig. 6 (fig.) | CFD, non-spinning, orientation scan | 10 | — | 0 | lateral C_S from −0.11 to +0.10 | — | seam-induced, quasi-steady |
| Kray 2014 Fig. 3 | 14-panel, S = 0 | 1.7–2.3 | — | 0 | lateral up to 0.10–0.11 | — | critical-Re asymmetry |
| Watts & Sawyer 1975 Fig. 3 | baseball, S = 0 | ≈1 | — | 0 | ±0.4 (my conversion) | — | stitched baseball, not transferable |
| *Inviscid formula (for comparison)* | potential flow + Kutta-type circulation | — | — | S | (16/3) S = 5.33 S | — | 1.07 at S = 0.2 |

---

## 10. Spin decay data

- **No source in this cluster gives a measured ω(t), a spin-decay rate or an aerodynamic torque coefficient.** Kray measured forces only, Barber's runs were non-spinning, and Bray & Kerwin and Watts & Sawyer did not measure spin. Bray & Kerwin explicitly assume a constant spin rate and axis [p. 76], and Barber et al. assume constant ¼ rev/s [p. 1098]. Wesson gives only the moment of inertia, I = ⅔ma² [p. 173].
- **Bracketing estimate (mine, not from these sources).** Write the aerodynamic spin-down torque as T = C_τ·½ρv²πR²·R. With I = ⅔mR² = 3.47×10^-3 kg m² and v = 31.5 m/s, ½ρv²πR²R = 2.49 N m, so dω/dt = 718·C_τ rad/s².
  - C_τ = 0.005 → dω/dt ≈ 3.6 rad/s² → 2.2 % loss over 0.4 s at ω = 65 rad/s (3.6 % at ω = 40 rad/s).
  - C_τ = 0.01 → 4.4 % (7.2 %).
  - C_τ = 0.02 → 8.8 % (14 %).
  - C_τ ≈ 0.005–0.02 is my assumed range for spinning rough spheres at S ≈ 0.1–0.3. It is *not sourced here* and should be checked against a dedicated source (e.g. golf/soccer spin-decay literature in another cluster).
- **Effect on our observables.** Over the 0.1 s observation window the loss is ≤ 1–2 % for any plausible C_τ, so it is negligible for parameter inference. Over the full 0.35–0.4 s flight it is a few percent in ω. Because C_L(S) is concave and flat at S ≥ 0.15, the loss in C_L is smaller still.

---

## 11. Recommended C_L(S) model, spin-decay model and priors

**C_L(S), primary.** A saturating fit to Kray 2014 Fig. 9 at Re = 4.62×10^5 (my least-squares fit to the digitised points, 0.026 ≤ S ≤ 0.23):

  C_L(S) = C_Lmax·(1 − exp(−S/S₀)), with C_Lmax = 0.29 ± 0.01 and S₀ = 0.072 ± 0.006 (RMS residual 0.008).

- Re = 3.42×10^5 curve (S ≥ 0.07): C_Lmax = 0.44 ± 0.09, S₀ = 0.27 ± 0.09 (RMS 0.017). This is nearly linear over its range: C_L ≈ 0.048 + 0.87 S.
- Pooled supercritical fit: C_Lmax = 0.31 ± 0.03, S₀ = 0.11 ± 0.03 (RMS 0.032). **Use the pooled fit as the nominal model and treat the spread between the two Re curves as model uncertainty.** That spread is about ±0.03–0.05 in C_L, or about ±0.03–0.05 in S at fixed C_L.
- Do **not** use the linear Wesson form beyond S ≈ 0.1, and never use 16/3·S.
- Sanity limit: C_L ≤ 0.35 for any S in this regime [Kray 2014, p. 52].

**C_D(S).** At Re ≈ 4.6×10^5, C_D ≈ 0.25 + 0.74 S for S ≤ 0.23 [Kray Fig. 9, my fit]. For Re ≈ 3.4×10^5, C_D ≈ 0.265 + 0.60 S. **Prior: C_D = 0.33 ± 0.05 for S ≈ 0.1.** This is consistent with Bray & Kerwin's 0.25–0.30 ± 0.03 for spinning kicks at slightly lower speed, and with Wesson's "≈10 % speed loss" (a C_D of 0.25–0.35 over 11 m gives 7–10 %).

**Spin decay.** Model ω(t) = ω₀ exp(−t/τ_ω), or dω/dt = −C_τ·(½ρv²πR³)/I. Prior C_τ ∈ [0, 0.02] (uniform, or log-uniform from 0.002), which gives τ_ω ≳ 5 s at 31.5 m/s. In practice ω can be held constant within the fit and the decay included as a ±5 % systematic in the extrapolation to the goal. Keep the spin axis fixed (gyroscopic stability; Bray & Kerwin's assumption).

**Priors for our penalty**
- v₀: 25–36 m/s. Euro 96 mean ≈ 31 m/s, maximum 36 m/s [Wesson p. 28]. Ours is 31.5 m/s.
- Spin of a non-deliberately curled, hard penalty: **f ≈ 2–8 rev/s (S ≈ 0.045–0.18)**. 4 rev/s comes from 1 % spin energy at 22 m/s [Wesson p. 25]. Curled free kicks need about S ≈ 0.1–0.3 to reach C_L ≈ 0.23–0.29 [Bray & Kerwin + Kray].
- **Inferred S given C_L = 0.20 ± 0.03** (inverting the Kray curves): S ≈ 0.09 (0.06–0.12) at Re 4.62×10^5, and S ≈ 0.14 (0.11–0.18) at Re 3.42×10^5. The combined estimate is **S ≈ 0.07–0.18, ω ≈ 20–50 rad/s (3–8 rev/s)**.
- Seam-induced quasi-steady lateral force: add a nuisance lateral C_S ~ N(0, 0.03–0.05) on top of the Magnus term. Its maximum is about 0.1 [Barber Fig. 6; Ito, Rogers via Kray p. 50], and it is reduced by spin averaging at ≥ 3 rev/s.
- Re regime: supercritical throughout (v from 31.5 to about 28 m/s). The inverse-Magnus regime (v ≈ 11–20 m/s) is excluded.

---

## 12. Answers to the four claims

**Claim 1: "F = (8/3)πρR³ ω×v implies C_L = (16/3)S ≈ 5.3 S, which overestimates the measured C_L ≈ 0.2–0.3 at S ≈ 0.2 by 4–5×."**
**Verified, with one nuance.** The algebra is right: (8/3)πρR³ωv / (½ρv²πR²) = (16/3)Rω/v. At S = 0.2 the formula gives C_L = 1.07, while the measured values are 0.235 (Re 3.42×10^5) and 0.275 (Re 4.62×10^5) [Kray Fig. 9]. That is an overestimate of **3.9–4.5×**. At S = 0.3 the overestimate is 5.4×. Wesson's empirical slope (C_s ≈ ¼–1) is also 5–20× below 16/3 [Wesson p. 169].
The nuance: at **very small S (≤ 0.03)** the measured supercritical curve is itself steep. Kray gives C_L = 0.11 at S = 0.026 at Re 4.62×10^5, against 0.14 from 16/3·S [Fig. 9, fig.]. So the overestimate is mostly a consequence of saturation, and its size depends on S: about 1.3× at S = 0.03, 2.6× at S = 0.1 and about 4× at S = 0.2. **Applied to our C_L = 0.2, the inviscid formula would infer S ≈ 0.038 (ω ≈ 11 rad/s). The measured curve gives S ≈ 0.09–0.14, so the inviscid formula underestimates ω by 2.4–3.7×.**

**Claim 2: "Spin decay over a ~0.4 s penalty flight is only a few percent."**
**Not testable from this cluster.** No source here measures spin decay or torque. All trajectory models here (Bray & Kerwin, Barber) assume constant spin. My order-of-magnitude bracket (C_τ = 0.005–0.02) gives a 2–9 % loss over 0.4 s at ω ≈ 65 rad/s, and 4–14 % at ω ≈ 40 rad/s. Because C_L is flat at S ≳ 0.15, the loss in C_L is smaller. So "a few percent" is plausible but **unsourced**. Treat it as a ±5 % systematic and look for a quantitative spin-decay source in another cluster.

**Claim 3: "Our inferred C_L ≈ 0.2 at v ≈ 31.5 m/s is consistent with S ≈ 0.2–0.3 (ω ≈ 10–12 rev/s)."**
**C_L ≈ 0.2 is plausible; S ≈ 0.2–0.3 is probably too high.**
- C_L ≈ 0.2 is fully consistent with real kicks: 0.23–0.29 for curled free kicks [Bray & Kerwin Table 1], and within the supercritical range of 0–0.30 [Kray].
- Using the measured soccer curve at our Re instead (Kray Re 4.62×10^5), C_L = 0.20 corresponds to **S ≈ 0.09 (ω ≈ 26 rad/s, 4.1 rev/s)**. The Re 3.42×10^5 curve gives S ≈ 0.14 (40 rad/s, 6.4 rev/s).
- S = 0.2–0.3 would give C_L ≈ 0.235–0.30, which is 20–50 % above the inferred value.
- There is also an internal inconsistency in the claim: S = 0.2–0.3 at 31.5 m/s means ω = 57–86 rad/s = **9–14 rev/s**, which overlaps "10–12 rev/s". But 60–75 rad/s is 9.5–12 rev/s, so it is the "ω ≈ 60–75 rad/s" in the preliminary analysis that matches.
- 9–14 rev/s would mean about 3–6 % of the kick energy is in spin (E_R/E_K = ⅔S²). That is high for a penalty, though attainable for a deliberate curler.
- **Recommendation: revise to S ≈ 0.07–0.18, ω ≈ 20–50 rad/s (3–8 rev/s)**, and note that a ±0.05 seam side-force contribution makes the low end even lower.

**Claim 4: "Is the knuckle effect (low spin) relevant at 31.5 m/s with significant spin?"**
**No, as long as the spin is ≳ 2–3 rev/s, which C_L ≈ 0.2 implies.**
- The knuckle regime is spin below about 2 rev/s, which the sources pair with S ≲ 0.1 at 30 m/s [Barber 2009, pp. 1098–1099; Kray 2014, p. 47]. *[Coordinator check: 2 rev/s at 30 m/s is S = 2π·2·0.11/30 ≈ 0.046, not 0.1. The sources' pairing of "2 Hz" with "S ≈ 0.1" is internally inconsistent; the S ≈ 0.1 seems to be where Magnus exceeds the seam forces. Both thresholds are well below our S ≈ 0.09–0.13 at 4–6 rev/s, so the conclusion stands.]* Above that the Magnus force dominates, and the residual supercritical side force with spin is only C_S ≈ 0–0.02 [Kray Fig. 9]. Passmore et al. found RMS fluctuations negligible for trajectories [via Kray p. 52].
- Our inferred S ≈ 0.09–0.14 (4–6 rev/s) sits just above the threshold. Seam-induced quasi-steady lateral coefficients (≤ 0.1, Barber Fig. 6) are then partly averaged out over about 1.5–2.5 revolutions in 0.4 s. Following Watts & Sawyer's Eq. 2, a periodic force at frequency f contributes a displacement amplitude of about F₀/(m(2πf)²): **about 2 mm for C_S = 0.05 at 5 Hz.** Knuckle wake switching (0.5–1 Hz) is far too slow to show up within 0.4 s except as a quasi-constant offset.
- **Residual relevance.** A constant seam-orientation lateral force (C_S of a few × 0.01, up to 0.1 when spin is near zero) cannot be distinguished from Magnus lift using 3 points over 0.1 s. Include it as an additional lateral-coefficient uncertainty of about ±0.03–0.05, roughly ±15–25 % of the inferred C_L.
