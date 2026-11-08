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


def entry_macros(m, pre, d):
    """Entry-point summary (most probable point, 68 % / 95 % intervals, outcome fractions, spin, wind) of one posterior."""
    keys = ["Ymode", "Zmode", "Ylo", "Yhi", "Ylolo", "Yhihi", "Zlo", "Zhi", "Zlolo", "Zhihi", "Pclean", "Pframe", "Pmiss",
            "SpinMed", "SpinLo", "SpinHi", "WindMed"]
    if d is None:
        m.update({pre + k: "" for k in keys}); return
    m[f"{pre}Ymode"], m[f"{pre}Zmode"] = fmt(d["mode_yz"][0]), fmt(d["mode_yz"][1])
    for ax in ("y", "z"):
        A = ax.upper()
        m[f"{pre}{A}lo"], m[f"{pre}{A}hi"] = fmt(d[ax]["p16"]), fmt(d[ax]["p84"])
        m[f"{pre}{A}lolo"], m[f"{pre}{A}hihi"] = fmt(d[ax]["p2.5"]), fmt(d[ax]["p97.5"])
    po = d["p_outcome"]
    m[f"{pre}Pclean"] = fmt(100 * po.get("clean entry", 0), 1)
    m[f"{pre}Pframe"] = fmt(100 * po.get("frame contact", 0), 1)
    m[f"{pre}Pmiss"] = fmt(100 * po.get("miss", 0), 1)
    if "spin_rev_s" in d:
        sp = d["spin_rev_s"]
        m[f"{pre}SpinMed"], m[f"{pre}SpinLo"], m[f"{pre}SpinHi"] = fmt(sp["median"], 1), fmt(sp["p16"], 1), fmt(sp["p84"], 1)
    if "wind_speed" in d:
        m[f"{pre}WindMed"] = fmt(d["wind_speed"]["median"], 1)


def goal_macros(m, pre, g):
    """Goal probability including frame impacts (run_stage5.py)."""
    keys = ["Pgoal", "PgoalSe", "Pnear", "PinOff", "PoutOff"]
    if g is None:
        m.update({pre + k: "" for k in keys}); return
    no = g["near_frame_outcomes"]
    m[f"{pre}Pgoal"], m[f"{pre}PgoalSe"] = fmt(100 * g["p_goal"], 1), fmt(100 * g["p_goal_mc_se"], 2)
    m[f"{pre}Pnear"] = fmt(100 * g["p_near_frame"], 1)
    m[f"{pre}PinOff"] = fmt(100 * no.get("goal off the frame", 0), 0)
    m[f"{pre}PoutOff"] = fmt(100 * no.get("miss off the frame", 0), 0)


def cov_macros(m, pre, c):
    """Simulation-based coverage of the 68 % / 95 % credible regions."""
    if c is None:
        m.update({pre + k: "" for k in ("sixtyeight", "ninetyfive", "n")}); return
    m[f"{pre}sixtyeight"], m[f"{pre}ninetyfive"] = fmt(100 * c["coverage68"], 0), fmt(100 * c["coverage95"], 0)
    m[f"{pre}n"] = str(c["n_trials"])


def merged_coverage(noise, prior):
    """Merge all coverage batches of one spin prior (files coverage_<noise>_<prior>[_tag].json), checking for repeated trials."""
    rows = []
    for f in sorted((ROOT / "results" / "final").glob(f"coverage_{noise}_{prior}*.json")):
        rows += json.load(open(f))["trials"]
    if not rows:
        return None
    ids = [r["trial"] for r in rows]
    assert len(ids) == len(set(ids)), f"repeated coverage trials in {noise}/{prior}"
    n = len(rows)
    return {"n_trials": n, "coverage68": sum(r["in68"] for r in rows) / n, "coverage95": sum(r["in95"] for r in rows) / n,
            "trials": rows}


