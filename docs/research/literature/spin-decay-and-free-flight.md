# Literature cluster D: spin decay, spin-dependent drag, free-flight Magnus data

The user added these sources for Stage 3. The coordinator read all three in full, including the equation images
rendered from the PDFs. Tags follow the analysis doc: [theory], [lit], [ours].

## 1. James & Haake 2008: The spin decay of sports balls in flight
*In: The Engineering of Sport 7, Vol. 2, pp. 165–170 (Springer).*
- **Method:** indoor launches with ball-projection machines; synchronised 500 fps cameras at the start and end of the
  trajectory; > 100 sequences. Uncertainty: spin ±10 rad/s, speed ±0.3 m/s. Balls: new and worn tennis balls, an oversize tennis ball, and a football (R = 0.11 m).
- **Model [lit: Smits & Smith 1994]:** $d\omega/dt = c\,U\,\omega$ (eq. 1). In dimensionless form, $SRD = \dfrac{(d\omega/dt)\,r^2}{U^2}$ (eq. 3) is
  linear in the spin parameter $\alpha = \omega r/U$ (eq. 2), with $SRD = k\,\alpha$ (Fig. 4).
- **Consequence [ours]:** $d\omega/dt = -k\,\omega\,U/r$. This is exponential decay with a **speed-dependent time constant
  $\tau = r/(kU)$**, not a fixed τ.
- **Football slope (Fig. 4, read by the coordinator):** $k \approx 2.0\times10^{-3}$, the highest of all the balls tested. **Caveat stated by the
  authors:** launches were at ≈ 7 m/s (Re subcritical, laminar boundary layer), and they expect the football to behave much
  more like a golf ball above ≈ 10.3 m/s (Re > 1.53×10⁵). So this k is an **upper bound**, not applicable at 30 m/s.
- At U = 30 m/s, k = 2×10⁻³ would give τ ≈ 1.8 s and a ≈ 20 % spin loss over 0.39 s [ours]. This is an upper bound only.

## 2. Hörzer et al. 2010: Simulation of spinning soccer ball trajectories influenced by altitude
*Procedia Engineering 2, 2461–2466. doi:10.1016/j.proeng.2010.04.016.*
- **Model:** 3-D, with gravity, drag $-\tfrac12\rho A C_d v^2\hat v$ and Magnus $\tfrac12\rho A C_m v^2(\hat\omega\times\hat v)$ (the same structure as ours).
  The spin axis is tilted (5° in x–z from video, 10° in y–z from Bray & Kerwin). Only the velocity component perpendicular to the axis enters S and F_M.
  Explicit stepping with Δt = 1 ms.
- **Spin-dependent coefficients [lit: linear fits by Hörzer to Asai et al. 2007, valid ≈ 22–30 m/s; C_m for Sp > 0.1]:**
  $$C_d = 0.80\,Sp + 0.12,\qquad C_m = 0.77\,Sp + 0.12 \quad\text{(eqs. 7–8)}$$
  Hörzer states that Asai found C_d and C_m are more influenced by Sp than by Re in that speed range.
