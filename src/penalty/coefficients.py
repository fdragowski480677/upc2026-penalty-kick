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