SENS_LABELS = {
    "spin_prior_loguniform_1_10": "spin prior log-uniform 1--10 rev/s",
    "spin_drag_off": "no spin-dependent drag ($k_s=0$)",
    "spin_drag_kray_0.74": "spin-drag slope $k_s=0.74$ (Kray)",
    "spin_decay_asai2020": "spin decay on (Asai 2020)",
    "no_seam_force": "no seam side force",
    "rho_uniform_1.10_1.29": "$\\rho\\sim\\mathcal U(1.10,1.29)$ instead of venues",
    "ball_fixed_0.43kg_0.11m": "ball fixed (0.43 kg, 0.11 m)",
    "lift_limit_linear": "$C_L$ limit: linear (upper bound)",
    "lift_limit_saturated": "$C_L$ limit: saturated (lower bound)",
    "kray2014_re_interp": "$C_L$: Kray 2014, interpolated in $Re$",
    "asai2007_re455": "$C_L$: Asai 2007, $Re=4.6\\times10^5$",
    "asai2007_re_interp": "$C_L$: Asai 2007, interpolated in $Re$",
    "final_kick_no_wind": "no wind",
    "final_kick_spin_decay": "spin decay on (Asai 2020)",
    "final_kick_rho_uniform": "$\\rho\\sim\\mathcal U(1.10,1.29)$ instead of venues",
}


def _sens_rows(base, cases):
    """Shift of the median entry point (cm) and the 68 % half-widths (cm) of each case against its single-curve baseline."""
    rows = []
    for lab, e in cases:
        dy = 100 * (e["median_yz"][0] - base["median_yz"][0]); dz = 100 * (e["median_yz"][1] - base["median_yz"][1])
        wy = 50 * (e["y"]["p84"] - e["y"]["p16"]); wz = 50 * (e["z"]["p84"] - e["z"]["p16"])
        rows.append((lab, dy, dz, wy, wz))
    return rows


def write_sensitivity_tables():
    """overleaf/tab_sensitivity_stage4.tex and tab_sensitivity_final.tex (rounding and tracking noise side by side)."""
    out = {}
    s4 = {nz: ROOT / "results" / "stage4" / f"summary_{nz}.json" for nz in ("rounding", "tracking")}
    if all(f.exists() for f in s4.values()):
        rr = {}
        for nz, f in s4.items():
            d = json.load(open(f))
            base = d["nominal"]["kray2014_re462"]["entry"]
            rr[nz] = [("baseline: Kray 2014 $C_L$, $Re=4.6\\times10^5$", 0.0, 0.0, 50 * (base["y"]["p84"] - base["y"]["p16"]),
                       50 * (base["z"]["p84"] - base["z"]["p16"]))]
            rr[nz] += _sens_rows(base, [(SENS_LABELS[k], v["entry"]) for k, v in d["sensitivity"].items()])
            rr[nz] += _sens_rows(base, [(SENS_LABELS[k], v["entry"]) for k, v in d["nominal"].items()
                                        if k != "kray2014_re462"])
        out["stage4"] = rr
    fin = {nz: ROOT / "results" / "final" / f"summary_final_{nz}.json" for nz in ("rounding", "tracking")}
    if all(f.exists() for f in fin.values()):
        rr = {}
        for nz, f in fin.items():
            d = json.load(open(f))
            base = _entry_of_npz(ROOT / "results" / "raw" / f"stage4_{nz}_final_kick_kray2014_re462.npz")
            rr[nz] = [("baseline: final model, kick prior, Kray 2014 $C_L$", 0.0, 0.0, 50 * (base["y"]["p84"] - base["y"]["p16"]),
                       50 * (base["z"]["p84"] - base["z"]["p16"]))]
            rr[nz] += _sens_rows(base, [(SENS_LABELS[k], v["entry"]) for k, v in d["sensitivity"].items()])
            lg = _entry_of_npz(ROOT / "results" / "raw" / f"stage4_{nz}_final_lognormal_kray2014_re462.npz")
            rr[nz] += _sens_rows(base, [("log-normal spin prior instead of kick", lg)])
        out["final"] = rr
    for name, rr in out.items():
        lines = ["% AUTO-GENERATED by scripts/export_results_tex.py",
                 "\\begin{tabular}{@{}lrrrrrrrr@{}}\\toprule",
                 " & \\multicolumn{4}{c}{rounding, $\\sigma=\\SI{2.9}{mm}$} & \\multicolumn{4}{c}{tracking, $\\sigma=\\SI{1}{cm}$}\\\\",
                 "\\cmidrule(lr){2-5}\\cmidrule(l){6-9}",
                 "Case & $\\Delta y$ & $\\Delta z$ & $\\delta y_{68}$ & $\\delta z_{68}$ & $\\Delta y$ & $\\Delta z$ & $\\delta y_{68}$ & $\\delta z_{68}$\\\\\\midrule"]
        for (lab, *a), (_, *b) in zip(rr["rounding"], rr["tracking"]):
            lines.append(lab + " & " + " & ".join(f"{x:+.1f}" if i < 2 else f"{x:.1f}" for i, x in enumerate(a)) + " & "
                         + " & ".join(f"{x:+.1f}" if i < 2 else f"{x:.1f}" for i, x in enumerate(b)) + "\\\\")
            if lab.startswith("baseline"):
                lines.append("\\midrule")
        lines.append("\\bottomrule\\end{tabular}")
        (ROOT / "overleaf" / f"tab_sensitivity_{name}.tex").write_text("\n".join(lines) + "\n")
        print("wrote", ROOT / "overleaf" / f"tab_sensitivity_{name}.tex")


