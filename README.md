# UPC 2026 — Problem B: Predicting FIFA Penalty Trajectories

Physics-based model for the University Physics Competition 2026, Problem B.

## Problem
Origin at the penalty mark; goal in the plane x = 11 m, −3.66 < y < 3.66, 0 < z < 2.44 (metres).
At t = 0 the ball centre is at (0, 0, 0.11). Given the ball position at t = 0.05 s and t = 0.10 s,
predict the point at which the ball is most likely to enter the goal and estimate the uncertainty.

Test case: (1.50, 0.45, 0.44) at t = 0.05 s and (2.96, 0.86, 0.74) at t = 0.10 s.

## Approach
The model is developed in stages of increasing physical realism (gravity → drag → spin/Magnus →
uncertainty → advanced effects). Each stage is preserved and comparable. See `docs/roadmap.md`.

## Setup
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Repository layout
- `docs/` — research notes, analysis of the 2022 reference reports, roadmap
- `references/` — reference reports (PDFs are kept locally and not committed)
