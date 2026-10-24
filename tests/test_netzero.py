"""
Unit tests for NetZero Scope 2 Pumping Emissions.
"""

from src.netzero_emitter import NetZeroEmitter

def test_netzero_emission_calculation():
    # 5 HP pump running 8 hours per day
    res = NetZeroEmitter.calculate_pumping_emissions(
        pump_hp=5.0,
        daily_hours_run=8.0,
        borewells_count=1,
        days_per_year=150,
        solar_fraction=0.0
    )

    assert res["subsystem"] == "water_pumping_scope2"
    assert res["daily_energy_consumption_kwh"] > 0
    assert res["annual_emissions_tco2e_per_year"] > 0
    assert res["target_recipient"] == "Raj Patil (NetZero Module)"
