"""Aerodynamic coefficient models (Stage 2: drag only).

A drag model is any object with a method ``cd(re) -> float``. Three switchable options:

* ``ConstantCD(0.22)`` is the **default** (team decision). It is the nominal non-spinning value for a modern ball
  at 30–34 m/s [lit: Alam 2010; Carré 2005; Asai 2007; see docs/research/literature/README.md].
* ``ConstantCD.from_literature(name)`` gives a ball-specific supercritical value from ``LITERATURE_CD``.
* ``LogisticCD()`` gives a speed-dependent C_D(Re) through the drag crisis [ours, fitted to the literature, drag.md §10].
  For a penalty the ball is supercritical throughout the flight, so this changes the result very little. It is included
  for completeness and for slower shots.

The spin dependence of C_D is deferred to Stage 3 (it needs the spin parameter).
"""
from dataclasses import dataclass

import numpy as np

#: Supercritical, non-spinning C_D at about 30–34 m/s (Re ≈ 4.5–5×10⁵), by ball and source.
#: "verified" = re-read from the original figure by the coordinator; "notes" = taken from the cluster notes (figure-read
#: by a reader agent, ±0.01–0.02); "extrap" = extrapolated from data ending at 26 m/s.
LITERATURE_CD = {
    "nominal":               (0.22,  "team default; centre of modern-ball spread (literature/README.md)"),
    "alam2010_adidas14":     (0.227, "Alam et al. 2010, Fig. 5, 14-panel Adidas, 110-120 km/h [verified]"),
    "alam2010_nike32":       (0.233, "Alam et al. 2010, Fig. 5, 32-panel Nike, 110-120 km/h [verified]"),
    "kray2014_14panel":      (0.255, "Kray et al. 2014, Fig. 9, textured 14-panel model, S = 0, Re 4.62e5 [verified]"),
    "asai2007_teamgeist":    (0.15,  "Asai et al. 2007, Fig. 4, Teamgeist 2006 [notes]"),
    "asai2007_roteiro":      (0.15,  "Asai et al. 2007, Fig. 4, Roteiro 2004 [notes]"),
    "asai2007_fevernova":    (0.195, "Asai et al. 2007, Fig. 4, Fevernova 2002 [notes]"),
    "carre2005_minifevernova": (0.24, "Carre et al. 2005, Fig. 3, 140 mm Fevernova [notes]"),
    "oggiano2010_terrapass": (0.20,  "Oggiano & Saetran 2010, Fig. 2, Adidas Terrapass [notes, extrap]"),
    "oggiano2010_t90":       (0.19,  "Oggiano & Saetran 2010, Fig. 2, Nike T90 Omni [notes, extrap]"),
    "oggiano2010_puma":      (0.21,  "Oggiano & Saetran 2010, Fig. 2, Puma v1.08 [notes, extrap]"),
    "goff2018_telstar18":    (0.20,  "Goff, Hong & Asai 2018, Figs 5-6, Telstar 18 (6 panels), 28-35 m/s [verified]"),
    "goff2018_brazuca":      (0.195, "Goff, Hong & Asai 2018, Figs 5-6, Brazuca (6 panels), 28-35 m/s [verified]"),
    "hong2014_teamgeist2":   (0.22,  "Hong & Asai 2014, Fig. 3d, Teamgeist 2, Re 4.5-5e5 [verified]"),
    "hong2014_jabulani":     (0.155, "Hong & Asai 2014, Fig. 3c, Jabulani, Re 4.5-5e5 [verified]"),
}


@dataclass(frozen=True)
class ConstantCD:
    value: float = 0.22
    label: str = "nominal"

    def cd(self, re):
        return self.value

    @classmethod
    def from_literature(cls, name):
        try:
            value, _ = LITERATURE_CD[name]
        except KeyError:
            raise KeyError(f"unknown C_D preset {name!r}; choose from {sorted(LITERATURE_CD)}") from None
        return cls(value, name)


@dataclass(frozen=True)
class LogisticCD:
    """C_D(Re) = C_sup + (C_sub − C_sup) / (1 + (Re/Re_c)^n): a smooth drag crisis.

    Central values from drag.md §10 (ranges: C_sub 0.38–0.53, C_sup 0.15–0.25, Re_c 1.2–3.0×10⁵, n 4–15).
    """
    c_sub: float = 0.45
    c_sup: float = 0.21
    re_c: float = 1.8e5
    n: float = 8.0
    label: str = "logistic"

    def cd(self, re):
        return self.c_sup + (self.c_sub - self.c_sup) / (1.0 + (re / self.re_c) ** self.n)


# ================================================================================================================
# Lift (Magnus) coefficient models, Stage 3.  Interface: cl(S, re, speed) -> float, with S = R|ω⊥|/|v| ≥ 0.
# See docs/stages/stage3-design.md for the physics discussion of the choice.
# ================================================================================================================

