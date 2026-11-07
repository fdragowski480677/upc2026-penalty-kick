# Literature cluster A: DRAG (C_D vs Re, drag crisis, roughness and seams)

Scope: UPC 2026 Problem B (penalty kick, v ≈ 31.5 m/s, D = 0.22 m, so Re ≈ 4.3–4.7×10^5 for ν = 1.5–1.6×10^-5 m²/s).
Sources: the 8 PDFs in `references/2022/`. Text was extracted with pypdf; data that exist only in plots were read off page renders.

**Tags used below.** **[text]** means the value is stated in the paper's text or abstract. **[table]** means it comes from a printed table. **[fig, read]** means I read it off a figure by eye. Figure readings are good to about ±0.01–0.02 in C_D and about ±10–15 % in Re on log axes, and about ±5 % on linear axes.

---

## 0. Cluster summary

- **Smooth sphere (Achenbach 1972).** Subcritical C_D ≈ 0.47–0.50. The drag falls sharply at Re ≈ 3–3.7×10^5 to a minimum C_D ≈ 0.07 at Re_crit ≈ 3.7×10^5. It then rises slowly, to about 0.12 at 10^6 and 0.19 at 6×10^6. This is the curve that gives the "C_D ≈ 0.06–0.08 at 30 m/s" numbers. It is very sensitive to free-stream turbulence, supports and surface finish.
- **Rough spheres (Achenbach 1974).** Roughness lowers Re_crit (from 4×10^5 down to 8×10^4), makes the minimum shallower (0.07 rising to 0.20), and raises the post-crisis plateau to C_D ≈ 0.24–0.40. The plateau saturates near 0.38–0.40 for k/d ≳ 2×10^-3.
- **Real footballs** (Asai 2007; Carré 2005; Alam 2010; Oggiano 2010), all wind-tunnel, non-spinning:
  - The crisis lies at Re_crit ≈ 1.2–3.1×10^5, well below the smooth sphere.
  - Subcritical C_D ≈ 0.38–0.53.
  - The post-crisis minimum is ≈ 0.12–0.16.
  - In the 3.5–5.4×10^5 range that matters for us, C_D ≈ 0.15–0.25. The best direct measurement at our speed (Alam 2010, 100–130 km/h) gives **0.22–0.24**.
  - The ball type spreads the value by about ±0.04.
- **Spin.** Asai 2007 (FRP Teamgeist replica, 22–30 m/s) finds C_D rising roughly linearly with the spin parameter Sp, from 0.17 at Sp = 0.05 to 0.29 at Sp = 0.31. Carré 2005 (1/3-scale model, Re ≤ 2.1×10^5) finds essentially no spin dependence (C_D ≈ 0.19–0.21).
- **Bottom line for v ≈ 31.5 m/s.** The ball is firmly supercritical for every football tested. C_D ≈ 0.22 ± 0.04 (non-spinning to moderate spin), with a hard plausible envelope of about 0.13–0.30. The drag crisis plays no role during the 0.1 s observation window: speed falls by only about 1–2 m/s, so Re changes by about 5 %.

---

## 1. Achenbach 1972: smooth sphere, very high Re

**Citation.** Achenbach, E. (1972). Experiments on the flow past spheres at very high Reynolds numbers. *J. Fluid Mech.* 54(3), 565–575.

**Method.**
- Wind tunnel: a free jet at the nozzle exit, so there is no blockage.
- Atmospheric rig up to U = 33 m/s, plus a pressurised tunnel up to 40 bar to reach high Re.
- Turbulence level about 0.45 %.
- Drag measured on a strain-gauge balance inside a polished aluminium sphere (d = 200 mm) on a rear sting (sting diameter 0.1d).
- A second sphere (d = 175 mm) carried skin-friction and pressure probes.
- Mach < 0.1.

**Ball.** Smooth (polished) sphere. Re range 5×10^4 to 6×10^6.

**Numerical data.**

| Re | C_D | Source |
|---|---|---|
| 5×10^4 – 2×10^5 | 0.47–0.50 (nearly constant, subcritical) | [fig, read] Fig. 4 |
| 3×10^5 | ≈ 0.45 → starts the steep drop | [fig, read] Fig. 4 |
| 3.5×10^5 | ≈ 0.2–0.3 (inside the near-vertical drop) | [fig, read] Fig. 4 |
| **3.7×10^5 (Re_crit, C_D minimum)** | **≈ 0.07** (scatter 0.06–0.08) | Re: [text] p. 569; C_D: [fig, read] Fig. 4 |
| 5×10^5 | ≈ 0.08 | [fig, read] Fig. 4 |
| 1×10^6 | ≈ 0.11–0.12 | [fig, read] Fig. 4 |
| 2×10^6 | ≈ 0.15 | [fig, read] Fig. 4 |
| 6×10^6 | 0.19 | [text] p. 570; Fig. 4 |

- **Flow regimes.** Achenbach distinguishes four regimes [text] p. 568–572:
  - subcritical: laminar separation at φ_s ≈ 82° (at Re = 1.62×10^5);
  - critical: a laminar separation bubble with turbulent reattachment;
  - supercritical: up to Re ≈ 1.5×10^6, with transition fixed just behind the equator;
  - transcritical: above Re ≈ 1.5×10^6, where transition moves toward the front stagnation point.
- **Effect of turbulence.** Free-flight (low-turbulence) data from Millikan & Klein put Re_crit about 10 % higher. Wieselsberger's data, disturbed by the support, only fall to 0.15 [text] p. 570. A high-turbulence tunnel (Bacon & Reid) gives a lower and more gradual crisis [text, Fig. 6].
- **Skin friction.** Friction peaks at about 12.5 % of total drag in the critical range [text] p. 574.

