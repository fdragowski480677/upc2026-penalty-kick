# Literature cluster E: ball impact mechanics, kick-generated spin, tracking accuracy, ball regulations

The team added these sources for Stage 5 and the environmental Monte Carlo. The coordinator read all of them in full, plus
Price Fig. 4 as a rendered figure. Tags: [lit], [ours].

## 1. Price, Jones & Harland 2007: Advanced finite-element modelling of a 32-panel soccer ball
*Proc. IMechE Part C 221, 1309–1319. doi:10.1243/09544062JMES711.*
- An FE shell model of a hand-stitched elite 32-panel ball: anisotropic woven panels (**E = 8 MPa at 0°/90°, 48 MPa at 45°**), seams
  5× stiffer than the panels, a latex bladder, **1 bar gauge pressure**, and stiffness-proportional damping. Validated within 5 % against normal impacts on
  a steel plate filmed at 10 000 fps.
- **Fig. 4 (read by the coordinator):**

| Impact speed (m/s) | 9 | 14 | 22 | 32 |
|---|---|---|---|---|
| COR (normal) | 0.87–0.92 | 0.82–0.85 | 0.78–0.80 | 0.70–0.77 |
| Contact time (ms) | 8.3–8.6 | 7.6–7.9 | 6.8–7.5 | 6.3–7.0 |
| Max deformation (mm) | 23–30 | 35–40 | 52–56 | 65–72 |

- Impact behaviour depends on **orientation** (7 distinct distortion types, panel buckling). Anisotropy can *induce* post-impact spin.
- **Relevance:** gives the speed-dependent normal COR e_n(v) ≈ 0.95 − 0.0072 v [ours, a linear fit to the figure] for the Stage 5 post/bar
  collision; contact times of 6–9 ms; a scatter that sets the COR uncertainty (≈ ±0.03).

## 2. Cross 2002: Grip-slip behavior of a bouncing ball
*Am. J. Phys. 70, 1093–1102.*
- Measured normal (N) and friction (F) forces on obliquely bouncing balls. **Real balls do not roll; they grip, then slip.** F reverses direction
  during the bounce, and the ball spins faster than the rolling condition allows.
- Model (Eqs. 8–12): a bounce is characterised by the normal COR e_y, the **tangential COR e_x** = −(v_x2 − Rω₂)/(v_x1 − Rω₁), and an offset D of
  the normal force, with I = αmR² (α = 2/3 for a thin shell). Pure sliding (F = μN) holds below a critical incidence angle (Eq. 7).
- Measured values: e_x ≈ 0.1–0.2 when gripping (tennis), 0.49 (superball); D ≈ 2–3 mm; e_x < 0 when sliding throughout.
- **Relevance:** the **equations for the Stage 5 collision model** (oblique impact with spin on the post surface, using the local normal).

## 3. Cross 2005: Bounce of a spinning ball near normal incidence
*Am. J. Phys. 73, 914–920. doi:10.1119/1.2008299.*
- Closed form for a bounce characterised by e_x (Eqs. 3–4): v_x2/v_x1 and ω₂/ω₁ as linear functions of Rω₁/v_x1. Validated (39 bounces).
- Tennis-ball values: e_x ≈ 0.06–0.08 for a spinning ball on a rigid floor, 0.13–0.32 without spin; the friction coefficient matters little near the normal.
- **Relevance:** how incident spin (our ≈ 5 rev/s sidespin) changes the rebound direction off a post. **Gap:** e_x and μ for a *football* on a
  *painted aluminium post* are not given in any source we hold.

## 4. Asai, Carré, Akatsuka & Haake 2002: The curve kick of a football I: impact with the foot
*Sports Engineering 5, 183–192.*
- 4500 fps video of 6 university players (official FIFA ball, **11 psi ≈ 0.76 bar gauge**). **Contact time 9.12 ± 0.28 ms**, ball speed **25.44 ± 0.76 m/s**,
  foot speed 23.1 m/s, foot travel during contact 0.147 m. The ball deforms to 85 % of its diameter.
