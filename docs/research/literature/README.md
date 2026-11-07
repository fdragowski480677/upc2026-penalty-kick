# Literature notes: index and consolidated parameters

The sources are the 20 papers cited by the 2022 reports (PDFs kept locally in `references/2022/`, not committed).
Detailed notes per cluster:

| File | Cluster | Sources |
|---|---|---|
| [`drag.md`](drag.md) | C_D vs Re, drag crisis, roughness/seams | Achenbach 1972, 1974; Mehta 1985; Asai 1998, 2007; Carré 2005; Alam 2010; Oggiano 2010 |
| [`lift-spin.md`](lift-spin.md) | Magnus/lift, spin, knuckle effect | Kray 2014; Bray & Kerwin 2003; Barber 2007, 2009; Watts & Sawyer 1975; Wesson 2002; Haake (ed.) 1996 |
| [`kick-keeper.md`](kick-keeper.md) | Foot–ball contact, launch speeds, goalkeeper timing | Ravenscroft & Linthorne 2015; Ishii 2012; Naito 2010; Hunter 2018; Murakami 1988 |

Many values were **read by eye from figures** (marked "fig." in the cluster notes, typically ±0.01–0.02 in a coefficient).

## Consolidated parameter table (for Stages 2–4)

Conditions: v ≈ 31.5 m/s, Re ≈ 4.6×10⁵ (supercritical throughout the flight).

| Quantity | Nominal | Prior / range | Source(s) | Status |
|---|---|---|---|---|
| C_D, non-spinning | 0.22 | N(0.22, 0.04²), truncated to [0.12, 0.35] | Alam 2010 (0.22–0.24 at 30–33 m/s); Asai 2007 (0.15–0.20); Carré 2005; Oggiano 2010 | verified |
| C_D spin dependence | +k_s·S | k_s = 0.45 [Asai 2007] … 0.74 [Kray 2014] (≈ 0 in Carré 2005) | — | **contradictory**; at S ≈ 0.1 gives C_D ≈ 0.20–0.32 |
| C_D(Re) form | logistic, Re_c ≈ 1.8×10⁵, n ≈ 8 | C_sub 0.38–0.53 | drag.md §10 | not needed for a penalty (always supercritical) |
| C_L(S) | 0.29·(1 − e^(−S/0.072)) at Re 4.6×10⁵ | pooled: C_Lmax 0.31 ± 0.03, S₀ 0.11 ± 0.03; C_L ≤ 0.35 | Kray 2014 Fig. 9 (fig., our fit) | verified at one ball (14-panel) |
| C_L from real kicks | 0.26 | 0.23–0.29 ± 0.05 | Bray & Kerwin 2003 | consistent |
| Inverse Magnus | — | only at Re ≈ 2×10⁵ (≈ 14 m/s) | Kray 2014 | excluded for us |
| Seam-induced side force | 0 | C_S ~ N(0, 0.03–0.05²), max ≈ 0.1 | Barber 2009; Kray 2014 Fig. 3 | nuisance term (cannot be told apart from Magnus in 0.1 s) |
| Spin decay | none | ±5 % systematic over the flight (C_M 0.005–0.02, our estimate) | — | **unsourced, open** |
| Typical penalty spin | 2–8 rev/s | S ≈ 0.045–0.18 | Wesson 2002; Bray & Kerwin; Kray inversion | estimated |
| Launch speed | — | university 23.9 ± 1.2 m/s; elite mean ≈ 31, max ≈ 36 m/s | Ravenscroft & Linthorne 2015; Wesson 2002 | verified |
| Launch elevation | — | 8 ± 5° | Ravenscroft & Linthorne 2015 | verified |
| Foot contact time | ≈ 10 ms | 8.8–12.0 ms | Ishii 2012 | verified |
| Keeper dive start | −0.22 s (before contact) | ± 0.11 s | Hunter 2018 | verified |
| Direction accuracy from kicker cues | ≈ 70 % at −0.2 s; 80–90 % at contact | — | Hunter 2018 | verified |

## Key conclusions for the 2026 model
1. **Use the measured C_L(S), never 16/3·S.** For our test case it yields S ≈ 0.09 (4–6 rev/s), not 0.2–0.3.
2. **The entry point is insensitive to C_D** once v₀ is fitted to the data (scratch check: Δy ≈ 0, Δz ≈ 4 cm for C_D 0.15–0.35).
   The lift model and its uncertainty dominate.
3. **t = 0 behaves as a free-flight origin** (the interval lengths rule out a contact lag); both observations are in free flight.
4. **Open gaps:** a measured spin-decay rate; a resolution of the Asai–Kray spin-drag contradiction; C_L data for other ball
   types (Kray only tested a 14-panel model); Asai et al. 2002 on the curve kick (spin from off-centre impacts) is cited but not in our folder.
