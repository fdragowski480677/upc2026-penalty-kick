# Stage 2: aerodynamic drag

## What changes compared with Stage 1
One force is added; nothing else in the integrator or the inverse method changes:

$$\ddot{\vec r} = -g\hat z \;-\; \frac{\rho\, C_D(Re)\, \pi R^2}{2m}\,|\vec v|\,\vec v,\qquad Re = \frac{|\vec v|\,2R}{\nu}.$$

**Physical motivation [theory + lit]:** at 32 m/s the drag deceleration is ≈ 12 m/s², larger than g, so it cannot be neglected.
The quadratic form is valid because Re ≈ 4–5×10⁵, far above the Stokes regime. Still air is assumed (the problem gives no wind).
ρ = 1.20 kg/m³, ν = 1.5×10⁻⁵ m²/s, m = 0.43 kg, R = 0.11 m.

## C_D settings (tested switches, `src/penalty/coefficients.py`)
| Setting | Value | Use |
|---|---|---|
| `ConstantCD()` (**default**) | 0.22 | team decision: the nominal modern ball at 30–34 m/s |
| `ConstantCD.from_literature(name)` | 0.15–0.255 | per-ball supercritical values from Alam 2010, Kray 2014, Asai 2007, Carré 2005, Oggiano 2010. The verification status of each value is recorded in the code |
| `LogisticCD()` | C_D(Re), 0.45 → 0.21 through the crisis at Re_c = 1.8×10⁵ | speed-dependent model [ours, fitted to the literature]; evaluated at the instantaneous Re |

CLI: `scripts/run_stage2.py [--cd PRESET | --logistic]`.

## Verification (`tests/test_stage2_drag.py`, 16 tests; the full suite has 34, all passing)
- The drag magnitude equals $K C_D v^2$ (11.6 m/s² at 31.5 m/s), the force is antiparallel to v, and it is zero at rest.
- 1-D pure drag matches the analytic $x(t)=\ln(1+cv_0t)/c$ to < 1e-9 m. The terminal velocity in a vertical fall matches $\sqrt{g/KC_D}$.
- Mechanical energy decreases strictly along the trajectory. With C_D = 0 the result is identical to Stage 1.
- Presets load with sources; an unknown preset raises an error. The logistic model has the correct limits and is monotone; it
  is within 0.005 of C_sup over a penalty; and it gives more drag than C_sup for a slow shot that crosses the crisis (which
  proves it is evaluated along the trajectory).
- The fit recovers v₀ exactly from noise-free synthetic data for the constant, preset and logistic models.

## Result for the test case (default C_D = 0.22)
| Quantity | Stage 1 | **Stage 2** |
|---|---|---|
| \|v₀\| | 31.66 m/s | **32.19 m/s** (Re₀ = 4.7×10⁵) |
| χ² / dof | 6.5 / 3 (p = 0.09) | **2.38 / 3 (p = 0.50)** |
| Residuals at 0.05 s | (−1.6, −1.6, −0.2) cm | (−0.5, **−1.3**, 0.0) cm |
| Flight time | 0.371 s | **0.390 s**; speed at goal 27.6 m/s (Re 4.0×10⁵, still supercritical) |
| **Entry (y, z)** | (3.217, 1.957) m | **(3.217, 1.914) m ± (0.035, 0.033) m** (noise only) |
| Outcome | clean entry | clean entry |

### C_D sensitivity (all switches)
Entry y is unchanged (3.217 m) for every setting. Entry z varies from 1.906 m (Kray, 0.255) to 1.928 m (Asai Teamgeist, 0.15).
That is **−0.7 to +1.4 cm, less than half the noise σ.** The logistic model gives the same result as constant 0.21.

## Interpretation [ours]
1. **Drag cannot curve the ball sideways.** Drag ∥ v and gravity ∥ ẑ, so the horizontal velocity keeps its direction
   ($\dot{\vec v}_h \parallel \vec v_h$). The plan-view path is a straight line from P₀, and its direction is fixed by the data.
   So the lateral entry point is *identical* to Stage 1, to three decimals. **Any lateral curvature needs a force
   perpendicular to v: Magnus lift, seam side force, or wind. Stage 3 is therefore what decides y.**
2. **Drag makes the model consistent with the data** (p = 0.09 → 0.50). The leftover residual is mainly lateral, −1.3 cm at
   0.05 s, which is the pattern a sideways Magnus force would remove. It is still only ≈ 1–2σ, so the data favours spin
   but cannot prove it alone.
3. **The C_D uncertainty is a minor term in the budget** (≲ 1.5 cm in z), as the literature pass predicted. A fixed default
   with switchable presets is adequate. The speed-dependent model matters only for shots slower than about 20 m/s.
4. **Fitted launch speed:** 32.2 m/s, at the top of the human range but plausible for a hard strike (literature/kick-keeper.md).

## Reproduce
```bash
.venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python scripts/run_stage2.py
```