- **Spin decay (eq. 9):** $\omega = \omega_0\exp(-t\,v\cdot2\times10^{-5}/r)$, i.e. golf-ball-like k = 2×10⁻⁵ (from James & Haake's suggestion).
  This gives ≈ 0.5 % loss over a 20 m kick. **The authors themselves call this "questionable"**, because Goff & Carré (2009)
  proposed ≈ 10 % for a similar flight length.
- **Altitude:** ρ = ρ(p, T) for dry air via the barometric formula. The South African 2010 venues span
  ρ ≈ 1.04–1.29 kg/m³ (at 5 °C). For a 20 m, 25 m/s, 8.5 rev/s free kick, the entry point differs by **0.39 m vertically and
  0.87 m laterally** between venues.
- **Relevance:** (i) it directly supports **spin-raising drag**; (ii) it gives a speed-dependent spin-decay model; (iii) it shows that
  **air density is a first-order parameter for curling shots**, since both drag and Magnus scale with ρ.
- **Note (coordinator):** the paper prints A = 0.0039 m², which must be a typo for 0.039 m² (πR² with R = 0.111 m).

## 3. Asai et al. 2020: Measurements of the flight trajectory of a spinning soccer ball and the Magnus force
*Proceedings 49, 88 (ISEA 2020). doi:10.3390/proceedings2020049088. Open access (CC BY).*
- **Method:** real curve kicks over 23 m by two collegiate players (7 kicks each). A 24-camera VICON system at 100 Hz tracked the ball and
  its spin axis with surface markers. The side force came from $S = m\ddot x\cos\theta - m\ddot y\sin\theta$, assuming a vertical spin axis.
- **Trial 1:** v ≈ 18.8 → 14.7 m/s (−22 %) in 1 s. **Spin 5.8 → 5.7 rev/s (≈ 2 %) in 0.8 s.** Side force 2 N → 1 N.
  **C_s 0.27 → 0.24**. Lateral deflection > 0.7 m in 1 s. The curvature peaks mid-flight. The other trials behave the same way.
- **Free-flight C_s vs time-averaged Sp:** 0.21, 0.24, 0.29 at Sp = 0.18, 0.22, 0.34. Their comparison with the wind tunnel
  (Asai 2007): 0.20, 0.23, 0.24 at Sp = 0.14, 0.18, 0.23. **Free flight confirms the wind-tunnel C_L(S) within ≈ 0.03.**
- **Physics conclusion of the paper:** the side force falls during flight mainly because $v^2$ falls. The spin barely decays.
- **Spin-decay constant derived [ours]:** a 2 % loss in 0.8 s at a mean speed of ≈ 17 m/s gives τ ≈ 40–46 s and
  $k = r/(\tau U) \approx 1.4\times10^{-4}$. At 30 m/s: τ ≈ 26 s, so **≈ 1.5 % loss over our 0.39 s flight.** The precision is
  limited by the ±0.1 rev/s readout.

## Consolidated conclusions [ours]

### Spin decay, with model $d\omega/dt = -k\,\omega\,|v|/R$ (Smits & Smith form)
| Preset | k | τ at 30 m/s | Spin loss over 0.39 s | Source / status |
|---|---|---|---|---|
| `none` (default) | 0 | ∞ | 0 | constant spin |
| `golf_like` | 2×10⁻⁵ | 183 s | 0.2 % | Hörzer 2010 eq. 9 (the authors call it questionable) |
| `asai2020` | 1.4×10⁻⁴ | 26 s | 1.5 % | derived from Asai 2020 free flight (**best direct evidence**) |
| `goff_carre` | 5×10⁻⁴ | 7 s | 5.4 % | ≈ 10 % over ≈ 1 s at ≈ 20 m/s, Goff & Carré 2009 *as quoted by Hörzer* (second-hand) |
| `james_subcritical` | 2×10⁻³ | 1.8 s | 20 % | James & Haake 2008 Fig. 4, laminar regime: **upper bound only** |

**Verdict:** for a 0.4 s penalty, spin decay is a ≲ 2–5 % effect on ω. Because C_L(S) is concave, its effect on the Magnus
force is smaller still. Constant spin is an adequate default, and the switch quantifies the residual.

### Spin-dependent drag, with model $C_D = C_{D0} + k_s\,S$
| Source | Slope k_s | Range | Status |
|---|---|---|---|
| Hörzer 2010 (claimed fit to Asai 2007) | 0.80 | 22–30 m/s | **inconsistent with Asai's own Fig. 8** (gives 0.36 at S = 0.3, where the measured value is 0.29); not used |
| Kray 2014 Fig. 9, Re 4.62×10⁵ | ≈ 0.74 for S ≤ 0.1, saturating at ≈ 0.40 | 31 m/s | verified by the coordinator |
| Kray 2014 Fig. 9, Re 3.42×10⁵ | ≈ 0.6 | 23 m/s | verified by the coordinator |
| Asai 2007 Fig. 8 (Re 3.3–4.6×10⁵, five Re curves collapse) | ≈ 0.47 (C_D ≈ 0.15 + 0.47 S) | 22–30 m/s | **verified by the coordinator** |
| Carré 2005 | ≈ 0 | scale model, Re ≤ 2.1×10⁵ | notes |
| Bray & Kerwin 2003 | C_D 0.25–0.30 for spinning kicks vs ≈ 0.22 non-spinning | 18–28 m/s | notes; indirect support |

**Verdict:** three independent sources (Asai 2007, Kray 2014, and indirectly Bray & Kerwin 2003) support **spin raising drag, with k_s ≈ 0.45–0.75**.
At our S ≈ 0.1 that is ΔC_D ≈ +0.05–0.07. Only Carré's low-Re scale model shows no effect. Asai also finds C_D(S) to be independent of Re over
3.3–4.6×10⁵ (the curves collapse), which supports a C_D0 + k_s·S form in our regime.

### Asai 2007 Fig. 9: side-force (Magnus) coefficient in our Re range (verified by the coordinator, ±0.01)
| Re | S → C_s |
|---|---|
| 4.55×10⁵ | 0.045→0.03, 0.10→0.175, 0.14→0.205, 0.18→0.23, 0.23→0.24 |
| 4.25×10⁵ | 0.05→0.04, 0.10→0.22, 0.15→0.24, 0.20→0.27, 0.25→0.28 |
| 3.64×10⁵ | 0.05→0.145, 0.11→0.265, 0.17→0.235, 0.23→0.30, 0.29→0.295 |
| 3.34×10⁵ | 0.06→0.15, 0.12→0.25, 0.19→0.29, 0.25→0.305, 0.31→0.33 |

**Implication:** at low S, C_s *decreases* with Re in Asai's data. In Kray's data it *increases* (0.065 → 0.18 at S = 0.07 from
Re 3.42 → 4.62×10⁵). The Re trend at low spin is therefore **rig- and ball-specific, not a physical law**. See the Stage 3 design notes.

### Air density (new first-order parameter)
Hörzer shows ρ alone moves a curling free kick by up to 0.87 m laterally. Both the drag and the Magnus accelerations are ∝ ρ.
The problem gives no venue or temperature, so ρ must be either fixed by assumption (1.20 kg/m³, 20 °C at sea level) or given a prior
(e.g. 1.04–1.29 kg/m³). **Open question for the team.**