**Caveats.** The crisis is extremely sensitive to turbulence level, supports and roughness (the paper stresses this). The probe sphere's slots acted as a boundary-layer trip. No spin, lift or side-force data.

**Relevance.**
- This is the reference smooth-sphere curve. At D = 0.22 m, 30 m/s is Re ≈ 4.4×10^5, which falls right in the smooth sphere's drag bucket (C_D ≈ 0.07–0.08).
- That is where a table showing "0.06 at 30 m/s" comes from. It does not describe a panelled ball (see the footballs below).

---

## 2. Achenbach 1974: surface roughness and tunnel blockage

**Citation.** Achenbach, E. (1974). The effects of surface roughness and tunnel blockage on the flow past spheres. *J. Fluid Mech.* 65(1), 113–125.

**Method.**
- Same pressurised wind tunnel and balance as in 1972; sphere d ≈ 0.2 m on a rear sting.
- Roughness was made by gluing glass beads (k = 2.5, 1, 0.5, 0.3 mm) onto the sphere, or by emery abrasion (≈ 0.05 mm grooves).
- Re range 5×10^4 to 6×10^6.
- Blockage was studied separately: a sphere in a tube with d_s/d_t = 0.5–0.92.

**Ball.** Rough spheres with k/d = 25, 150, 250, 500 and 1250 ×10^-5. The effective roughness is about 0.55k for beads [text] p. 124.

**Numerical data.** From Fig. 2 [fig, read] unless marked.

| k/d (×10^-5) | Re_crit (C_D min) | C_D,min | C_D at Re ≈ 4–5×10^5 | Transcritical plateau |
|---|---|---|---|---|
| 0 (smooth, 1972) | ≈ 3.7×10^5 | ≈ 0.07 | ≈ 0.07–0.08 | → 0.19 (6×10^6) |
| 25 (emery) | ≈ 3.5×10^5 | ≈ 0.07–0.08 | ≈ 0.08–0.10 | ≈ 0.24 |
| 150 | ≈ 2×10^5 | ≈ 0.09 | ≈ 0.27–0.30 | ≈ 0.36–0.37 |
| 250 | ≈ 1.6×10^5 | ≈ 0.10 | ≈ 0.33–0.35 | ≈ 0.38 |
| 500 | ≈ 1.2×10^5 | ≈ 0.14 | ≈ 0.36 | ≈ 0.38–0.39 |
| 1250 | ≈ 8×10^4 | ≈ 0.20 | ≈ 0.38–0.39 | ≈ 0.39 |

- **Subcritical drag.** C_D ≈ 0.50–0.51 for all roughnesses (the curves collapse) [text] p. 115.
- **Re_crit vs k/d** [fig, read] Fig. 3: 1250 → 8.2×10^4; 500 → 1.2×10^5; 250 → 1.45×10^5; 150 → 1.9×10^5; 25 → about 2.8–3×10^5; smooth → 4×10^5.
- **Plateau saturation.** The transcritical C_D rises with k/d and saturates at a maximum of about 0.4 [text] abstract. Fig. 4 [fig, read] at Re = 5×10^6: 0.19 (smooth), 0.24 (k/d = 2.5×10^-4), 0.36 (1.5×10^-3), and 0.38–0.39 for k/d ≥ 2.5×10^-3.
- **Mechanism.** Roughness thickens the turbulent boundary layer, so separation moves upstream and the drag recovers more strongly after the crisis.
- **Strouhal number.** Subcritical St is the same for rough and smooth spheres. No dominant shedding frequency appears beyond Re_crit [text].
- **Blockage.** Subcritical C_D/C_D∞ = 1 + 1.45 (d_s/d_t)^4.6, with C_D∞ = 0.51 at Re = 2×10^5 [text, Fig. 8].
- **Lateral force.** Near the critical Re, lateral forces from asymmetric transition pushed the sphere against the tube wall [text] p. 125. This is qualitative evidence of strong, random side forces near the crisis (a knuckle-type effect).

**Caveats.**
- The roughness is uniform sand-grain-like beads, not seams.
- The effective diameter was taken as d + 0.9k.
- Blockage results apply to pipe flow only and are irrelevant for us.

**Relevance.**
- This paper provides the physics: roughness lowers Re_crit, reduces the depth of the drag bucket, and raises the supercritical drag.
- It also shows how a C_D ≈ 0.35 at Re ≈ 4.5×10^5 could arise physically: only with distributed roughness k/d ≳ 2×10^-3 (k ≳ 0.4 mm over the whole surface). No modern football tested in this cluster behaves like that (see §9).

---

## 3. Mehta 1985: Aerodynamics of sports balls (review)

**Citation.** Mehta, R. D. (1985). Aerodynamics of sports balls. *Annu. Rev. Fluid Mech.* 17, 151–189.

**Method.** Review of wind-tunnel, force-balance, pendulum and trajectory work on cricket balls, baseballs and golf balls. There is **no soccer-ball data**.

**General drag and roughness content** (relevant to us).
- **Magnus mechanism.** Spin delays separation on the retreating side and advances it on the advancing side. A normal Magnus force needs postcritical flow on both sides. A slowly rotating smooth sphere can show a *negative* Magnus force at precritical Re [text] p. 152.
- **Fig. 21** (after Bearman & Harvey 1976; Achenbach 1972, 1974) [fig, read]:
  - Golf ball: drops from 0.5 to about 0.25 at Re ≈ 6×10^4 and stays flat at ≈ 0.25–0.27 up to 2×10^5.
  - Rough spheres: recover to ≈ 0.38–0.40 after their crisis.
  - Smooth sphere: minimum ≈ 0.07 near 4×10^5.
  - Mehta's reading of the figure: dimples trip the boundary layer *without* the thickening penalty of sand-grain roughness, which is why the golf-ball C_D does not climb back up [text] p. 179.
