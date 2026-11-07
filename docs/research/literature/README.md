# Literature notes: index and consolidated parameters

The sources are the 20 papers cited by the 2022 reports, plus 3 added by the team for Stage 3 (PDFs kept locally in `references/2022/`, not committed).
Detailed notes per cluster:

| File | Cluster | Sources |
|---|---|---|
| [`drag.md`](drag.md) | C_D vs Re, drag crisis, roughness/seams | Achenbach 1972, 1974; Mehta 1985; Asai 1998, 2007; Carré 2005; Alam 2010; Oggiano 2010 |
| [`lift-spin.md`](lift-spin.md) | Magnus/lift, spin, knuckle effect | Kray 2014; Bray & Kerwin 2003; Barber 2007, 2009; Watts & Sawyer 1975; Wesson 2002; Haake (ed.) 1996 |
| [`kick-keeper.md`](kick-keeper.md) | Foot–ball contact, launch speeds, goalkeeper timing | Ravenscroft & Linthorne 2015; Ishii 2012; Naito 2010; Hunter 2018; Murakami 1988 |
| [`spin-decay-and-free-flight.md`](spin-decay-and-free-flight.md) | Spin decay, spin-dependent drag, free-flight Magnus data, air density | James & Haake 2008; Hörzer 2010; Asai 2020 (read in full by the coordinator) |

Many values were **read by eye from figures** (marked "fig." in the cluster notes, typically ±0.01–0.02 in a coefficient).

## Consolidated parameter table (for Stages 2–4)

Conditions: v ≈ 31.5 m/s, Re ≈ 4.6×10⁵ (supercritical throughout the flight).

| Quantity | Nominal | Prior / range | Source(s) | Status |
|---|---|---|---|---|
| C_D, non-spinning | 0.22 | N(0.22, 0.04²), truncated to [0.12, 0.35] | Alam 2010 (0.22–0.24 at 30–33 m/s); Asai 2007 (0.15–0.20); Carré 2005; Oggiano 2010 | verified |
| C_D spin dependence | +k_s·S | k_s = 0.45 [Asai 2007] … 0.74 [Kray 2014] (≈ 0 in Carré 2005) | — | ball/rig-dependent (see verification §1); at S ≈ 0.1 gives C_D ≈ 0.20–0.34 |
| C_D(Re) form | logistic, Re_c ≈ 1.8×10⁵, n ≈ 8 | C_sub 0.38–0.53 | drag.md §10 | not needed for a penalty (always supercritical) |
| C_L(S) | 0.29·(1 − e^(−S/0.072)) at Re 4.6×10⁵ | pooled: C_Lmax 0.31 ± 0.03, S₀ 0.11 ± 0.03; C_L ≤ 0.35 | Kray 2014 Fig. 9 (fig., our fit) | verified at one ball (14-panel) |
| C_L from real kicks | 0.26 | 0.23–0.29 ± 0.05 | Bray & Kerwin 2003 | consistent |
| Inverse Magnus | — | only at Re ≈ 2×10⁵ (≈ 14 m/s) | Kray 2014 | excluded for us |
| Seam-induced side force | 0 | C_S ~ N(0, 0.03–0.05²), max ≈ 0.1 | Barber 2009; Kray 2014 Fig. 3 | nuisance term (cannot be told apart from Magnus in 0.1 s) |
| Spin decay | none | dω/dt = −kω|v|/R; k = 1.4×10⁻⁴ (≈ 1.5 % over the flight), upper bound 2×10⁻³ | Asai 2020 (free flight); James & Haake 2008 | **sourced** (spin-decay-and-free-flight.md) |
| Typical penalty spin | 2–8 rev/s | S ≈ 0.045–0.18 | Wesson 2002; Bray & Kerwin; Kray inversion | estimated |
| Launch speed | — | university 23.9 ± 1.2 m/s; elite mean ≈ 31, max ≈ 36 m/s | Ravenscroft & Linthorne 2015; Wesson 2002 | verified |
| Launch elevation | — | 8 ± 5° | Ravenscroft & Linthorne 2015 | verified |
| Foot contact time | ≈ 10 ms | 8.8–12.0 ms | Ishii 2012 | verified |
| Keeper dive start | −0.22 s (before contact) | ± 0.11 s | Hunter 2018 | verified |
| Direction accuracy from kicker cues | ≈ 70 % at −0.2 s; 80–90 % at contact | — | Hunter 2018 | verified |

## Coordinator verification of the three key sources

I read Kray 2014, Alam 2010 and Ishii 2012 in full and re-read their key figures from rendered pages: Kray Fig. 9, Alam Fig. 5 and
Ishii Fig. 5/Table 1. This was done independently of the cluster notes.