- A coupled FE (foot) and fluid–structure (ball air, γ-law gas) model. Foot E = 30 MPa, calf 300 MPa, Poisson ratio 0.3, leg mass 4 kg, foot speed 25 m/s.
- **Spin versus impact offset (Table 2, friction μ = 0.4):** offset 0 → 1.9 rev/s at 26.0 m/s; 0.04 m → 4.0 rev/s at 23.1 m/s; 0.06 m → 6.9 rev/s
  at 20.7 m/s; 0.08 m → 10.5 rev/s at 18.5 m/s; maximum 16.2 rev/s at 0.12 m (11.2 m/s). Friction from 0 to 1 adds at most 13 rad/s; spin occurs
  even at μ = 0, via deformation. The infront curve kick gives 32.7 rad/s (5.2 rev/s).
- **Relevance:** a quantitative **speed–spin trade-off**. At a fixed foot speed, every rev/s of spin costs launch speed. See the consistency check below.

## 5. Ronkainen & Harland 2010: Laser tracking system for sports ball trajectory measurement
*Proc. IMechE Part P 224, 219–228. doi:10.1243/17543371JSET67.*
- A galvanometer-steered laser and camera tracker; real time up to ≈ 10 m/s; 2-D launch monitor.
- Accuracy: launch angle within ±0.5°; **speed systematically 0.8 m/s higher than high-speed video (0.11–1.3 m/s range)**, attributed to misalignment.
- **Relevance:** real ball tracking has **systematic (correlated) errors**, not only independent noise. This supports a noise sensitivity case with a
  correlated bias term, beyond the isotropic iid σ. The technology tested is slower than our 32 m/s ball.

## 6. IFAB Laws of the Game 2025/26, Law 2 (the ball), fetched from theifab.com
- Spherical; circumference **68–70 cm**; mass **410–450 g at the start of the match**; pressure **0.6–1.1 atm (600–1100 g/cm²) at sea level**.
- A ball that becomes defective during a penalty before touching a player, the crossbar or the posts → the penalty is retaken.

## 7. FIFA Quality PRO certificate: adidas "FIFA World Cup 26 Trionda Pro", fetched from inside.fifa.com
- Size 5, **FIFA Quality PRO**, licence 1019112, test institute EMPA, test manual **v1.2**, valid 9 Sept 2024 – 8 Sept 2028.
- **The page contains no numerical specifications.** The Quality PRO limits (tighter than Law 2: circumference, mass, sphericity, rebound,
  water uptake, pressure loss, test temperatures) are in the FIFA test manual, which **we do not have** (gap).
- There is **no wind-tunnel C_D/C_L data for Trionda** in our sources. Our coefficients come from older 14/32-panel designs, so the ball-to-ball spread
  is retained as uncertainty.

## Consistency check from Asai 2002 [ours, preliminary]
At a foot speed of ≈ 25 m/s, Asai's model gives a ball speed of ≈ 26 m/s at ≈ 2 rev/s and ≈ 22 m/s at ≈ 5 rev/s (ratio ≈ 0.85). Our test case has
**32.6 m/s with a posterior median of ≈ 5 rev/s**. Scaling linearly, that needs a foot speed of ≈ 30 m/s, far above the measured 17–25 m/s
(Ishii 2012; Ravenscroft & Linthorne 2015; Asai 2002). **A 32 m/s shot is more plausibly a low-spin (≈ 1–3 rev/s) instep strike.** If that holds,
a physically joint speed–spin prior would shift the posterior toward lower spin, and the entry point toward the post (y ≈ 2.8–3.0 m instead of 2.6–2.7 m).
This is to be checked properly in Stage 5 with the foot–ball contact model.

## Environment and ball parameters for the Monte Carlo (team proposal: sample within the physical limits)
| Quantity | Physics | Effect on flight |
|---|---|---|
| Air density ρ(T, p, RH) | ideal-gas moist air, ρ = (p_d M_d + p_v M_v)/(RT); barometric altitude (Hörzer 2010) | drag and Magnus ∝ ρ, **first order** |
| Air viscosity μ(T) | Sutherland's law; ν = μ/ρ | via Re only; supercritical, so weak |
| Ball mass m | Law 2: 410–450 g (FIFA PRO tighter); water uptake on a wet day | aerodynamic acceleration ∝ ρR²/m, **first order** |
| Ball radius R | circumference 68–70 cm | ∝ R² in K; also in S = Rω/v and Re |
| Internal pressure | 0.6–1.1 atm gauge; p_abs ∝ T at fixed volume | **none in flight** (rigid shell); sets COR and contact time → Stage 5 |

