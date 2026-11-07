# Stage comparison: competition test case

Observations: (1.50, 0.45, 0.44) m at 0.05 s and (2.96, 0.86, 0.74) m at 0.10 s; P₀ = (0, 0, 0.11) m exact; σ = 1 cm.
Entry point = ball-centre crossing of x = 11 m. The σ values cover measurement noise only, unless stated otherwise.

| Stage | Physics | \|v₀\| (m/s) | χ²/dof | t_goal (s) | Entry y (m) | Entry z (m) | σ_y, σ_z (m) | Outcome | Commit/tag |
|---|---|---|---|---|---|---|---|---|---|
| 1 | gravity | 31.66 | 6.5 / 3 | 0.371 | 3.217 | 1.957 | 0.035, 0.033 | clean entry | v0.1-gravity-baseline |
| 2 | gravity + drag (C_D = 0.22 fixed) | 32.19 | 2.38 / 3 | 0.390 | 3.217 | 1.914 | 0.035, 0.033 | clean entry | v0.2-aerodynamic-drag |
| 3 | + Magnus + spin drag (unconstrained LSQ) | 32.58 | 0.19 / 1 | 0.401 | 2.448 | 1.979 | not meaningful | clean entry | not released: implausible spin (15 rev/s) |
| 3 | profile, spin fixed at 2 / 5 / 10 rev/s | — | 0.83 / 0.39 / 0.27 | — | 2.831 / 2.600 / 2.451 | 1.961 / 1.984 / 1.991 | — | clean entry | spin must come from a prior (Stage 4) |

Stage 2 C_D switches (literature presets 0.15–0.255, logistic C_D(Re)): y unchanged; z from 1.906 to 1.928 m.
