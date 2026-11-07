"""Atmospheric state and its effect on the aerodynamic parameters (Stage 4 Monte Carlo over climate and venue).

Physics [theory]:
* Moist-air density (ideal gas mixture of dry air and water vapour): ρ = (p − e)/(R_d T) + e/(R_v T), with e = RH·e_s(T).
* Saturation vapour pressure e_s(T): Buck/Magnus form, e_s = 611.21·exp((18.678 − T/234.5)·T/(257.14 + T)) Pa (T in °C).
* Pressure at altitude: International Standard Atmosphere troposphere, p = p0 (1 − L h / T0)^(g M / (R L)), times a weather factor.
* Dynamic viscosity μ(T): Sutherland's law (μ_ref = 1.716e-5 Pa s at 273.15 K, S = 110.4 K). The effect of humidity on μ (≲ 1 %) is neglected.
  The kinematic viscosity is ν = μ/ρ.
Humidity *lowers* ρ (water vapour is lighter than dry air). Altitude is by far the largest effect (Hörzer 2010).

Venue envelope: FIFA World Cup 2026 stadiums (team decision). Mexico City 2240 m, Guadalajara 1670 m and Monterrey 550 m come from the team's
venue table (references/2022/literature.txt). The US and Canadian venues are approximate (± ~20 m; all < 300 m, so their effect on ρ is < 0.3 %).
Several stadiums are roofed or air-conditioned; the broad temperature range is a conservative envelope.
"""
import numpy as np

R_D, R_V = 287.058, 461.495        # J/(kg K): specific gas constants of dry air and water vapour
P0, T0_ISA, LAPSE = 101325.0, 288.15, 0.0065
G0, M_AIR, R_UNIV = 9.80665, 0.0289644, 8.31446

#: (stadium, city, approximate altitude in m)
WC2026_VENUES = [
    ("MetLife Stadium", "New York/New Jersey", 3), ("SoFi Stadium", "Los Angeles", 30), ("AT&T Stadium", "Dallas", 180),
    ("Levi's Stadium", "San Francisco Bay Area", 10), ("Hard Rock Stadium", "Miami", 3), ("Mercedes-Benz Stadium", "Atlanta", 300),
    ("Lumen Field", "Seattle", 5), ("NRG Stadium", "Houston", 15), ("Lincoln Financial Field", "Philadelphia", 10),
    ("Arrowhead Stadium", "Kansas City", 260), ("Gillette Stadium", "Boston", 80), ("BMO Field", "Toronto", 80),
    ("BC Place", "Vancouver", 5), ("Estadio Azteca", "Mexico City", 2240), ("Estadio Akron", "Guadalajara", 1670),
    ("Estadio BBVA", "Monterrey", 550),
]


def saturation_vapour_pressure(t_c):
    t_c = np.asarray(t_c, dtype=float)
    return 611.21 * np.exp((18.678 - t_c / 234.5) * (t_c / (257.14 + t_c)))


def pressure_at_altitude(h):
    return P0 * (1 - LAPSE * np.asarray(h, dtype=float) / T0_ISA) ** (G0 * M_AIR / (R_UNIV * LAPSE))


def air_density(t_c, p, rh):
    T = np.asarray(t_c, dtype=float) + 273.15
    e = np.asarray(rh, dtype=float) * saturation_vapour_pressure(t_c)
    return (p - e) / (R_D * T) + e / (R_V * T)


def dynamic_viscosity(t_c):
    T = np.asarray(t_c, dtype=float) + 273.15
    return 1.716e-5 * (T / 273.15) ** 1.5 * (273.15 + 110.4) / (T + 110.4)


def sample_environment(n, rng, t_range=(12.0, 35.0), rh_range=(0.20, 0.90), weather_sd=0.01, venues=WC2026_VENUES):
    """Monte Carlo draw of (ρ, T [°C], altitude [m]) over the venue envelope: a uniform venue, uniform T and RH, and a Gaussian weather pressure factor."""
    alt = np.array([v[2] for v in venues], dtype=float)[rng.integers(0, len(venues), n)]
    t = rng.uniform(*t_range, n)
    rh = rng.uniform(*rh_range, n)
    p = pressure_at_altitude(alt) * (1 + weather_sd * rng.standard_normal(n))
    return air_density(t, p, rh), t, alt


class DensityPrior:
    """The marginal prior density of ρ implied by the venue/climate envelope, from a Monte Carlo histogram (smoothed, tabulated, log-interpolated)."""

    def __init__(self, n=400_000, seed=11, bins=240):
        rho, _, _ = sample_environment(n, np.random.default_rng(seed))
        lo, hi = rho.min() - 0.01, rho.max() + 0.01
        hist, edges = np.histogram(rho, bins=bins, range=(lo, hi), density=True)
        kernel = np.exp(-0.5 * (np.arange(-4, 5) / 1.5) ** 2)
        hist = np.convolve(hist, kernel / kernel.sum(), mode="same")
        self.x = 0.5 * (edges[1:] + edges[:-1])
        self.logp = np.log(np.maximum(hist, 1e-12))
        self.bounds = (lo, hi)
        self.samples = rho

    def __call__(self, rho):
        rho = np.asarray(rho)
        out = np.interp(rho, self.x, self.logp)
        return np.where((rho > self.bounds[0]) & (rho < self.bounds[1]), out, -np.inf)
