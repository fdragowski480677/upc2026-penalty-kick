"""Atmospheric physics used for the climate/venue Monte Carlo (standard reference values)."""
import numpy as np
import pytest

from penalty.environment import (DensityPrior, air_density, dynamic_viscosity, pressure_at_altitude,
                                 sample_environment, saturation_vapour_pressure)


def test_isa_sea_level_density():
    assert air_density(15.0, 101325.0, 0.0) == pytest.approx(1.225, abs=0.001)


def test_humid_air_is_lighter():
    assert air_density(30.0, 101325.0, 0.9) < air_density(30.0, 101325.0, 0.0)


def test_saturation_vapour_pressure_reference_values():
    assert saturation_vapour_pressure(20.0) == pytest.approx(2339, rel=0.01)   # tables: 2.339 kPa
    assert saturation_vapour_pressure(100.0) == pytest.approx(101325, rel=0.01)


def test_sutherland_viscosity():
    assert dynamic_viscosity(20.0) == pytest.approx(1.81e-5, rel=0.01)


def test_isa_pressure_at_mexico_city():
    assert pressure_at_altitude(2240.0) == pytest.approx(77.2e3, rel=0.01)


def test_team_venue_table_isa_densities():
    """The team's venue table gives ISA densities (15 °C at sea level, standard lapse rate): 0.982 / 1.040 / 1.162 kg/m³."""
    from penalty.environment import T0_ISA, LAPSE
    for h, rho_ref in ((2240, 0.982), (1670, 1.040), (550, 1.162)):
        t_c = T0_ISA - LAPSE * h - 273.15
        assert air_density(t_c, pressure_at_altitude(h), 0.0) == pytest.approx(rho_ref, abs=0.003)


def test_envelope_and_prior():
    rho, t, alt = sample_environment(50_000, np.random.default_rng(0))
    assert 0.80 < rho.min() and rho.max() < 1.30
    assert np.all(rho[alt == 2240] < 1.0)
    prior = DensityPrior(n=100_000)
    assert np.isfinite(prior(1.15)) and prior(1.15) > prior(0.92)    # most venues are near sea level
    assert prior(0.5) == -np.inf