- **Cricket ball** (Sherwin & Sproston, Fig. 7): C_D ≈ 0.45 at seam angle 30° in the 0.3–1.3×10^5 range [text] p. 158. The side-force coefficient from seam-induced asymmetric transition reaches a maximum of about 0.3 [text].
- **Seam/roughness tripping.** A roughness height of the order of the laminar boundary-layer thickness is needed, with a roughness Reynolds number of at least about 900 (Graham 1969) [text] p. 156–157.
- **Golf ball with spin.** C_D increases with spin (induced drag) and C_L with spin parameter V/U (Bearman & Harvey, Figs. 22–24).
- **Concluding statement.** Lateral forces of about 50 % of ball weight (C ≈ 0.3) are typical of swing and curve mechanisms [text] p. 188.

**Caveats.** Pre-dates every soccer-ball study. The golf and cricket Re are lower than ours.

**Relevance.**
- Background for how roughness elements (seams, dimples) set Re_crit and the supercritical C_D.
- Supports reading the football as "between smooth sphere and golf ball".
- Its side-force scale (C_S up to about 0.3) is the order of magnitude to allow for knuckle or seam forces.

---

## 4. Asai, Akatsuka & Haake 1998: The physics of football (Physics World)

**Citation.** Asai, T., Akatsuka, T. & Haake, S. (1998). The physics of football. *Physics World* 11(6), 25–27.

**Method.** Popular-science overview with schematic figures. There are **no new measurements** of C_D.

**Content.**
- Example forces [text] p. 25: a free kick at 25–30 m/s with 8–10 rev/s spin gives a lift (Magnus) force of about 3.5 N, an acceleration of about 8 m/s², and up to about 4 m of deflection over 30 m.
- Fig. 1b is a **schematic** C_D–Re sketch for a dimpled golf ball, a rough sphere and a smooth sphere. The axis label reads "×10^-5" but the values only make sense as ×10^4.
- Football Re_crit is quoted as about 4×10^5, versus about 2×10^4 for the golf ball [text] p. 26.
- Fig. 1d is a schematic of drag force vs speed: it peaks near 20–22 m/s and drops at higher speed. **It is not quantitative.** Back-computing C_D from it gives non-physical values.
- Narrative for the Roberto Carlos free kick: the ball starts supercritical (above 30 m/s), drops into the laminar (high-drag) regime late in flight, and bends more.

**Caveats.**
- Qualitative only.
- The claim "football Re_crit ≈ 4×10^5" is a smooth-sphere-like value. It is **superseded by the same group's measurements** (Asai 2007: 2.2–3.1×10^5) and by all other ball data here.

**Relevance.** None quantitatively. Do not use Fig. 1d or the 4×10^5 Re_crit as a model.

---

## 5. Asai, Seo, Kobayashi & Sakashita 2007: Fundamental aerodynamics of the soccer ball

**Citation.** Asai, T., Seo, K., Kobayashi, O. & Sakashita, R. (2007). Fundamental aerodynamics of the soccer ball. *Sports Engineering* 10, 101–110.

**Method.**
- Wind tunnel at Tokai University: closed return, 1.5 × 1 m test section, maximum 40 m/s, turbulence 1 %, six-component balance.
- Non-spinning tests: real balls on a rear sting, U = 7–35 m/s.
- Spinning tests: a full-size FRP model of the Teamgeist on side piano wires, 22–30 m/s, 2–10 rev/s.
- The set-up was checked against a smooth sphere: C_D ≈ 0.45 (sub) and ≈ 0.1 (super), Re_crit ≈ 3.5×10^5 [text] p. 103.
- Plus TiCl₄ smoke visualisation of balls kicked in real flight.
- Re is computed with D ≈ 0.22 m and ν ≈ 1.45×10^-5 m²/s: their Re = 455 172 corresponds to 30 m/s.

**Balls.** Adidas Fevernova (2002, 32 panels, hand-stitched), Roteiro (2004, 32 panels, thermally bonded) and Teamgeist (2006, 14 panels, thermally bonded). Spinning tests used the FRP Teamgeist replica.

**Numerical data (non-spinning).**

| Quantity | Value | Source |
|---|---|---|
| Re_crit, Fevernova and Roteiro | ≈ 2.2×10^5 | [text] p. 104 |
| Re_crit, Teamgeist | ≈ 3.1×10^5 (abstract says 2.2–3.0×10^5) | [text] p. 101, 104 |
| Subcritical C_D (all three) | ≈ 0.43 (points 0.43–0.47 at 1.1–1.5×10^5) | [text] p. 108; [fig, read] Fig. 4 |
| Supercritical C_D | ≈ 0.15 | [text] p. 108 |
| Drop (50 % point) | Re ≈ 1.7–2.0×10^5 | [fig, read] Fig. 4 |
| C_D minimum | ≈ 0.14 at Re ≈ 2.5–3×10^5 | [fig, read] Fig. 4 |
| C_D at Re ≈ 5×10^5 (≈ 33–35 m/s) | Fevernova ≈ 0.19–0.20 (rising); Roteiro ≈ 0.15; Teamgeist ≈ 0.15 | [fig, read] Fig. 4 |
| Drag force, Roteiro | 0.5 N at 7 m/s → 3.8 N at 35 m/s | [text] p. 104 |
| Speed of the drag crisis (Roteiro) | ~12–15 m/s | [text] p. 104 |

Consistency check: 3.8 N at 35 m/s, with ρ = 1.2 and A = 0.038 m², gives C_D ≈ 0.14. This matches the supercritical value.

