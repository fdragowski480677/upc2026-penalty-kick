"""Write overleaf/results.tex: every number quoted in the paper, taken directly from the simulation code and its outputs.

Usage:  PYTHONPATH=src .venv/bin/python scripts/export_results_tex.py
The paper uses only these macros for simulation parameters and results, so the text always matches the code. Rerun after every
production run. \\resStatus states which model version the numbers come from.
"""
import json
from pathlib import Path

import numpy as np

from penalty.bayes import Priors, density_prior
from penalty.coefficients import SPIN_DECAY_K, SPIN_DRAG_SLOPES
from penalty.collision import FrameImpact
from penalty.constants import P0, SIGMA_OBS, TEST_CASE, Ball, Goal
from penalty.kick import KickSpinPrior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "overleaf" / "results.tex"
HEADLINE = "kick"   # spin prior quoted as the headline result (unsuffixed macros); chosen by the team: kick mechanics (Asai 2002 scaling)


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


def main():
    m = {}
    pr, b, g = Priors(), Ball(), Goal()
    # ---- simulation parameters (from the code) ----
    m["parMass"], m["parRadius"], m["parGoalX"] = fmt(b.mass, 2), fmt(b.radius, 2), fmt(g.x, 0)
    from penalty.constants import Air
    m["parRhoNominal"] = fmt(Air().density, 2)
    m["parMassLo"], m["parMassHi"] = fmt(pr.mass_bounds[0] * 1000, 0), fmt(pr.mass_bounds[1] * 1000, 0)
    m["parCircLo"], m["parCircHi"] = fmt(pr.circ_bounds[0] * 100, 0), fmt(pr.circ_bounds[1] * 100, 0)
    m["parCDmean"], m["parCDsd"] = fmt(pr.cd0_mean, 2), fmt(pr.cd0_sd, 2)
    m["parKs"], m["parKsKray"] = fmt(SPIN_DRAG_SLOPES["asai2007"], 2), fmt(SPIN_DRAG_SLOPES["kray2014"], 2)
    m["parSpinMedian"], m["parSpinSigmaLn"] = fmt(pr.spin_median_rev, 0), fmt(pr.spin_sigma_ln, 2)
    m["parSeamSd"] = fmt(pr.seam_sd, 2)
    m["parTlo"], m["parThi"] = fmt(pr.t_bounds[0], 0), fmt(pr.t_bounds[1], 0)
    rho = density_prior().samples
    m["parRhoLo"], m["parRhoHi"] = fmt(rho.min(), 2), fmt(rho.max(), 2)
    m["parRhoMedian"] = fmt(float(np.median(rho)), 2)
    m["parSigmaTrack"] = fmt(SIGMA_OBS * 100, 0)
    m["parSigmaRound"] = fmt(SIGMA_OBS / np.sqrt(12) * 1000, 1)
    m["parSpinDecayK"] = "1.4"  # ×10^-4, SPIN_DECAY_K['asai2020']
    assert abs(SPIN_DECAY_K["asai2020"] - 1.4e-4) < 1e-12
    imp = FrameImpact()
    m["parPostRadius"] = fmt(imp.post_radius * 1000, 0)
    kp = KickSpinPrior()
    med, lo, hi = kp.summary(32.6)
    m["parKickSpinMed"], m["parKickSpinLo"], m["parKickSpinHi"] = fmt(med, 1), fmt(lo, 1), fmt(hi, 1)
    m["obsA"] = ", ".join(fmt(v, 2) for v in TEST_CASE[0].position)
    m["obsB"] = ", ".join(fmt(v, 2) for v in TEST_CASE[1].position)
    # ---- results ----
    # Final unified model (results/final/) if present, else the Stage 4 posterior. For the final model every result macro is
    # written once per spin prior (suffix L = log-normal, K = kick mechanics) and once unsuffixed for the headline prior.
    status = []
    final = {nz: ROOT / "results" / "final" / f"summary_final_{nz}.json" for nz in ("rounding", "tracking")}
    use_final = all(f.exists() for f in final.values())
    sources = []
    for noise, key in (("rounding", "R"), ("tracking", "T")):
        if use_final:
            bsp = json.load(open(final[noise]))["by_spin_prior"]
            for sp, suf in (("lognormal", "L"), ("kick", "K")):
                sources.append((noise, key, suf, bsp[sp], sp))
            sources.append((noise, key, "", bsp[HEADLINE], HEADLINE))
        else:
            f = ROOT / "results" / "stage4" / f"summary_{noise}.json"
            if f.exists():
                sources.append((noise, key, "", json.load(open(f))["pooled"], "lognormal"))
    for noise, key0, suf, d, sp in sources:
        key = key0 + suf
        m[f"res{key}Ymode"], m[f"res{key}Zmode"] = fmt(d["mode_yz"][0]), fmt(d["mode_yz"][1])
        for ax in ("y", "z"):
            A = ax.upper()
            m[f"res{key}{A}lo"], m[f"res{key}{A}hi"] = fmt(d[ax]["p16"]), fmt(d[ax]["p84"])
            m[f"res{key}{A}lolo"], m[f"res{key}{A}hihi"] = fmt(d[ax]["p2.5"]), fmt(d[ax]["p97.5"])
        po = d["p_outcome"]
        m[f"res{key}Pclean"] = fmt(100 * po.get("clean entry", 0), 1)
        m[f"res{key}Pframe"] = fmt(100 * po.get("frame contact", 0), 1)
        m[f"res{key}Pmiss"] = fmt(100 * po.get("miss", 0), 1)
        m[f"res{key}SpinMed"] = fmt(d["spin_rev_s"]["median"], 1)
        if "wind_speed" in d:
            m[f"res{key}WindMed"] = fmt(d["wind_speed"]["median"], 1)
        if use_final:
            g = ROOT / "results" / "final" / f"goal_probability_{noise}_{sp}.json"
            if g.exists():
                m[f"res{key}Pgoal"] = fmt(100 * json.load(open(g))["p_goal"], 1)
        status.append(noise)
    for noise, key in (("tracking", "T"), ("rounding", "R")):
        f = ROOT / "results" / ("final" if use_final else "stage4") / f"coverage_{noise}.json"
        if f.exists():
            c = json.load(open(f))
            m[f"cov{key}sixtyeight"], m[f"cov{key}ninetyfive"] = fmt(100 * c["coverage68"], 0), fmt(100 * c["coverage95"], 0)
            m[f"cov{key}n"] = str(c["n_trials"])
    if not use_final:
        for noise, key in (("rounding", "R"), ("tracking", "T")):
            f = ROOT / "results" / "stage5" / f"goal_probability_{noise}.json"
            if f.exists():
                m[f"res{key}Pgoal"] = fmt(100 * json.load(open(f))["p_goal"], 1)
    m["resHeadlinePrior"] = {"lognormal": "log-normal", "kick": "kick-mechanics"}[HEADLINE] if use_final else "log-normal"
    m["resStatus"] = (f"final unified model (wind included), headline spin prior: {m['resHeadlinePrior']}" if use_final
                      else "Stage 4 posterior (no wind, log-normal spin prior); preliminary, final unified model pending")
    lines = ["% AUTO-GENERATED by scripts/export_results_tex.py. Do not edit by hand; rerun the script after each production run."]
    for k, v in m.items():
        lines.append(f"\\providecommand{{\\{k}}}{{}}\\renewcommand{{\\{k}}}{{{v}}}")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(m)} macros); status: {m['resStatus']}")


if __name__ == "__main__":
    main()