def _entry_of_npz(path):
    e = np.load(path)["entries"]
    e = e[np.all(np.isfinite(e), axis=1)]
    q = lambda x: {"p16": float(np.percentile(x, 16)), "p84": float(np.percentile(x, 84))}
    return {"median_yz": [float(np.median(e[:, 1])), float(np.median(e[:, 2]))], "y": q(e[:, 1]), "z": q(e[:, 2])}


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
    # Stage 4 (no wind, log-normal spin prior): macros \\sfour<R|T>...; Stage 5 goal probability on the Stage 4 chains: \\sfive...;
    # final unified model (Stage 6, wind): \\res<R|T><K|L|> (K = kick-mechanics prior, L = log-normal, unsuffixed = headline prior).
    # Final-model macros that do not exist yet are written as \\TBD{running} so the paper always compiles.
    for noise, key in (("rounding", "R"), ("tracking", "T")):
        f = ROOT / "results" / "stage4" / f"summary_{noise}.json"
        if f.exists():
            d4 = json.load(open(f))
            entry_macros(m, f"sfour{key}", d4["pooled"])
            m[f"sfour{key}NtauMin"] = fmt(min(v["convergence"]["steps_over_tau"] for v in d4["nominal"].values()), 0)
        c = ROOT / "results" / "stage4" / f"coverage_{noise}.json"
        if c.exists():
            cov_macros(m, f"sfourcov{key}", json.load(open(c)))
        g = ROOT / "results" / "stage5" / f"goal_probability_{noise}.json"
        if g.exists():
            goal_macros(m, f"sfive{key}", json.load(open(g)))
    for key in ("R", "T"):   # Stage 5 goal probability still computing -> placeholder
        for t in ("Pgoal", "PgoalSe", "Pnear", "PinOff", "PoutOff"):
            m.setdefault(f"sfive{key}{t}", "\\TBD{running}")
    final = {nz: ROOT / "results" / "final" / f"summary_final_{nz}.json" for nz in ("rounding", "tracking")}
    use_final = all(f.exists() for f in final.values())
    template = {}
    entry_macros(template, "x", None); goal_macros(template, "x", None)
    for noise, key in (("rounding", "R"), ("tracking", "T")):
        bsp = json.load(open(final[noise]))["by_spin_prior"] if final[noise].exists() else {}
        for sp, suf in (("lognormal", "L"), ("kick", "K"), (HEADLINE, "")):
            pre = f"res{key}{suf}"
            if sp in bsp:
                entry_macros(m, pre, bsp[sp])
                m[f"{pre}NtauMin"] = fmt(min(v["steps_over_tau"] for v in bsp[sp]["convergence"].values()), 0)
            g = ROOT / "results" / "final" / f"goal_probability_{noise}_{sp}.json"
            if g.exists():
                goal_macros(m, pre, json.load(open(g)))
        c = ROOT / "results" / "final" / f"coverage_{noise}.json"
        if c.exists():
            cov_macros(m, f"cov{key}", json.load(open(c)))                 # log-normal spin prior (final model)
        kb = merged_coverage(noise, "kick")                                   # kick prior: all batches merged
        if kb:
            cov_macros(m, f"cov{key}K", kb)
        for t in ("sixtyeight", "ninetyfive", "n"):
            m.setdefault(f"cov{key}K{t}", "\\TBD{running}")
        # Stage 5 model = kick-mechanics prior + frame impacts, no wind (sensitivity chain final_kick_no_wind, Kray C_L curve)
        if final[noise].exists():
            entry_macros(m, f"sfiveE{key}", json.load(open(final[noise]))["sensitivity"]["final_kick_no_wind"]["entry"])
        for t in template:
            if t[1:] in ("Ymode", "Zmode", "Ylo", "Yhi", "Zlo", "Zhi", "Ylolo", "Yhihi", "Zlolo", "Zhihi"):
                m.setdefault(f"sfiveE{key}" + t[1:], "\\TBD{running}")
        for suf in ("L", "K", ""):
            for t in list(template) + ["xNtauMin"]:
                m.setdefault(f"res{key}{suf}" + t[1:], "\\TBD{running}")
        for t in ("sixtyeight", "ninetyfive", "n"):
            m.setdefault(f"cov{key}{t}", "\\TBD{running}")
    # Stage 5 goal probability (kick prior, no wind, Kray curve; run_stage5.py --chain no_wind) and the extra columns of the staged
    # table (scripts/staged_table_extras.py): launch speed, flight time and chi^2 (sigma = 1 cm) of the Bayesian stages, Stage 3 refits.
    g5 = ROOT / "results" / "final" / "goal_probability_rounding_kick_no_wind.json"
    if g5.exists():
        pg = 100 * json.load(open(g5))["p_goal"]
        m["sfiveERPgoal"] = "$>99.9$" if pg > 99.95 else fmt(pg, 1)      # 99.96 would round to a misleading 100.0
    ex = ROOT / "results" / "final" / "staged_extras_rounding.json"
    if ex.exists():
        e = json.load(open(ex))
        for st, name in (("stage4", "Four"), ("stage5", "Five"), ("stage6", "Six")):
            d = e[st]
            lo, med, hi = d["speed"]                       # stored as the 16 / 50 / 84 % quantiles
            m[f"tab{name}V"], m[f"tab{name}Vlo"], m[f"tab{name}Vhi"] = fmt(med, 2), fmt(lo, 2), fmt(hi, 2)
            lo, med, hi = d["t_goal"]
            m[f"tab{name}T"], m[f"tab{name}Tlo"], m[f"tab{name}Thi"] = fmt(med, 3), fmt(lo, 3), fmt(hi, 3)
            m[f"tab{name}Chimin"], m[f"tab{name}Chimed"] = fmt(d["chi2_min"], 3), fmt(d["chi2_median"], 2)
        for rev, name in (("2", "Two"), ("5", "Five"), ("10", "Ten")):
            m[f"tabThreeV{name}"] = fmt(e["stage3"][rev]["speed"], 2)
            m[f"tabThreeT{name}"] = fmt(e["stage3"][rev]["t_goal"], 3)
    for k in ["sfiveERPgoal"] + [f"tab{n}{f}" for n in ("Four", "Five", "Six") for f in ("V", "Vlo", "Vhi", "T", "Tlo", "Thi", "Chimin", "Chimed")] \
            + [f"tabThree{f}{n}" for f in ("V", "T") for n in ("Two", "Five", "Ten")]:
        m.setdefault(k, "\\TBD{running}")
    m["resHeadlinePrior"] = {"lognormal": "log-normal", "kick": "kick-mechanics"}[HEADLINE]
    m["resStatus"] = ("final unified model (wind included)" if use_final else
                      "final unified model still running; final-model numbers marked TBD")
    write_sensitivity_tables()
    lines = ["% AUTO-GENERATED by scripts/export_results_tex.py. Do not edit by hand; rerun the script after each production run."]
    for k, v in m.items():
        lines.append(f"\\providecommand{{\\{k}}}{{}}\\renewcommand{{\\{k}}}{{{v}}}")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(m)} macros); status: {m['resStatus']}")


if __name__ == "__main__":
    main()
