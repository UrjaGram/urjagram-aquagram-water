"""
NetZero Carbon Accounting & Scope 2 Emission Emitter for Water Pumping.
Prepares standard data stream for Raj Patil's NetZero accounting module.
"""

from typing import Dict, Any
from .config import CEA_GRID_EMISSION_FACTOR_KG_PER_KWH, VILLAGE_ID

class NetZeroEmitter:
    @staticmethod
    def calculate_pumping_emissions(
        pump_hp: float,
        daily_hours_run: float,
        borewells_count: int = 1,
        days_per_year: int = 150,
        grid_emission_factor_kg_kwh: float = CEA_GRID_EMISSION_FACTOR_KG_PER_KWH,
        solar_fraction: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates Scope 2 emissions from groundwater pumping using Central Electricity Authority factor.
        Formula:
        kW = HP * 0.7457
        Daily kWh = kW * daily_hours * pump_count
        Annual kWh = Daily kWh * days_per_year
        Gross emissions = Annual kWh * (1 - solar_fraction) * Factor
        """
        pump_kw = pump_hp * 0.7457
        daily_kwh = pump_kw * daily_hours_run * borewells_count
        annual_kwh = daily_kwh * days_per_year

        grid_kwh = annual_kwh * (1.0 - solar_fraction)
        avoided_solar_kwh = annual_kwh * solar_fraction

        annual_co2e_kg = grid_kwh * grid_emission_factor_kg_kwh
        annual_co2e_tonnes = annual_co2e_kg / 1000.0

        avoided_co2e_tonnes = (avoided_solar_kwh * grid_emission_factor_kg_kwh) / 1000.0

        return {
            "village_id": VILLAGE_ID,
            "subsystem": "water_pumping_scope2",
            "active_borewells": borewells_count,
            "daily_energy_consumption_kwh": round(daily_kwh, 2),
            "annual_grid_energy_kwh": round(grid_kwh, 2),
            "solar_replacement_share_percentage": round(solar_fraction * 100, 1),
            "emissions_kg_co2e_per_day": round(daily_kwh * (1.0 - solar_fraction) * grid_emission_factor_kg_kwh, 2),
            "annual_emissions_tco2e_per_year": round(annual_co2e_tonnes, 3),
            "avoided_emissions_tco2e_per_year": round(avoided_co2e_tonnes, 3),
            "accounting_standard": "IPCC Guidelines for National Greenhouse Gas Inventories & CEA CO2 Database",
            "target_recipient": "Raj Patil (NetZero Module)"
        }