| Source | Value in notes | Own reading | Verdict |
|---|---|---|---|
| Kray Fig. 9, C_M at Re 4.62×10⁵ | 0.11 / 0.15 / 0.185 / 0.22 / 0.24 / 0.255 / 0.27 / 0.275 / 0.285 at S = 0.026…0.23 | same (±0.005); **plus C_M ≈ −0.045 at S = 0** (non-rotating, arbitrary orientation) | ✓ |
| Kray Fig. 9, C_D at Re 4.62×10⁵ | 0.25 → 0.40; "≈ 0.25 + 0.74 S" | 0.255, 0.253, 0.277, 0.313, 0.34, 0.362, 0.377, 0.383, 0.392, 0.40 | ✓ values; the linear fit is crude (flat to S ≈ 0.03, then saturating) |
| Kray Fig. 9, C_M at Re 3.42×10⁵ | 0.00 / 0.065 / 0.15 / 0.20 / 0.23 / … / 0.297 | same | ✓ |
| Kray text | C_M levels off at 0.30–0.35; use only above 2 Hz; inverse Magnus C_M = −0.09 at S = 0.12, Re 2.06×10⁵ | same (pp. 51–52) | ✓ |
| Alam Fig. 5, C_D at 110–120 km/h (30.6–33.3 m/s) | 0.225–0.24; smooth sphere 0.073 | Adidas 0.225–0.228, Nike 0.227–0.238; sphere 0.073–0.075 | ✓ (also consistent with the Fig. 4 drag force: 6.7 N at 130 km/h → C_D ≈ 0.226) |
| Alam text | "≈ 0.23 above 60 km/h" | the figure shows 0.24–0.27 at 60–70 km/h; the plateau of 0.225–0.24 starts at about 80 km/h | minor overstatement in the paper |
| Ishii Table 1 | contact means 9.6–10.7 ms, range 8.8–12.0 ms | same | ✓ |
| Ishii Fig. 5 / text | peak force 1.06–2.23 kN, near-half-sine, peak at ≈ 4 ms; deformation 29–65 mm | same (≈ 2000 N at ≈ 4.2 ms in the example) | ✓ |
| Ishii Table 1 speeds | "launch speed 17.1–24.7 m/s" | these are **normalised** ball speeds, from lab kicks off a stand | caveat added to kick-keeper.md |
| Knuckle threshold | "2 rev/s ⇔ S ≲ 0.1 at 30 m/s" | 2 rev/s ⇔ S ≈ 0.046 | inconsistency in the sources; corrected in lift-spin.md; conclusion unchanged |

**Additional points the cluster notes under-weighted:**
1. **Kray's own caveats.** The model is an *aluminium 14-panel prototype* (D = 226 mm), not a real ball. Kray argues that earlier
   soccer-ball force data (Asai 2007, Carré 2005, Oggiano 2010, Passmore 2011) suffers from support interference and "cannot be
   considered as reliable" [p. 47]. He attributes Teamgeist's lower drag in Asai 2007 to a later separation angle (≈ 115°) [p. 49].
   **So the Asai–Kray C_D(S) disagreement is a ball-to-ball and rig-to-rig difference rather than a contradiction to resolve.**
   For us it becomes model uncertainty, covered by the wide C_D prior and the insensitivity of the entry point to C_D.
2. **The Re-sensitivity of C_L lies exactly in our regime.** Kray notes the curves differ most for 0.025 < S < 0.15 [p. 52]. At S = 0.07
   C_L is 0.18 at Re 4.62×10⁵ but 0.065 at Re 3.42×10⁵. Our ball slows from ≈ 32 to ≈ 28 m/s (Re 4.7 → 4.1×10⁵) while S rises at
   constant ω. **C_L(S, Re) along the flight is therefore the single most important modelling uncertainty for Stage 3.** It should be
   interpolated between the two curves, not fixed.
3. **The non-spinning C_D varies by ball:** Kray 0.255 (+0.01 from the gap), Alam 0.225–0.24, Asai/Teamgeist ≈ 0.15. The prior
   N(0.22, 0.04²) covers this.
4. **The contact-lag test survives 1 cm noise.** The difference of the two interval lengths has σ = √5 · 1 cm ≈ 2.2 cm, and a 5 ms lag would
   shift it by ≈ 0.15 m. That is a ≈ 6σ exclusion.

## Key conclusions for the 2026 model
1. **Use the measured C_L(S), never 16/3·S.** For our test case it yields S ≈ 0.09 (4–6 rev/s), not 0.2–0.3.
2. **The entry point is insensitive to C_D** once v₀ is fitted to the data (scratch check: Δy ≈ 0, Δz ≈ 4 cm for C_D 0.15–0.35).
   The lift model and its uncertainty dominate.
3. **t = 0 behaves as a free-flight origin** (the interval lengths rule out a contact lag); both observations are in free flight.
4. **Open gaps:** a measured spin-decay rate; C_L(S, Re) between Kray's two supercritical curves (largest uncertainty for Stage 3); C_L data for other ball
   types (Kray only tested a 14-panel model); Asai et al. 2002 on the curve kick (spin from off-centre impacts) is cited but not in our folder.