#: Digitised C_L(S) curves (coordinator readings of the original figures, ±0.005–0.01). C_L(0) = 0 is imposed
#: (no lift without spin; the small non-zero values at S = 0 are seam/orientation effects, handled as a separate
#: nuisance term in Stage 4). Beyond the last point, C_L is held at the last measured value (plateau; Kray p. 52: 0.30–0.35).
CL_CURVES = {
    "kray2014_re462": (4.62e5, np.array([[0.0, 0.0], [0.026, 0.11], [0.052, 0.15], [0.079, 0.185], [0.107, 0.22],
                                         [0.13, 0.24], [0.155, 0.255], [0.18, 0.27], [0.205, 0.275], [0.23, 0.285]]),
                       "Kray et al. 2014, Fig. 9, Re 4.62e5 [verified]"),
    "kray2014_re342": (3.42e5, np.array([[0.0, 0.0], [0.036, 0.005], [0.072, 0.065], [0.107, 0.15], [0.143, 0.20],
                                         [0.18, 0.232], [0.215, 0.237], [0.248, 0.272], [0.281, 0.287], [0.314, 0.297]]),
                       "Kray et al. 2014, Fig. 9, Re 3.42e5 [verified]"),
    "asai2007_re455": (4.55e5, np.array([[0.0, 0.0], [0.045, 0.03], [0.10, 0.175], [0.14, 0.205], [0.18, 0.23],
                                         [0.23, 0.24]]),
                       "Asai et al. 2007, Fig. 9, Re 4.55e5 [verified]"),
    "asai2007_re364": (3.64e5, np.array([[0.0, 0.0], [0.05, 0.145], [0.11, 0.265], [0.17, 0.235], [0.23, 0.30],
                                         [0.29, 0.295]]),
                       "Asai et al. 2007, Fig. 9, Re 3.64e5 [verified]"),
}


@dataclass(frozen=True)
class TabulatedCL:
    """Measured C_L(S) at a single Re (piecewise-linear interpolation, plateau beyond the data). **Default: Kray Re 4.62e5.**"""
    curve: str = "kray2014_re462"
    label: str = "kray2014_re462"

    def cl(self, s, re=None, speed=None):
        pts = CL_CURVES[self.curve][1]
        return float(np.interp(s, pts[:, 0], pts[:, 1]))


@dataclass(frozen=True)
class ReInterpCL:
    """Linear interpolation in Re between two measured curves (clamped outside). An empirical choice, not a physical law."""
    low: str = "kray2014_re342"
    high: str = "kray2014_re462"
    label: str = "kray2014_re_interp"

    def cl(self, s, re, speed=None):
        re_lo, re_hi = CL_CURVES[self.low][0], CL_CURVES[self.high][0]
        w = min(max((re - re_lo) / (re_hi - re_lo), 0.0), 1.0)
        return (1 - w) * TabulatedCL(self.low).cl(s) + w * TabulatedCL(self.high).cl(s)


@dataclass(frozen=True)
class LinearCL:
    """Physical limit n = 1: C_L ∝ S (unsaturated regime), hence F_L ∝ |v| at constant ω. The slope is immaterial in a fit
    (ω absorbs it); 2.0 ≈ the initial slope of the measured curves."""
    slope: float = 2.0
    label: str = "limit_linear"

    def cl(self, s, re=None, speed=None):
        return self.slope * s


@dataclass(frozen=True)
class SaturatedCL:
    """Physical limit n = 2: C_L independent of S along the flight (saturated regime), hence F_L ∝ v².
    Implemented as C_L = slope · S · |v| / v_ref = slope · R|ω⊥| / v_ref (constant at constant ω), so that ω still sets
    the lift magnitude in a fit."""
    slope: float = 2.0
    v_ref: float = 32.0
    label: str = "limit_saturated"

    def cl(self, s, re=None, speed=None):
        return self.slope * s * speed / self.v_ref


LIFT_MODELS = {
    "kray2014_re462": TabulatedCL("kray2014_re462", "kray2014_re462"),
    "kray2014_re342": TabulatedCL("kray2014_re342", "kray2014_re342"),
    "kray2014_re_interp": ReInterpCL("kray2014_re342", "kray2014_re462", "kray2014_re_interp"),
    "asai2007_re455": TabulatedCL("asai2007_re455", "asai2007_re455"),
    "asai2007_re_interp": ReInterpCL("asai2007_re364", "asai2007_re455", "asai2007_re_interp"),
    "limit_linear": LinearCL(),
    "limit_saturated": SaturatedCL(),
}

#: Spin-dependent drag slope k_s in C_D = C_D0 + k_s·S. Default 0.47 (team decision).
SPIN_DRAG_SLOPES = {"asai2007": 0.47, "kray2014": 0.74, "off": 0.0}

#: Spin-decay constant k in dω/dt = −k ω |v| / R (Smits & Smith form). Default 0 (constant spin).
SPIN_DECAY_K = {"none": 0.0, "golf_like": 2e-5, "asai2020": 1.4e-4, "goff_carre": 5e-4, "james_subcritical": 2e-3}
