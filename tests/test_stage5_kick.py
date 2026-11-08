"""Stage 5: speed-dependent spin prior from the Asai 2002 kick model."""
import numpy as np
import pytest

from penalty.kick import ASAI2002_TABLE, KickSpinPrior, kick_outcome


def test_reproduces_asai_table_at_reference_speed():
    for d, spin, speed in ASAI2002_TABLE:
        vb, w = kick_outcome(26.0, d)
        assert vb == pytest.approx(speed) and w == pytest.approx(abs(spin))


def test_linear_scaling_with_kicker_speed():
    vb1, w1 = kick_outcome(26.0, 0.05)
    vb2, w2 = kick_outcome(39.0, 0.05)
    assert vb2 / vb1 == pytest.approx(1.5) and w2 / w1 == pytest.approx(1.5)


@pytest.fixture(scope="module")
def prior():
    return KickSpinPrior(n=600_000)


def test_conditional_density_normalised(prior):
    i = int(np.argmin(abs(prior.vb - 32.5)))
    assert np.sum(np.exp(prior.logp[i])) * 0.1 == pytest.approx(1.0, rel=1e-3)


def test_fast_shots_have_less_spin(prior):
    medians = [prior.summary(v)[0] for v in (28.0, 30.0, 32.0, 34.0)]
    assert all(a > b for a, b in zip(medians, medians[1:]))


def test_outside_support_is_impossible(prior):
    assert prior.log_density(45.0, 3.0)[0] == -np.inf
    assert np.isfinite(prior.log_density(32.6, 3.0)[0])
