"""Accuracy of the method by type of shot, from the blind trials of the final-model coverage test.

Usage:  PYTHONPATH=src .venv/bin/python scripts/accuracy_by_shot.py

Every coverage trial i drew its true penalty with the random seed 1000 + i (validate_stage4_coverage.py), so the full true parameter
vector (launch speed, spin, drag, air, ball, seams, wind) is regenerated exactly here. The regenerated true entry point is checked
against the stored one (to 1e-9 m) before a trial is used. For every trial: launch speed, spin, distance of the true crossing point
from the nearer post, height, and the error of the most probable point (lateral, vertical, total). The errors are summarised in bins
of each property, separately for the two noise models; the coverage of the 68 % region is given per bin as well.
Writes results/final/accuracy_by_shot.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_stage4_coverage import draw_truth  # noqa: E402

from penalty.bayes import TWO_PI, Priors, physics, unpack  # noqa: E402
from penalty.coefficients import LIFT_MODELS  # noqa: E402
from penalty.constants import P0  # noqa: E402
from penalty.fastsim import Settings, crossings  # noqa: E402

FILES = {("rounding", "lognormal"): ["coverage_rounding.json"], ("tracking", "lognormal"): ["coverage_tracking.json"],
         ("rounding", "kick"): ["coverage_rounding_kick_local.json", "coverage_rounding_kick_primus.json",
                                "coverage_rounding_kick_primus2.json"],
         ("tracking", "kick"): ["coverage_tracking_kick_local.json", "coverage_tracking_kick_primus.json"]}
BINS = {"speed": [28, 31, 33, 37], "spin": [0, 2.5, 5, 30], "post_dist": [-1, 0.3, 1.0, 5], "height": [0, 1.5, 2.2, 4]}


def main():
    st = Settings(LIFT_MODELS["kray2014_re462"])
    rows, bad = [], 0
    for (noise, sp), files in FILES.items():
        for f in files:
            p = ROOT / "results" / "final" / f
            if not p.exists():
                continue
            for t in json.load(open(p))["trials"]:
                th = draw_truth(np.random.default_rng(1000 + t["trial"]), Priors(spin_prior=sp))[None, :]
                e = crossings(P0, *unpack(th), st, **physics(th))[0]
                if not np.allclose(e[1:3], t["true_yz"], atol=1e-9):
                    bad += 1
                    continue
                dy, dz = t["mode_yz"][0] - t["true_yz"][0], t["mode_yz"][1] - t["true_yz"][1]
                rows.append({"noise": noise, "spin_prior": sp, "trial": t["trial"], "speed": float(np.linalg.norm(th[0, :3])),
                             "spin": float(np.hypot(th[0, 3], th[0, 4]) / TWO_PI), "post_dist": float(3.66 - abs(t["true_yz"][0])),
                             "height": float(t["true_yz"][1]), "dy": dy, "dz": dz, "err": float(np.hypot(dy, dz)), "in68": t["in68"],
                             "in95": t["in95"]})
    summary = {}
    for noise in ("rounding", "tracking"):
        R = [r for r in rows if r["noise"] == noise]
        summary[noise] = {"n": len(R), "median_abs_dy": float(np.median([abs(r["dy"]) for r in R])),
                          "rms_dy": float(np.sqrt(np.mean([r["dy"] ** 2 for r in R]))),
                          "rms_dz": float(np.sqrt(np.mean([r["dz"] ** 2 for r in R]))), "bins": {}}
        for key, edges in BINS.items():
            out = []
            for lo, hi in zip(edges[:-1], edges[1:]):
                B = [r for r in R if lo <= r[key] < hi]
                if B:
                    out.append({"lo": lo, "hi": hi, "n": len(B), "median_abs_dy": float(np.median([abs(r["dy"]) for r in B])),
                                "median_err": float(np.median([r["err"] for r in B])),
                                "rms_dy": float(np.sqrt(np.mean([r["dy"] ** 2 for r in B]))),
                                "cov68": float(np.mean([r["in68"] for r in B]))})
            summary[noise]["bins"][key] = out
    rep = {"n_trials": len(rows), "n_not_reproduced": bad, "summary": summary, "trials": rows}
    (ROOT / "results" / "final" / "accuracy_by_shot.json").write_text(json.dumps(rep, indent=1))
    print(f"{len(rows)} trials reproduced, {bad} not reproduced")
    for noise, s in summary.items():
        print(noise, {k: round(v, 3) for k, v in s.items() if k not in ("bins",)})
        for key, out in s["bins"].items():
            print("  ", key, [(b["lo"], b["hi"], b["n"], round(100 * b["median_abs_dy"], 1), round(100 * b["rms_dy"], 1),
                               round(b["cov68"], 2)) for b in out])


if __name__ == "__main__":
    main()
