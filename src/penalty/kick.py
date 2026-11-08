"""Stage 5: a speed-dependent spin prior from foot–ball impact mechanics.

Basis [lit: Asai, Carré, Akatsuka & Haake 2002, Table 2]: an FE foot/ball model (foot speed 25 m/s, μ = 0.4) gives the ball speed
V(d) and spin Ω(d) as functions of the offset d between the impact point and the ball's axis. There is a **speed–spin trade-off**:
off-centre impacts add spin but lose speed.

Model [ours, with explicit assumptions]:
1. Impact mechanics are approximately linear in foot speed, so a kicker whose zero-offset ("full") strike reaches V_max produces
   V_b = V_max · V(d)/V(0) and Ω = V_max · Ω(d)/V(0). (Ishii 2012 supports ball speed ∝ foot speed; spin ∝ foot speed is assumed.)
2. Kicker capability: V_max ~ N(32, 2.5²) m/s, truncated to [25, 38] (elite penalties: mean ≈ 31, max ≈ 36 m/s, Wesson 2002;
   university players ≈ 24–26 m/s, Ravenscroft & Linthorne 2015; Asai 2002).
3. Offset: d ~ U(−0.10, 0.10) m (within the range where Asai's table is smooth; beyond ±0.12 m the ball speed collapses).
The prior on |ω| is the conditional p(Ω | V_b), with V_b = |v0|, tabulated from a Monte Carlo over (V_max, d).
"""
import numpy as np

#: Asai et al. 2002, Table 2: offset d [m], spin [rev/s] (sign = direction), ball speed [m/s]; foot 25 m/s, μ = 0.4.
ASAI2002_TABLE = np.array([
    [-0.16, -10.6, 6.2], [-0.14, -13.0, 10.9], [-0.12, -11.0, 15.2], [-0.10, -9.7, 19.0], [-0.08, -8.2, 20.5],
    [-0.06, -5.7, 22.9], [-0.04, -3.5, 23.5], [-0.02, -3.0, 25.5], [0.00, -1.9, 26.0], [0.02, 0.8, 25.9],
    [0.04, 4.0, 23.1], [0.06, 6.9, 20.7], [0.08, 10.5, 18.5], [0.10, 14.6, 15.1], [0.12, 16.2, 11.2],
    [0.14, 9.7, 4.5], [0.16, 0.0, 0.0]])
V_REF = 26.0  # ball speed at zero offset in the table


def kick_outcome(v_max, d):
    """(ball speed [m/s], |spin| [rev/s]) for kicker capability v_max and offset d (scaled Asai table)."""
    t = ASAI2002_TABLE
    scale = np.asarray(v_max) / V_REF
    return scale * np.interp(d, t[:, 0], t[:, 2]), scale * np.abs(np.interp(d, t[:, 0], t[:, 1]))


class KickSpinPrior:
    """Tabulated conditional log-density log p(Ω | V_b) on a (V_b, Ω) grid, from a Monte Carlo over (V_max, d)."""

    def __init__(self, n=2_000_000, seed=5, vmax_mean=32.0, vmax_sd=2.5, vmax_bounds=(25.0, 38.0), d_bounds=(-0.10, 0.10),
                 vb_grid=np.arange(18.0, 40.01, 0.25), w_grid=np.arange(0.0, 16.01, 0.1)):
        rng = np.random.default_rng(seed)
        vmax = rng.normal(vmax_mean, vmax_sd, 3 * n)
        vmax = vmax[(vmax > vmax_bounds[0]) & (vmax < vmax_bounds[1])][:n]
        d = rng.uniform(*d_bounds, vmax.size)
        vb, w = kick_outcome(vmax, d)
        H, _, _ = np.histogram2d(vb, w, bins=(np.append(vb_grid, vb_grid[-1] + 0.25) - 0.125,
                                             np.append(w_grid, w_grid[-1] + 0.1) - 0.05))
        k = np.exp(-0.5 * (np.arange(-3, 4) / 1.2) ** 2); k /= k.sum()
        H = np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), 1, H)
        H = np.apply_along_axis(lambda c: np.convolve(c, k, mode="same"), 0, H)
        rows = H.sum(axis=1, keepdims=True)
        cond = np.where(rows > 0, H / np.maximum(rows, 1e-300) / 0.1, 0.0)  # density in rev/s⁻¹ per V_b row
        self.vb, self.w = vb_grid, w_grid
        self.logp = np.log(np.maximum(cond, 1e-12))
        self.support = rows[:, 0] > 50

    def log_density(self, vb, w_rev):
        """log p(Ω = w_rev | V_b = vb) by bilinear interpolation; −inf outside the supported grid."""
        vb, w_rev = np.atleast_1d(vb), np.atleast_1d(w_rev)
        i = np.clip((vb - self.vb[0]) / (self.vb[1] - self.vb[0]), 0, len(self.vb) - 1.000001)
        j = np.clip((w_rev - self.w[0]) / (self.w[1] - self.w[0]), 0, len(self.w) - 1.000001)
        i0, j0 = i.astype(int), j.astype(int)
        fi, fj = i - i0, j - j0
        L = self.logp
        out = ((1 - fi) * (1 - fj) * L[i0, j0] + fi * (1 - fj) * L[i0 + 1, j0] + (1 - fi) * fj * L[i0, j0 + 1]
               + fi * fj * L[i0 + 1, j0 + 1])
        ok = (vb >= self.vb[0]) & (vb <= self.vb[-1]) & (w_rev <= self.w[-1]) & self.support[i0] & self.support[np.minimum(i0 + 1, len(self.vb) - 1)]
        return np.where(ok, out, -np.inf)

    def summary(self, vb):
        """Median and 2.5/97.5 % quantiles of Ω (rev/s) given the ball speed vb."""
        i = int(round((vb - self.vb[0]) / (self.vb[1] - self.vb[0])))
        p = np.exp(self.logp[i]); c = np.cumsum(p) / p.sum()
        return tuple(float(np.interp(q, c, self.w)) for q in (0.5, 0.025, 0.975))