**Spin data** (FRP Teamgeist, Re = 3.34–4.55×10^5, i.e. 22–30 m/s).

| Sp | C_D (Fig. 8) [fig, read] | C_S (Fig. 9) [fig, read] |
|---|---|---|
| 0.05 | 0.16–0.18 | 0.03–0.15 (scattered) |
| 0.10 | 0.18–0.22 | 0.17–0.25 |
| 0.15 | 0.21–0.23 | 0.21–0.27 |
| 0.20 | 0.24–0.26 | 0.23–0.29 |
| 0.25 | 0.26–0.28 | 0.24–0.30 |
| 0.30 | 0.28–0.29 | 0.30–0.33 |

- **Speed independence.** C_D is about linear in Sp and roughly independent of Re over this range [text] p. 106. My fit to the figure: C_D ≈ 0.15 + 0.45·Sp. *(Coordinator check: confirmed, slope ≈ 0.47. Hörzer 2010's 0.80 fit to this figure is inconsistent with it.)*
- **Real kicks.** A real high-speed curve kick had C_D ≈ 0.3 [text] p. 106. In flight at 27 m/s, 7 rev/s (Sp ≈ 0.18), C_D and C_S were both estimated at about 0.25 [text] p. 107.
- **Separation angle.** About 90° at 5 m/s and about 120° at 29 m/s (visualisation) [text]. The non-spinning wake showed large-scale undulation, which the authors attribute to a possible knuckle effect [text].

**Caveats.**
- The turbulence level (1 %) is higher than in real air, which may lower Re_crit slightly.
- The sting fixes the ball orientation (one orientation only).
- The spinning data come from an FRP model, not a real ball, and cover a narrow range: 22–30 m/s and ≤ 10 rev/s.

**Relevance. This is the key source.**
- At 31.5 m/s (Re ≈ 4.6×10^5), a non-spinning 2002–2006 ball has C_D ≈ 0.15–0.20.
- With spin, C_D ≈ 0.15 + 0.45·Sp. A penalty with 2–5 rev/s has Sp ≈ 0.04–0.11, giving C_D ≈ 0.17–0.20. A heavily spun kick at 10 rev/s (Sp ≈ 0.22) gives about 0.25.

---

## 6. Carré, Goodwill & Haake 2005: Effect of seams

**Citation.** Carré, M. J., Goodwill, S. R. & Haake, S. J. (2005). Understanding the effect of seams on the aerodynamics of an association football. *Proc. IMechE Part C: J. Mech. Eng. Sci.* 219, 657–666. DOI 10.1243/095440605X31463.

**Method.**
- Wind tunnel with a slotted-wall test section (305 × 355 mm), turbulence 0.3 %, speeds 20–70 m/s.
- Two balls: a 66 mm rapid-prototyped 1/3-scale generic 32-panel model (sanded smooth panels, seams present) and a 140 mm "mini" Adidas Fevernova.
- Rear sting with a tare correction. The tare was large, about half the measured drag.
- Spinning tests used side stings, ±2800 rpm, 20–60 m/s.
- A 66 mm smooth sphere was tested for comparison.
- Plus 3-D trajectory simulations using the fitted coefficients.

**Numerical data.**

| Ball | Re | C_D | Source |
|---|---|---|---|
| Scale model (non-spinning) | 9×10^4 | ≈ 0.45–0.47 | [fig, read] Fig. 3 |
| Scale model | 0.9–1.3×10^5 | drop 0.5 → 0.2 | [text] p. 659 |
| Scale model | 1.4–3.2×10^5 | ≈ 0.21–0.22 (slight rise) | [fig, read] Fig. 3 |
| Mini football | 1.8–3.2×10^5 | ≈ 0.20–0.23 | [fig, read] Fig. 3 |
| Mini football | 3.6–4.0×10^5 | ≈ 0.22–0.24 | [fig, read] Fig. 3 |
| Mini football | 4.5–4.7×10^5 | ≈ 0.23–0.25 | [fig, read] Fig. 3 |
| Simulation input, central kick 26 m/s | 3.9×10^5 | 0.22 | [text] p. 664 |
| Simulation input, curve kick 18.5 m/s | 2.7×10^5 | 0.22 (C_M = 0.32 at Sp = 0.43) | [text] p. 664 |
| Spinning scale model | 1.7 and 2.1×10^5, Sp 0–0.3 | ≈ 0.19–0.21, **no clear Sp dependence** | [fig, read] Fig. 7; [text] p. 662 |
| Spinning scale model | 1.1×10^5 | ≈ 0.27–0.37 (transitional) | [fig, read] Fig. 7 |
| Smooth sphere, rear sting | 7×10^4 – 5×10^5 (equivalent) | 0.53 ± 0.02 (stays **subcritical**) | [text] p. 662 |
| Smooth sphere, spinning | 0.9–2.6×10^5 | 0.54 ± 0.04 | [text] p. 662 |

- **Magnus fit (eq. 3, Table 2)** [table]:
  - C_M = a(1 − e^(−b·Sp)) − c·Sp(1 − e^(−d·Sp))
  - a = 0.35, b = 2.39×10^-5·Re, c = 12150·e^(−8.22×10^-5·Re), d = 1.42×10^-4·Re
  - The pypdf text lost the minus signs. They are restored here from context.
  - Valid only for 9×10^4 < Re < 2.9×10^5 and 0 < Sp < 0.5.
- **Reverse Magnus.** C_M ≈ −0.3 for the football at Re = 9×10^4 and low Sp. The smooth sphere at Re ≥ 1.7×10^5 and Sp ≥ 0.3 gave −0.31 ± 0.02 [text].
- **Launch table** (Table 1, adapted from Asai 2002) [table]: a central strike at 25 m/s foot speed gives 26.0 m/s and about 1.9 rev/s. Strikes 80 mm off-centre give 18.5–20.5 m/s and 8–10.5 rev/s. This illustrates the speed–spin trade-off.

**Caveats.**
- Scale models carry a Re-scaling problem. Seam depth relative to D is not that of a real ball: Asai 2007 notes that the 1/3 model's Re_crit of about 1.3×10^5 is lower than for real balls.
- The tare correction is large.
- The equivalent full-size Re in Fig. 3 extends only to about 4.7×10^5 with the mini ball.
- The smooth-sphere result (0.53, still subcritical at 5×10^5) disagrees with Achenbach's 0.07. This underlines how set-up-dependent the smooth-sphere crisis is.

**Relevance.**
- Independent confirmation that a seamed ball sits at C_D ≈ 0.22–0.25 for Re ≈ 3.5–4.7×10^5.
- In this data, spin does not raise C_D materially, unlike Asai 2007.
- The authors themselves used C_D = 0.22 for a 26 m/s low-spin kick.

---

## 7. Alam, Chowdhury, Moria & Fuss 2010: Comparative study of football aerodynamics

**Citation.** Alam, F., Chowdhury, H., Moria, H. & Fuss, F. K. (2010). A comparative study of football aerodynamics. *Procedia Engineering* 2, 2443–2448 (ISEA 2010). doi:10.1016/j.proeng.2010.04.013.

**Method.**
- RMIT Industrial Wind Tunnel: closed return, maximum about 150 km/h, large test section.
- Real full-size balls on a sting with a JR-3 six-component sensor. The sting effect was judged negligible.
- Speeds 20–130 km/h (5.6–36 m/s).
- Smoke visualisation.

**Balls.**
- Nike 32-panel, stitched, 14.5 psi.
- Adidas 14-panel, thermally bonded (Teamgeist type), at 13 and 14.5 psi.
- Smooth sphere for comparison.

**Numerical data.** From Fig. 5 [fig, read], with linear Re axis and C_D readings ±0.005–0.01.

| Speed (km/h) | ≈ v (m/s) | Re | 14-panel C_D | 32-panel C_D | Smooth sphere C_D |
|---|---|---|---|---|---|
| 20 | 5.6 | 0.83×10^5 | 0.375–0.385 | 0.425 | 0.445 |
| 30 | 8.3 | 1.25×10^5 | 0.385 | 0.37 | 0.447 |
| 40 | 11.1 | 1.66×10^5 | 0.30 | 0.285 | 0.45 |
| 50 | 13.9 | 2.08×10^5 | 0.265 | 0.268 | 0.45 |
| 60 | 16.7 | 2.5×10^5 | 0.24 | 0.27 | 0.45 |
| 70 | 19.4 | 2.9×10^5 | 0.235 | 0.252 | 0.435 |
| 80 | 22.2 | 3.3×10^5 | 0.225–0.23 | 0.245 | 0.30 |
| 90 | 25.0 | 3.75×10^5 | 0.225 | 0.233 | 0.125 |
| 100 | 27.8 | 4.15×10^5 | 0.225 | 0.24 | 0.07 |
| **110** | **30.6** | **4.6×10^5** | **0.225** | **0.238** | **0.073** |
| 120 | 33.3 | 5.0×10^5 | 0.228 | 0.228 | 0.075 |
| 130 | 36.1 | 5.4×10^5 | 0.228 | 0.22 | 0.078 |

- **Text values** [text] p. 2446 and conclusions:
  - average C_D ≈ 0.23 above 60 km/h for both balls;
  - about 0.40 below 30 km/h;
  - ball transition over Re ≈ 1.1–3×10^5, versus 2.9–4.6×10^5 for the smooth sphere.
- **Panels.** The 32-panel ball is slightly higher at 60–120 km/h and fluctuates more.
- **Inflation pressure.** Has a negligible effect.
- **Separation angle.** About 100° for the 32-panel ball and about 90° for the 14-panel ball (smoke) [text].

**Caveats.**
- Single orientation, no spin.
- Lift and side forces were measured but not reported.
- No error bars. The temperature and ν used for Re are not stated.

**Relevance.**
- **This is the most direct measurement at our exact speed.** At 110–120 km/h (30.6–33.3 m/s), C_D = 0.225–0.24 for both ball types.
- On the same rig the smooth sphere gives 0.07 at the same speed. That is a factor of about 3 lower than any football.

---

## 8. Oggiano & Sætran 2010: Aerodynamics of modern soccer balls

**Citation.** Oggiano, L. & Sætran, L. (2010). Aerodynamics of modern soccer balls. *Procedia Engineering* 2, 2473–2479 (ISEA 2010). doi:10.1016/j.proeng.2010.04.018.

The PDF is image-only, so everything below was read from page renders.

**Method.**
- NTNU wind tunnel: 12.5 × 1.8 × 2.7 m test section, maximum about 30 m/s.
- Schenck six-component balance.
- Static ball on a shielded rear support. A spinning ball was driven by a motor support.
- Drag at 8 Re values between 6 and 26 m/s. Side force at 12, 17, 22 and 26 m/s × 4 spin rates.
- An RK trajectory simulation of a 25 m/s, 5 rev/s free kick.
- **Note on Re.** Their Re values (12 m/s → 1.54×10^5) imply μ ≈ 2.1×10^-5 Pa·s with r = 0.11 m and ρ = 1.225. The standard value is μ ≈ 1.8×10^-5, so their Re (1.29×10^4 per m/s) is the highest of the four groups and above the standard-air 1.47×10^4 per m/s. Compare by **speed** where possible.

**Balls.** Adidas Terrapass (matchball, 16 thermally bonded panels with a textured skin), Adidas Terrapass replica (not FIFA-approved), Puma v1.08 (24 panels with a dimpled casing) and Nike T90 Omni (micro-grooved casing).

**Numerical data.**

| Ball | Re_crit [text] | C_D min [fig, read] | C_D at top speed ~26 m/s (Re ≈ 3.4–3.6×10^5) [fig, read] |
|---|---|---|---|
| Adidas Terrapass | ≈ 2.0×10^5 | ≈ 0.14 at ~2×10^5 | ≈ 0.18–0.19 |
| Nike T90 | ≈ 1.5×10^5 | ≈ 0.16 | ≈ 0.18 |
| Adidas Replica | ≈ 1.5×10^5 | ≈ 0.155 | ≈ 0.165–0.17 (lowest at high speed) |
| Puma v1.08 | ≈ 1.2×10^5 | ≈ 0.12 at ~1.5×10^5 | ≈ 0.19–0.20 (highest at high speed) |

- **Subcritical C_D** (low speed): about 0.50–0.54 for all four [fig, read] Fig. 2.
- **Drag force range.** 0.5–3.8 N over 6–26 m/s [text] p. 2476.
- **Typo in the paper.** The text's "Re > 2×10^6" for the Terrapass having the highest drag is presumably a typo for 2×10^5.
- **Side-force coefficient C_S** [fig, read] Fig. 3:
  - at 26 m/s, Sp = 0.05–0.25: Terrapass 0.13–0.17; Nike and Replica 0.15–0.25; Puma 0.19–0.30;
  - at 12 m/s: reverse Magnus (C_S < 0) for Terrapass and Nike at Sp ≲ 0.25 [text].
- **Re_crit and side force.** A lower Re_crit goes with a higher C_S [text].

**Caveats.**
- The maximum speed of 26 m/s is below ours, so 31.5 m/s needs a small extrapolation. Every curve is flat or slightly rising there.
- The figure is small and low-resolution.
- There are no error bars.

**Relevance.**
- Shows the ball-to-ball spread among 2010-era balls: C_D ≈ 0.17–0.20 at 26 m/s, with a mild upward trend.
- Shows that even "dimpled" or textured balls do not exceed about 0.20 at these speeds.

---

## 9. Consolidated table: C_D vs Re/speed by ball type

Re here is standard air (ν ≈ 1.5×10^-5) at D = 0.22 m unless a paper's own Re is quoted. The ≈ v column is an approximate equivalent full-size speed.

| Ball type | Re_crit | Sub-crit C_D | Post-crisis min | C_D at Re ≈ 3.5–4×10^5 (≈ 24–27 m/s) | C_D at Re ≈ 4.5–5×10^5 (≈ 30–34 m/s) | Source |
|---|---|---|---|---|---|---|
| Smooth sphere | 3.7×10^5 | 0.47–0.50 | **0.07** (at 3.7×10^5) | 0.07–0.3 (on the cliff) | 0.07–0.08 | Achenbach 1972, Fig. 4 [fig, read]; Re_crit [text] |
| Smooth sphere (other rigs) | 3.5–4×10^5 or >5×10^5 | 0.44–0.53 | 0.07–0.1 | 0.12–0.45 | 0.07 (Alam) / 0.53 (Carré, still subcritical) | Asai 2007 [text]; Alam 2010 Fig. 5; Carré 2005 [text] |
| Rough sphere k/d = 2.5×10^-4 | ~3.5×10^5 | 0.50 | 0.07–0.08 | 0.08 | 0.08–0.10 | Achenbach 1974 Fig. 2 [fig, read] |
| Rough sphere k/d = 1.5×10^-3 | ~2×10^5 | 0.50 | 0.09 | 0.27 | 0.30–0.33 | Achenbach 1974 Fig. 2 [fig, read] |
| Rough sphere k/d ≥ 2.5×10^-3 | 0.8–1.6×10^5 | 0.50 | 0.10–0.20 | 0.33–0.38 | 0.35–0.39 | Achenbach 1974 Fig. 2 [fig, read] |
| Golf ball (dimpled) | ~6×10^4 | 0.5 | 0.22–0.25 | n/a (data end at 2.4×10^5) | n/a | Mehta 1985 Fig. 21; Asai 2007 Fig. 4 [fig, read] |
| Adidas Fevernova 2002 (32 p, stitched) | 2.2×10^5 | 0.43–0.47 | ≈ 0.15 | 0.16–0.17 | 0.19–0.20 | Asai 2007 [text] + Fig. 4 [fig, read] |
| Adidas Roteiro 2004 (32 p, bonded) | 2.2×10^5 | 0.43 | ≈ 0.14 | 0.15 | 0.15 | Asai 2007 [text] + Fig. 4 [fig, read] |
| Adidas Teamgeist 2006 (14 p, bonded) | 3.1×10^5 | 0.43–0.47 | ≈ 0.14 | 0.15 | 0.15 | Asai 2007 [text] + Fig. 4 [fig, read] |
| Generic 32-panel 1/3 model | 0.9–1.3×10^5 | 0.45–0.5 | ≈ 0.20 | n/a | n/a (≤ 3.2×10^5: 0.21–0.22) | Carré 2005 [text] + Fig. 3 |
| Mini Fevernova (140 mm) | <1.8×10^5 | n/a | ≈ 0.20 | 0.22–0.24 | 0.23–0.25 | Carré 2005 Fig. 3 [fig, read] |
| Nike 32-panel (stitched) | 1.1–3×10^5 | 0.37–0.43 | n/a (monotone) | 0.233–0.245 | 0.22–0.24 | Alam 2010 Fig. 5 [fig, read]; "≈0.23" [text] |
| Adidas 14-panel (bonded) | 1.1–3×10^5 | 0.38 | n/a (monotone) | 0.225 | 0.225–0.228 | Alam 2010 Fig. 5 [fig, read]; "≈0.23" [text] |
| Adidas Terrapass | 2.0×10^5 | 0.53 | 0.14 | 0.18–0.19 (26 m/s) | (extrap. ≈ 0.19–0.21) | Oggiano 2010 [text] + Fig. 2 [fig, read] |
| Nike T90 Omni | 1.5×10^5 | 0.53 | 0.16 | 0.18 (26 m/s) | (extrap. ≈ 0.18–0.20) | Oggiano 2010 |
| Adidas Terrapass replica | 1.5×10^5 | 0.53 | 0.155 | 0.165–0.17 (26 m/s) | (extrap. ≈ 0.17) | Oggiano 2010 |
| Puma v1.08 (dimpled) | 1.2×10^5 | 0.53 | 0.12 | 0.19–0.20 (26 m/s) | (extrap. ≈ 0.20–0.22) | Oggiano 2010 |
| Teamgeist FRP, **spinning** | n/a | n/a | n/a | 0.15 + 0.45·Sp (22–30 m/s, Sp 0.05–0.31) | 0.17 (Sp 0.05) to 0.29 (Sp 0.31) | Asai 2007 Fig. 8 [fig, read]; "0.3" for a real curve kick [text] |
| 1/3 model, **spinning** | n/a | n/a | n/a | n/a (Re ≤ 2.1×10^5: 0.19–0.21 for Sp 0–0.3) | n/a | Carré 2005 Fig. 7 [fig, read] |

**Spread of modern footballs at 30–34 m/s** (non-spinning, all four ball studies): **0.15–0.25**, centred near 0.20–0.22. The two measurements actually *at* our speed (Alam 2010) give 0.22–0.24. Asai 2007 gives 0.15–0.20.

---

## 10. Recommended C_D model and prior for our project

### 10.1 Functional form

Use a smooth logistic in log Re, with an optional linear spin term:

```
C_D(Re, Sp) = C_sup + (C_sub − C_sup) / (1 + (Re / Re_c)^n)  +  k_s · Sp
Sp = R·|ω| / v
```

| Parameter | Central value | Plausible range | Basis |
|---|---|---|---|
| C_sub (subcritical plateau) | 0.45 | 0.38–0.53 | Asai 2007 0.43; Alam 0.38–0.43; Carré 0.45–0.5; Oggiano 0.53 |
| C_sup (supercritical plateau) | **0.21** | 0.15–0.25 | Asai 2007 0.15–0.20; Carré 0.22–0.25; Alam 0.22–0.24; Oggiano 0.17–0.20 |
| Re_c (mid-point of the drop) | 1.8×10^5 | 1.2–3.0×10^5 | all four ball studies |
| n (steepness) | 8 | 4–15 | the drop spans about a factor 1.3–2 in Re (Asai, Alam, Oggiano figs) |
| k_s (spin slope) | 0.2 | 0–0.5 | 0.45 Asai 2007 (FRP model, 22–30 m/s); ≈ 0 Carré 2005 (scale model) |

**Notes.**
- At Re ≈ 4.6×10^5 the logistic term is below 0.005 for any n ≥ 4 with Re_c ≤ 3×10^5. **For the penalty kick the model reduces to C_D ≈ C_sup + k_s·Sp.**
- Over the 0.1 s window speed drops by only about 1.2–1.8 m/s, so a constant C_D is fully adequate. The Re dependence is needed only if we propagate the trajectory far enough for v to fall below about 20 m/s, which a penalty never does.
- A single post-crisis value is enough for us. If an extended model is wanted for Re > 3×10^5, use a mild slope of about +0.02 per 10^5 in Re, as seen for Fevernova, Puma and the mini ball.
- Do **not** use a smooth-sphere curve (Achenbach 1972) for a football. Its 0.07 bucket at 3.7–5×10^5 is exactly our operating point and would underestimate drag by a factor of about 3.

### 10.2 Prior for the test case (v ≈ 31.5 m/s, unknown modern ball, unknown spin)

- **Recommended prior: C_D ~ Normal(0.22, 0.04²), truncated to [0.12, 0.35].**
  - The mean 0.22 matches Alam's direct measurement and Carré's value. It sits between Asai's 0.15–0.20 and the slight upward allowance for spin.
  - σ = 0.04 covers the ball-to-ball spread (0.15–0.25) and a moderate spin contribution (up to about +0.05 at Sp ≈ 0.1–0.2).
- **If spin is estimated from video:**
  - typical penalty spin is 2–5 rev/s, giving Sp ≈ 0.04–0.11;
  - use C_D ≈ 0.20 + (0 to 0.45)·Sp, i.e. 0.20–0.25.
- **Sensitivity check.** The drag deceleration is a ≈ 52.6·C_D m/s² (ρ = 1.2, m = 0.43 kg, A = 0.038 m², v = 31.5 m/s). So C_D = 0.22 gives a ≈ 11.6 m/s².

---

## 11. Answers to the three claims

### Claim 1: "Real panelled balls show a milder drag crisis at lower Re than a smooth sphere, with supercritical C_D ≈ 0.15–0.25."

**Largely VERIFIED, with refinements.**
- **Lower Re: yes.** Re_crit for balls is 1.2–3.1×10^5:
  - 2.2–3.1×10^5 [Asai 2007, text p. 104];
  - 1.1–3×10^5 [Alam 2010, text];
  - 1.2–2.0×10^5 [Oggiano 2010, text];
  - 0.9–1.3×10^5 for the 1/3 model [Carré 2005, text].
  This compares with 3.5–3.7×10^5 for the smooth sphere [Achenbach 1972, text p. 569].
- **Milder: yes in depth**, but not necessarily in steepness.
  - Balls drop from about 0.43–0.53 to a minimum of about 0.12–0.16. The smooth sphere drops from about 0.5 to 0.07.
  - The drop for balls is still fairly abrupt (within a factor of about 1.5–2 in Re) [Asai 2007 Fig. 4; Oggiano Fig. 2; fig, read].
  - Alam's balls show the gentlest, monotone decline [Alam 2010 Fig. 5].
- **Supercritical 0.15–0.25: yes.**
  - All ball data at Re ≈ 3–5.4×10^5 fall in 0.15–0.25 [§9 table].
  - Brief minima down to 0.12–0.14 occur just after the crisis (Puma, Asai balls), at Re ≈ 1.5–3×10^5. These are not relevant at 31.5 m/s.
  - One refinement: Asai 2007's conclusion states sub ≈ 0.43 and super ≈ 0.15 [text p. 108]. So 0.15 is the lower bound, not an outlier.

### Claim 2: "The B-471 team's table (C_D → 0.06 at 30 m/s, from a smooth-sphere curve) is unrepresentative of footballs."

**VERIFIED.**
- **What Achenbach gives for the smooth sphere:**
  - C_D falls to a minimum at **Re_crit ≈ 3.7×10^5** [Achenbach 1972, text p. 569].
  - The minimum value is **≈ 0.07** (scatter about 0.06–0.08) [Fig. 4, fig, read].
  - It then rises slowly: about 0.08 at 5×10^5, 0.12 at 10^6 [fig, read], and 0.19 at 6×10^6 [text p. 570].
- **Why the table shows 0.06.** At D = 0.22 m, 30 m/s is Re ≈ 4.4×10^5. That falls in the smooth sphere's bucket, which explains the B-471 value. The value 0.06 is at the very bottom of Achenbach's scatter; 0.07–0.08 is the representative bucket value.
- **Why it is wrong for footballs.** Every football measurement at the same speed is 2.5–4× higher:
  - 0.225–0.24 at 30.6–33.3 m/s [Alam 2010 Fig. 5, fig, read], where the smooth sphere on the same rig gives 0.073;
  - 0.15–0.20 at about 33–35 m/s [Asai 2007 Fig. 4];
  - 0.23–0.25 at Re ≈ 4.5×10^5 [Carré 2005 Fig. 3].
- **The smooth-sphere bucket is not even robust for spheres.** Carré's smooth sphere stayed subcritical (C_D ≈ 0.53) up to an equivalent Re of 5×10^5 [Carré 2005, text p. 662]. A model built on it is therefore both unrepresentative and fragile.

### Claim 3: "Our preliminary fit gave C_D ≈ 0.35 ± 0.05 at v ≈ 31.5 m/s. Is that plausible for some balls, or is it a sign of model or noise problems?"

**Most likely a model or noise problem.** It is physically possible only in edge cases.
- **Against the literature.**
  - Non-spinning modern balls at this speed give 0.15–0.25 (§9). A value of 0.35 is about 3σ above our prior mean (0.22 ± 0.04).
  - The fit's own 1σ lower edge (0.30) still sits above every non-spinning football measurement.
- **How could a real ball reach 0.35? Only in these cases:**
  - (a) **Very high spin.** Asai 2007 reaches 0.29 at Sp = 0.31 (about 14 rev/s at 31.5 m/s) [Fig. 8, fig, read], and reports about 0.3 for a real curve kick [text p. 106]. Extrapolating to 0.35 needs Sp ≈ 0.4 (about 18 rev/s), which is implausible for a penalty. Carré 2005 finds no spin effect on C_D at all.
  - (b) **A uniformly rough sphere.** With k/d ≳ 2×10^-3, Achenbach 1974 gives 0.33–0.38 at Re ≈ 4–5×10^5 [Fig. 2, fig, read]. That would need roughness of about 0.4 mm or more over the whole surface, which describes no ball in these papers.
  - (c) **A subcritical ball** (0.38–0.53). This is excluded at 31.5 m/s for every ball tested.
- **Why noise and modelling are the likely cause.** With samples at 0, 0.05 and 0.10 s, C_D is fixed essentially by the second difference of position, Δ²x = a·Δt².
  - C_D = 0.22 gives Δ²x ≈ 29 mm and C_D = 0.35 gives about 46 mm. The difference is only about 17 mm.
  - The result is that σ(C_D) = 0.05 corresponds to just about 2.7 mm of per-point position noise. So **±0.05 is optimistic unless positions are known to about 3 mm.**
  - At that level of precision, small errors can produce the +0.13 excess:
    - frame-timing jitter;
    - a scale or perspective error;
    - a projection error in depth (a 3-D path seen in 2-D);
    - Magnus or lift acceleration aliased into the along-track direction;
    - mis-handling of the gravity component.
  - The gravity component alone is small: a 5° launch adds g·sin θ ≈ 0.85 m/s², equivalent to ΔC_D ≈ 0.016.
- **Recommendation.**
  - Do not fit C_D freely from three points. Impose the prior N(0.22, 0.04) and let the data update it.
  - Check whether the posterior shifts at all. If the data "want" 0.35, test the residuals for timing, scale or projection errors first.
  - Propagate C_D uncertainty into the goal-entry point. Over the 11 m to the goal (t ≈ 0.36 s), ΔC_D = ±0.04 means Δa ≈ ±2.1 m/s². That shifts the ball about ±13 cm *along* its path, i.e. it changes arrival time by about ±4 ms. Drag acts along the velocity, so it barely moves the entry point. The only effect is the extra gravity drop during that ±4 ms, g·t·Δt ≈ ±1.5 cm. **Drag is a minor error source compared with errors in initial velocity and direction.**
