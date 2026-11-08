# UPC 2026 — Problem B: Predicting FIFA Penalty Trajectories

A physics-based, Bayesian prediction of where a penalty kick enters the goal. It uses the ball position at three early instants and
gives a calibrated uncertainty estimate. Built for the University Physics Competition 2026, Problem B.

## Problem
Origin at the penalty mark; goal in the plane x = 11 m, −3.66 < y < 3.66, 0 < z < 2.44 (metres).
At t = 0 the ball centre is at (0, 0, 0.11). Given the ball position at t = 0.05 s and t = 0.10 s,
predict the point at which the ball is most likely to enter the goal and estimate the uncertainty.

Test case: (1.50, 0.45, 0.44) at t = 0.05 s and (2.96, 0.86, 0.74) at t = 0.10 s.

## Result (final model, kick-mechanics spin prior)
| | positions exact to their 1 cm rounding (main case) | 1 cm tracking noise |
|---|---|---|
| most probable entry point (y, z) | **(2.68, 1.96) m** | (3.17, 1.92) m |
| 68 % interval, y | [2.58, 2.80] m | [2.78, 3.30] m |
| 68 % interval, z | [1.83, 2.09] m | [1.68, 2.19] m |
| probability of a goal (incl. off the frame) | **99.9 %** | 93.4 % |

The credible regions are calibrated by blind simulation tests (53 trials for the main case: 68 % / 91 % coverage of the
68 % / 95 % regions). All numbers come from the files in `results/`.

## Physics, built in stages
| Stage | Adds | Key finding |
|---|---|---|
| 1 | gravity | analytic baseline |
| 2 | quadratic drag, measured C_D | in still air drag cannot curve the ball; it lowers it by 4 cm |
| 3 | Magnus lift from measured C_L(S, Re), spin-dependent drag, spin decay | the inviscid 16/3·S lift law overestimates curl ~4× |
| 4 | Bayesian inference (MCMC) over spin, drag, air density, ball, seams | spin is not identifiable from 0.1 s of flight |
| 5 | frame impacts (post/crossbar), kick-mechanics spin prior | centres within 7 cm inside the post rebound out |
| 6 | wind (final unified model) | wind adds uncertainty but shifts the answer by ~1 cm |

Each stage is preserved, tested and compared with the previous ones. See `docs/roadmap.md` and `docs/stages/`.

## Setup
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest            # 114 verification tests
```

## Reproducing the results
```bash
export PYTHONPATH=src
.venv/bin/python scripts/run_stage4.py --model final --noise rounding --nsteps 20000 --burn 5000   # posterior (≈30 min, 11 cores)
.venv/bin/python scripts/run_stage5.py --model final --spin-prior kick --noise rounding             # probability of a goal
.venv/bin/python scripts/goal_probability_map.py --noise rounding                                   # P(goal | crossing point)
.venv/bin/python scripts/validate_stage4_coverage.py --noise rounding --spin-prior kick --trials 16  # calibration test
.venv/bin/python scripts/benchmark_timing.py                                                        # time evaluation
.venv/bin/python scripts/make_figures.py                                                            # all report figures
```
Coverage batches can run on several machines in parallel (`--start`, `--tag`). `scripts/export_results_tex.py` writes every
number used in the report from `results/`.

## Repository layout
- `src/penalty/`: simulation package (forces, coefficients, integrators, Bayesian model, kick prior, frame impacts, climate)
- `tests/`: verification tests (analytic limits, literature reproductions, integrator equivalence)
- `scripts/`: stage runs, validation, figures, timing, report export
- `results/`: production summaries, goal probabilities, coverage tests, timing (raw MCMC chains are not committed)
- `docs/`: analysis of the 2022 reference reports, literature notes, roadmap, per-stage notes
- `references/`: reference literature (PDFs kept locally, not committed)
