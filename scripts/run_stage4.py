"""Stage 4: Bayesian posterior of the goal-entry point for the test case.

Usage:  PYTHONPATH=src .venv/bin/python scripts/run_stage4.py [--noise tracking|rounding] [--quick] [--procs N]
  tracking: σ = 1 cm Gaussian per coordinate (team decision: realistic tracking noise)
  rounding: the given values are exact up to their 2-decimal rounding: uniform ±5 mm, approximated by a Gaussian of
            equal variance, σ = 0.01/√12 = 2.89 mm
Outputs: results/stage4/summary_<noise>.json, results/figures/stage4_entry_posterior_<noise>.png,
raw chains in results/raw/ (git-ignored). Every chain runs in its own process.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import json
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from penalty.bayes import Priors, sample, summarise
from penalty.coefficients import LIFT_MODELS, SPIN_DECAY_K
from penalty.constants import TEST_CASE, Observation
from penalty.fastsim import Settings

ROOT = Path(__file__).resolve().parents[1]
NOMINAL_CURVES = ["kray2014_re462", "kray2014_re_interp", "asai2007_re455", "asai2007_re_interp"]
STAGE_POINTS = {"Stage 1 (gravity)": (3.217, 1.957), "Stage 2 (+ drag)": (3.217, 1.914)}


def derived(post, settings):
    th = post.samples
    v0 = np.linalg.norm(th[:, :3], axis=1)
    w = np.hypot(th[:, 3], th[:, 4])
    S = th[:, 9] / (2 * np.pi) * w / v0
    return {"spin_rev_s": w / (2 * np.pi), "S0": S, "CD_launch": th[:, 5] + settings.spin_drag_slope * S,
            "speed": v0, "rho": th[:, 6], "air_T_C": th[:, 7], "mass_kg": th[:, 8], "circumference_m": th[:, 9],
            "flight_time": post.entries[:, 0]}


def q(x):
    x = x[np.isfinite(x)]
    return {"median": float(np.median(x)), "p2.5": float(np.percentile(x, 2.5)), "p16": float(np.percentile(x, 16)),
            "p84": float(np.percentile(x, 84)), "p97.5": float(np.percentile(x, 97.5))}


def entry_report(entries):
    s = summarise(entries)
    return s, {"mode_yz": s.mode.round(4).tolist(), "mean_yz": s.mean.round(4).tolist(), "median_yz": s.median.round(4).tolist(),
               "sd_yz": s.sd.round(4).tolist(), "p_reach_goal_plane": s.p_reach, "p_outcome": s.p_outcome,
               "y": q(entries[:, 1]), "z": q(entries[:, 2])}


NOISE = {"tracking": 0.01, "rounding": 0.01 / np.sqrt(12)}


def run_case(label, settings, priors, kw, raw_dir, noise):
    t0 = time.perf_counter()
    obs = tuple(Observation(o.t, o.position, NOISE[noise]) for o in TEST_CASE)
    post = sample(settings, label, priors=priors, observations=obs, **kw)
    np.savez_compressed(raw_dir / f"stage4_{noise}_{label}.npz", samples=post.samples, entries=post.entries)
    steps_after_burn = kw["nsteps"] - kw["burn"]
    conv = {"acceptance": post.acceptance, "tau_max": float(np.nanmax(post.tau)),
            "steps_over_tau": float(steps_after_burn / np.nanmax(post.tau)), "n_samples": int(len(post.samples)),
            "runtime_s": round(time.perf_counter() - t0, 1)}
    print(f"  {label:28s} acc {conv['acceptance']:.2f}  tau_max {conv['tau_max']:.0f}  N/tau {conv['steps_over_tau']:.0f}  "
          f"{conv['runtime_s']:.0f} s", flush=True)
    return post, conv


def _job(args):
    label, st, p, kw, raw, noise = args
    post, conv = run_case(label, st, p, kw, raw, noise)
    return label, post, conv, st


def figure(entries, summary, path, noise):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle

    surface, ink, ink2, muted = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984"
    blues = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95"]
    cmap = LinearSegmentedColormap.from_list("seq_blue", blues)
    series = {"Stage 1 (gravity)": "#eb6834", "Stage 2 (+ drag)": "#1baf7a"}

    fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=200, facecolor=surface)
    ax.set_facecolor(surface)
    yy, zz = np.meshgrid(np.linspace(-0.5, 4.5, 400), np.linspace(0.0, 3.2, 260))
    dens = summary.kde(np.vstack((yy.ravel(), zz.ravel()))).reshape(yy.shape)
    lo95, lo68 = summary.levels[0.95], summary.levels[0.68]
    # fill only inside the 95 % region, so the surface stays neutral elsewhere
    ax.contourf(yy, zz, dens, levels=np.linspace(lo95, dens.max(), 9), cmap=cmap, zorder=1)
    ax.contour(yy, zz, dens, levels=[lo95], colors=[blues[5]], linewidths=2.0, linestyles="-", zorder=3)
    ax.contour(yy, zz, dens, levels=[lo68], colors=[ink], linewidths=2.0, linestyles="--", zorder=3)
    for x0 in (3.66, -3.78):
        ax.add_patch(Rectangle((x0, 0), 0.12, 2.56, color=ink2, zorder=4))
    ax.add_patch(Rectangle((-3.78, 2.44), 7.56, 0.12, color=ink2, zorder=4))
    m = summary.mode
    ax.plot(*m, marker="o", ms=9, color=ink, mec=surface, mew=2, zorder=6)
    ax.annotate(f"most probable entry\n(y, z) = ({m[0]:.2f}, {m[1]:.2f}) m", m, xytext=(0.0, 1.0), color=ink, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=ink2, lw=1), zorder=7)
    offsets = {"Stage 1 (gravity)": (3.95, 2.05), "Stage 2 (+ drag)": (3.95, 1.70)}
    for name, (y, z) in STAGE_POINTS.items():
        ax.plot(y, z, marker="D", ms=8, color=series[name], mec=surface, mew=2, zorder=5)
        ax.annotate(name, (y, z), xytext=offsets[name], color=ink, fontsize=8,
                    arrowprops=dict(arrowstyle="-", color=muted, lw=0.8), zorder=7)
    ax.set_xlim(-0.5, 4.9); ax.set_ylim(0, 3.2); ax.set_aspect("equal")
    ax.set_xlabel("y (m), lateral", color=ink2); ax.set_ylabel("z (m), height", color=ink2)
    for sp in ax.spines.values():
        sp.set_color(muted)
    ax.tick_params(colors=ink2)
    handles = [Line2D([], [], color=ink, lw=2, ls="--", label="68 % credible region"),
               Line2D([], [], color=blues[5], lw=2, label="95 % credible region"),
               Line2D([], [], marker="o", ls="", color=ink, ms=8, label="most probable (posterior mode)")]
    handles += [Line2D([], [], marker="D", ls="", color=c, ms=7, label=f"{k} point estimate") for k, c in series.items()]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8, labelcolor=ink)
    sig = {"tracking": "σ = 1 cm tracking noise", "rounding": "rounding only, σ = 2.9 mm"}[noise]
    ax.set_title(f"Posterior entry-point density on the goal plane (right half), Stage 4: {sig}", color=ink, fontsize=10, loc="left")
    fig.tight_layout()
    fig.savefig(path, facecolor=surface)
    plt.close(fig)


def replot(noise):
    raw = ROOT / "results" / "raw"
    pooled = np.concatenate([np.load(raw / f"stage4_{noise}_{c}.npz")["entries"] for c in NOMINAL_CURVES])
    figure(pooled, summarise(pooled), ROOT / "results" / "figures" / f"stage4_entry_posterior_{noise}.png", noise)


SPIN_PRIORS = ("lognormal", "kick")


def main_final(a, kw):
    """Final unified model (Stage 6: wind included). One chain per C_L curve for each spin prior, plus sensitivity cases."""
    raw = ROOT / "results" / "raw"; raw.mkdir(parents=True, exist_ok=True)
    out = ROOT / "results" / "final"; out.mkdir(parents=True, exist_ok=True)
    pr = Priors()                                          # wind_sd = 2.0 m/s
    base = Settings(LIFT_MODELS["kray2014_re462"])
    jobs = [(f"final_{sp}_{c}", Settings(LIFT_MODELS[c]), replace(pr, spin_prior=sp), kw, raw, a.noise)
            for sp in SPIN_PRIORS for c in NOMINAL_CURVES]
    sens = {"final_kick_no_wind": (base, replace(pr, spin_prior="kick", wind_sd=1e-6)),
            "final_kick_spin_decay": (replace(base, spin_decay_k=SPIN_DECAY_K["asai2020"]), replace(pr, spin_prior="kick")),
            "final_kick_rho_uniform": (base, replace(pr, spin_prior="kick", rho_prior="uniform"))}
    jobs += [(n, st, p, kw, raw, a.noise) for n, (st, p) in sens.items()]
    print(f"FINAL model, noise {a.noise} (sigma = {NOISE[a.noise] * 1000:.2f} mm); {len(jobs)} chains on {a.procs} processes", flush=True)
    with Pool(a.procs) as pool:
        results = {label: (post, conv, st) for label, post, conv, st in pool.imap_unordered(_job, jobs)}
    report = {"config": {"model": "final (Stage 6, wind)", "noise": a.noise, "sigma_obs_m": NOISE[a.noise], "chains": kw,
                         "priors": pr.__dict__, "nominal_curves": NOMINAL_CURVES}, "by_spin_prior": {}, "sensitivity": {}}
    for sp in SPIN_PRIORS:
        labels = [f"final_{sp}_{c}" for c in NOMINAL_CURVES]
        pooled = np.concatenate([results[l][0].entries for l in labels])
        _, rep = entry_report(pooled)
        rep["spin_rev_s"] = q(np.concatenate([derived(results[l][0], results[l][2])["spin_rev_s"] for l in labels]))
        wind = np.concatenate([np.hypot(results[l][0].samples[:, 12], results[l][0].samples[:, 13]) for l in labels])
        rep["wind_speed"] = q(wind)
        rep["convergence"] = {l: results[l][1] for l in labels}
        report["by_spin_prior"][sp] = rep
        print(f"  [{sp}] mode {rep['mode_yz']}  y68 [{rep['y']['p16']:.3f},{rep['y']['p84']:.3f}]  z68 [{rep['z']['p16']:.3f},"
              f"{rep['z']['p84']:.3f}]  outcomes {rep['p_outcome']}  spin median {rep['spin_rev_s']['median']:.2f}")
    for n in sens:
        post, conv, st = results[n]
        _, rep = entry_report(post.entries)
        report["sensitivity"][n] = {"convergence": conv, "entry": rep}
        print(f"  {n:26s} mode {rep['mode_yz']}  y68 [{rep['y']['p16']:.2f},{rep['y']['p84']:.2f}]  N/tau {conv['steps_over_tau']:.0f}")
    (out / f"summary_final_{a.noise}.json").write_text(json.dumps(report, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=("stage4", "final"), default="stage4")
    ap.add_argument("--quick", action="store_true", help="short chains for a smoke test")
    ap.add_argument("--noise", choices=sorted(NOISE), default="tracking")
    ap.add_argument("--procs", type=int, default=11)
    ap.add_argument("--nsteps", type=int, default=6000)
    ap.add_argument("--burn", type=int, default=2000)
    ap.add_argument("--replot", action="store_true", help="redraw the figure from saved chains only")
    a = ap.parse_args()
    if a.replot:
        replot(a.noise)
        return
    kw = (dict(nwalkers=64, nsteps=1200, burn=400, thin=10) if a.quick
          else dict(nwalkers=128, nsteps=a.nsteps, burn=a.burn, thin=max(10, a.nsteps // 300)))
    if a.model == "final":
        return main_final(a, kw)
    raw = ROOT / "results" / "raw"; raw.mkdir(parents=True, exist_ok=True)
    out = ROOT / "results" / "stage4"; out.mkdir(parents=True, exist_ok=True)
    figs = ROOT / "results" / "figures"; figs.mkdir(parents=True, exist_ok=True)
    pr = Priors()
    report = {"config": {"noise": a.noise, "sigma_obs_m": NOISE[a.noise], "chains": kw, "priors": pr.__dict__,
                         "nominal_curves": NOMINAL_CURVES, "spin_drag_slope": 0.47, "spin_decay_k": 0.0},
              "nominal": {}, "sensitivity": {}}
    base = Settings(LIFT_MODELS["kray2014_re462"])
    sens = {"spin_prior_loguniform_1_10": (base, replace(pr, spin_prior="loguniform")),
            "spin_drag_off": (replace(base, spin_drag_slope=0.0), pr),
            "spin_drag_kray_0.74": (replace(base, spin_drag_slope=0.74), pr),
            "spin_decay_asai2020": (replace(base, spin_decay_k=SPIN_DECAY_K["asai2020"]), pr),
            "no_seam_force": (base, replace(pr, seam_sd=1e-6)),
            "rho_uniform_1.10_1.29": (base, replace(pr, rho_prior="uniform")),
            "ball_fixed_0.43kg_0.11m": (base, replace(pr, ball_prior="fixed")),
            "lift_limit_linear": (Settings(LIFT_MODELS["limit_linear"]), pr),
            "lift_limit_saturated": (Settings(LIFT_MODELS["limit_saturated"]), pr)}
    jobs = [(c, Settings(LIFT_MODELS[c]), pr, kw, raw, a.noise) for c in NOMINAL_CURVES]
    jobs += [(n, st, p, kw, raw, a.noise) for n, (st, p) in sens.items()]
    print(f"Noise model: {a.noise} (sigma = {NOISE[a.noise] * 1000:.2f} mm); {len(jobs)} chains on {a.procs} processes", flush=True)
    with Pool(a.procs) as pool:
        results = {label: (post, conv, st) for label, post, conv, st in pool.imap_unordered(_job, jobs)}

    for c in NOMINAL_CURVES:
        post, conv, st = results[c]
        _, rep = entry_report(post.entries)
        report["nominal"][c] = {"convergence": conv, "entry": rep, **{k: q(v) for k, v in derived(post, st).items()}}
    pooled_post = [results[c][0] for c in NOMINAL_CURVES]
    pooled = np.concatenate([p.entries for p in pooled_post])
    summ, rep = entry_report(pooled)
    report["pooled"] = rep
    report["pooled"]["spin_rev_s"] = q(np.concatenate([derived(results[c][0], results[c][2])["spin_rev_s"] for c in NOMINAL_CURVES]))
    figure(pooled, summ, figs / f"stage4_entry_posterior_{a.noise}.png", a.noise)
    for n in sens:
        post, conv, st = results[n]
        _, rep = entry_report(post.entries)
        report["sensitivity"][n] = {"convergence": conv, "entry": rep, "spin_rev_s": q(derived(post, st)["spin_rev_s"])}

    (out / f"summary_{a.noise}{'_quick' if a.quick else ''}.json").write_text(json.dumps(report, indent=2))
    r = report["pooled"]
    print(f"\nPooled: most probable entry (y, z) = {r['mode_yz']} m; mean {r['mean_yz']}; sd {r['sd_yz']}")
    print(f"        y 68 % [{r['y']['p16']:.3f}, {r['y']['p84']:.3f}], 95 % [{r['y']['p2.5']:.3f}, {r['y']['p97.5']:.3f}]")
    print(f"        z 68 % [{r['z']['p16']:.3f}, {r['z']['p84']:.3f}], 95 % [{r['z']['p2.5']:.3f}, {r['z']['p97.5']:.3f}]")
    print(f"        outcomes {r['p_outcome']}; spin {r['spin_rev_s']}")
    for n, v in report["sensitivity"].items():
        e = v["entry"]
        print(f"  {n:28s} mode {e['mode_yz']}  y68 [{e['y']['p16']:.2f},{e['y']['p84']:.2f}]  z68 [{e['z']['p16']:.2f},{e['z']['p84']:.2f}]  "
              f"clean {e['p_outcome'].get('clean entry', 0):.2f}  N/tau {v['convergence']['steps_over_tau']:.0f}")


if __name__ == "__main__":
    main()