## 8. Hong & Asai 2014: Effect of panel shape of soccer ball on its flight characteristics
*Sci. Rep. 4, 5068. doi:10.1038/srep05068.* Read by the coordinator; Fig. 3 verified.
- Wind tunnel (Tsukuba, turbulence ≤ 0.1 %, rear sting), 7–35 m/s, two panel orientations; balls Brazuca (6 panels), Cafusa (32),
  Jabulani (8), Teamgeist 2 (14), conventional (32). Plus an impact kick robot at 30 m/s, < 1 rotation, 25 m to a goal, 20 kicks per orientation.
- **Supercritical C_D at Re ≈ 4.5–5×10⁵ (Fig. 3):** Brazuca ≈ 0.20; Cafusa ≈ 0.17; Jabulani 0.14–0.17; Teamgeist 2 0.21–0.23;
  conventional 0.19–0.21. Critical Re ≈ 2.2–3.6×10⁵ depending on the ball and orientation.
- Unsteady side and lift forces grow from 20 to 30 m/s and correlate with total seam length. Non-spinning impact-point SDs over 25 m are
  0.13–0.68 m (knuckling). **Our ball spins at ≥ 2 rev/s**, which averages these forces out (Kray 2014; Barber 2009).

## 9. Goff, Hong & Asai 2018: Aerodynamic and surface comparisons between Telstar 18 and Brazuca
*Proc. IMechE Part P. doi:10.1177/1754337118773214.* Read by the coordinator; Figs. 5–10 verified.
- The same tunnel, non-spinning, 7–35 m/s, two orientations; ν = 1.54×10⁻⁵ at 24 °C, ρ = 1.2, A = 0.038 m². Masses: Telstar 18 0.429 kg, Brazuca 0.426 kg.
- **C_D at 28–35 m/s:** Telstar 18 ≈ 0.20 (0°), 0.20–0.21 (45°); Brazuca ≈ 0.19–0.20. Critical speed ≈ 15 m/s.
- **Steady side and lift coefficients above the critical speed are within ≈ ±0.03** (one point at −0.09 at 35 m/s). Lateral knuckle deflection is ≤ 4 % of range.
- Seams: Telstar 18 has 6 panels, 4.32 m of seams, 1.1 mm deep; Brazuca has 6 panels, 3.32 m, 1.4 mm. Longer but shallower seams give a similar aerodynamic roughness.
- **Implications:** (i) for a modern six-panel World Cup ball (the closest proxy for Trionda), C_D ≈ 0.20. That is within our prior N(0.22, 0.04),
  which is kept as decided; the new presets are switches. (ii) The seam/orientation nuisance prior σ_C_S = 0.03 is confirmed.

## 10. FIFA Quality Programme for Footballs (web page) and goal frame (team table)
- The page names the seven tests (weight, circumference, roundness, bounce, water absorption, loss of pressure, shape and size retention) and says
  Quality PRO passes them "under even more demanding conditions". **No numerical limits are on the page, and no test-manual PDF is linked.**
  The file added to the references index (FIFA-TTM-I) is the *football turf* manual and is not present in the folder. **The ball ranges
  therefore stay at IFAB Law 2.**
- Goal frame (team table): internal 7.32 × 2.44 m, external 7.56 × 2.56 m, post/bar width and depth ≤ 120 mm, profiles round, elliptical, square,
  rectangular or hybrid. This is consistent with `constants.Goal` (frame width 0.12 m). The profile matters only for the Stage 5 collision normal.

## 11. Venue altitudes (team table) and ISA densities
Mexico City 2240 m (ρ_ISA 0.982), Guadalajara 1670 m (1.040), Monterrey 550 m (1.162), sea level 1.225 kg/m³. These are reproduced by
`environment.py` (test). Our Monte Carlo uses summer match temperatures (12–35 °C) instead of the ISA lapse-rate temperature, so at altitude it gives
lower densities (e.g. Mexico City ≈ 0.88–0.95 kg/m³ at 20–30 °C).
