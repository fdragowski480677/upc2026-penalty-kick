"""Find an 'in off the post' posterior trajectory for the example figure; saves results/raw/example_in_off_post.npz.

Usage:  PYTHONPATH=src .venv/bin/python scripts/find_example_trajectory.py [--noise tracking]
Scans near-frame samples of the pooled Stage 4 posterior and resolves them with the frame-impact model (nominal impact parameters)
until a 'goal off the frame' case with a post (not bar) impact is found. The no-frame counterfactual is saved too.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_stage5 import CURVES, FORCES, sample_params  # noqa: E402

from penalty.bayes import TWO_PI  # noqa: E402
from penalty.collision import GOAL_OFF_FRAME, FrameImpact, resolve  # noqa: E402
from penalty.constants import P0, Goal  # noqa: E402
from penalty.integrate import simulate  # noqa: E402
from penalty.outcome import distance_to_frame  # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--noise", default="tracking"); a = ap.parse_args()
    rng = np.random.default_rng(7)
    g = Goal()
    for c in CURVES:
        d = np.load(ROOT / "results" / "raw" / f"stage4_{a.noise}_{c}.npz")
        th, en = d["samples"], d["entries"]
        ok = np.all(np.isfinite(en), axis=1)
        near = [i for i in np.where(ok)[0] if distance_to_frame(en[i, 1], en[i, 2]) < th[i, 9] / TWO_PI + 0.03
                and 3.3 < abs(en[i, 1]) < g.half_width and en[i, 2] < 2.2]           # inside clips of a post
        for i in rng.permutation(near)[:400]:
            v0, ball, p = sample_params(th[i], c)
            out, info = resolve(P0, v0, FORCES, p, ball=ball, imp=FrameImpact(), record=True)
            fi = info["first_impact"]
            if out == GOAL_OFF_FRAME and fi and abs(fi["point"][1]) > 3.45 and fi["point"][2] < 2.2:   # a post, not the bar
                sol, cr = simulate(P0, v0, FORCES, p, ball=ball, goal=Goal(x=12.0))   # counterfactual: no frame
                # continue the real (post-impact) flight into the net for the figure, with the post-impact spin
                from dataclasses import replace as _r
                s = info["final_state"]
                sol2, c2 = simulate(s[:3], s[3:6], FORCES, _r(p, spin=info["spins"][-1]), ball=ball, goal=Goal(x=12.0))
                tail = sol2.sol(np.linspace(0, c2.t if c2 else sol2.t[-1], 60))[:3]
                path = np.hstack(info["path"] + [tail])
                np.savez(ROOT / "results" / "raw" / "example_in_off_post.npz", theta=th[i], curve=c, path=path,
                         impact=np.array(fi["point"]), vn=fi["vn"], spin_before=info["spins"][0], spin_after=info["spins"][1],
                         nofr=sol.sol(np.linspace(0, cr.t, 300))[:3], noise=a.noise)
                print(f"found ({c}, sample {i}): impact at {np.round(fi['point'], 3)}, v_n = {fi['vn']:.1f} m/s, "
                      f"spin {np.linalg.norm(info['spins'][0]) / TWO_PI:.1f} -> {np.linalg.norm(info['spins'][1]) / TWO_PI:.1f} rev/s")
                return
    print("no example found")


if __name__ == "__main__":
    main()
