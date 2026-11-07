# Values audit: every physical constant and coefficient in `src/penalty/`

Status: ✓ = checked by the coordinator against the original source (text, table or figure); (n) = from the cluster notes only;
⚠ = caveat. Last audit: Stage 3.

## Problem data and geometry
| Quantity | Code | Value | Source | Status |
|---|---|---|---|---|
| Initial centre | `constants.P0` | (0, 0, 0.11) m | problem statement | ✓ |
| Observations | `constants.TEST_CASE` | (1.50, 0.45, 0.44) @ 0.05 s; (2.96, 0.86, 0.74) @ 0.10 s | problem statement | ✓ |
| Noise | `SIGMA_OBS` | 1 cm per coordinate, independent | team decision | ✓ |
| Goal plane, half-width, height | `Goal` | 11, 3.66, 2.44 m | problem statement; IFAB Law 1 (inner edges) | ✓ |
| Post/bar width | `Goal.frame_width` | 0.12 m | IFAB Law 1 (maximum) | ✓ (the actual width may be smaller; this only affects frame/miss classification) |
| g | `constants.G` | 9.81 m/s² | standard | ✓ |

## Ball and air
| Quantity | Value | Source | Status |
|---|---|---|---|
| m | 0.43 kg | IFAB Law 2 (410–450 g); Ishii 2012 ball 432 g; Hörzer 0.43 kg | ✓ fixed (team decision) |
| R | 0.11 m (circumference 69.1 cm) | IFAB Law 2 (68–70 cm); Asai 2020 R = 0.11 m | ✓ fixed (team decision) |
| A = πR² | 0.0380 m² | Asai 2020 uses A = 0.038 m² | ✓ (Hörzer prints 0.0039 m², a typo) |
| ρ | 1.20 kg/m³ | standard air; Asai 2020 uses 1.2 | ✓ nominal; Stage 4 prior 1.10–1.29 |
| ν | 1.5×10⁻⁵ m²/s | consistent with Alam 2010's Re–speed mapping (130 km/h ↔ Re 5.37×10⁵ ⇒ ν = 1.48×10⁻⁵) | ✓ |

## Aerodynamic coefficients: definition conventions (critical for mixing sources)
| Item | Our code | Kray 2014 | Asai 2007 / 2020 | Alam 2010 | Status |
|---|---|---|---|---|---|
| Reference area | πR² | π/4·D² | A = 0.038 m² | projected area | ✓ identical |
| Dynamic pressure | ½ρv² | ½ρu∞² | ½ρU² | ½ρV² | ✓ |
| Spin parameter | S = R\|ω⊥\|/\|v\| | SP = ωD/(2u∞) | Sp = ωR/U | — | ✓ identical |
| Re | v·2R/ν | u∞D/ν, with D = 0.226 m (model) | — | — | ⚠ Kray's model is 2.7 % larger than our ball; at equal speed our Re is 2.7 % lower. Negligible against the curve-to-curve spread |
| Sign of lift | magnitude used, direction ω×v | C_M = −C_L (rig orientation) | side force | — | ✓ |

## Drag
| Setting | Value | Status |
|---|---|---|
| C_D0 default | 0.22 | ✓ centre of the modern-ball spread; Alam 0.227/0.233 ✓; Kray 0.255 ✓; Asai 0.15–0.20 (n) |
| Spin drag k_s | 0.47 (default), 0.74, 0 | ✓ Asai 2007 Fig. 8 (slope ≈ 0.47; Re-independent across 3.3–4.6×10⁵); ✓ Kray Fig. 9 (≈ 0.74 for S ≤ 0.1, saturating near 0.40) |
| Drag magnitude check | K·0.22·31.5² = 11.6 m/s² | ✓ unit test |

## Lift
| Setting | Status |
|---|---|
| Kray Re 4.62×10⁵ / 3.42×10⁵ curves | ✓ digitised by the coordinator (±0.005–0.01). ⚠ The measured range ends at **S = 0.23** (Re 4.62) and 0.31 (Re 3.42); beyond that our code holds the last value (0.285), while Kray reports a plateau of 0.30–0.35 |
| Asai 2007 Re 4.55 / 3.64×10⁵ curves | ✓ digitised (±0.01); ⚠ sting-mounted (support interference per Kray) |
| C_L(0) = 0 imposed | ✓ physical (the non-spinning lateral force is a seam/orientation effect, Stage 4 nuisance) |
| Free-flight cross-check | ✓ Asai 2020: C_s 0.21/0.24/0.29 at Sp 0.18/0.22/0.34; the tunnel curves agree within ≈ 0.03 |

## Spin decay
| Preset | k | Status |
|---|---|---|
| none (default) | 0 | — |
| asai2020 | 1.4×10⁻⁴ | ✓ derived from Asai 2020 (5.8 → 5.7 rev/s in 0.8 s); ±50 % (readout precision) |
| golf_like | 2×10⁻⁵ | ✓ Hörzer eq. 9 (the authors call it questionable) |
| goff_carre | 5×10⁻⁴ | ⚠ second-hand (Hörzer quoting Goff & Carré 2009; the paper is not in our folder) |
| james_subcritical | 2×10⁻³ | ✓ James & Haake Fig. 4; ⚠ laminar regime only, so an upper bound |

## Plausibility checks of *inferred* values (automated in `scripts/run_stage3.py`)
Launch speed 25–36 m/s; spin 2–8 rev/s (Asai 2007: real curve kicks ≤ 10 rev/s); C_L 0.15–0.30; C_D 0.20–0.32; speed loss 7–16 %;
flight time 0.33–0.45 s; S within the measured curve range. **The unconstrained Stage 3 least-squares fit fails four of these.** See
`docs/stages/stage3-magnus-effect.md`.
