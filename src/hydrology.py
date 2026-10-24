"""
Hydrological Water Balance & Aquifer Runout Engine.
Formulated according to FAO-56 and CGWB groundwater estimation methodology.
"""

from typing import Dict, Any
from .config import M3_PER_HECTARE_MM, ACRES_TO_HECTARES, FEET_TO_METERS

# Standard FAO-56 Crop Coefficients (Kc) and water requirements for Vidarbha
CROP_WATER_SPECS = {
    "Cotton": {
        "season": "Kharif",
        "duration_days": 160,
        "total_water_need_mm": 650.0,
        "kc_mid": 1.15,
        "critical_stages": ["Flowering", "Boll Formation"]
    },
    "Pigeonpea (Tur)": {
        "season": "Kharif-Extended",
        "duration_days": 180,
        "total_water_need_mm": 500.0,
        "kc_mid": 1.05,
        "critical_stages": ["Branching", "Pod Development"]
    },
    "Gram (Chana)": {
        "season": "Rabi",
        "duration_days": 105,
        "total_water_need_mm": 280.0,
        "kc_mid": 0.95,
        "critical_stages": ["Pre-flowering", "Pod Filling"]
    },
    "Wheat": {
        "season": "Rabi",
        "duration_days": 120,
        "total_water_need_mm": 450.0,
        "kc_mid": 1.15,
        "critical_stages": ["Crown Root Initiation", "Flowering", "Milking"]
    }
}

class HydrologyEngine:
    def __init__(self, baseline_storage_m3: float = 380000.0, safe_yield_threshold_m3: float = 120000.0):
        self.current_storage_m3 = baseline_storage_m3
        self.safe_yield_threshold_m3 = safe_yield_threshold_m3

    def calculate_crop_water_demand(self, crop_name: str, area_acres: float, reference_et0_mm_day: float = 4.5) -> Dict[str, float]:
        """Calculates daily and seasonal water demand for a crop."""
        spec = CROP_WATER_SPECS.get(crop_name, {
            "total_water_need_mm": 350.0,
            "kc_mid": 1.0,
            "duration_days": 100
        })
        area_ha = area_acres * ACRES_TO_HECTARES
        daily_etc_mm = reference_et0_mm_day * spec["kc_mid"]
        daily_demand_m3 = daily_etc_mm * area_ha * M3_PER_HECTARE_MM
        total_seasonal_demand_m3 = spec["total_water_need_mm"] * area_ha * M3_PER_HECTARE_MM

        return {
            "crop": crop_name,
            "area_acres": area_acres,
            "area_hectares": round(area_ha, 3),
            "daily_demand_m3": round(daily_demand_m3, 2),
            "total_seasonal_demand_m3": round(total_seasonal_demand_m3, 2),
            "critical_stages": spec.get("critical_stages", [])
        }

    def compute_daily_water_balance(
        self,
        rainfall_mm: float,
        pumping_draw_m3: float,
        domestic_draw_m3: float = 45.0,
        recharge_efficiency_factor: float = 0.12,
        village_recharge_area_ha: float = 400.0
    ) -> Dict[str, Any]:
        """
        Computes the net daily groundwater balance:
        Recharge = Rainfall * Area * Infiltration Factor
        Net Storage = Storage + Recharge - Total Extraction
        """
        daily_recharge_m3 = rainfall_mm * village_recharge_area_ha * M3_PER_HECTARE_MM * recharge_efficiency_factor
        total_extraction_m3 = pumping_draw_m3 + domestic_draw_m3
        net_change_m3 = daily_recharge_m3 - total_extraction_m3
        
        updated_storage = max(0.0, self.current_storage_m3 + net_change_m3)
        self.current_storage_m3 = updated_storage

        usable_storage_above_threshold = max(0.0, updated_storage - self.safe_yield_threshold_m3)
        days_of_water_left = (
            usable_storage_above_threshold / total_extraction_m3
            if total_extraction_m3 > 0 else 999.0
        )

        return {
            "daily_rainfall_mm": rainfall_mm,
            "daily_recharge_m3": round(daily_recharge_m3, 2),
            "total_extraction_m3": round(total_extraction_m3, 2),
            "net_daily_change_m3": round(net_change_m3, 2),
            "current_storage_m3": round(updated_storage, 2),
            "usable_storage_above_dead_limit_m3": round(usable_storage_above_threshold, 2),
            "days_of_water_remaining": round(days_of_water_left, 1)
        }

    def compute_single_farm_runout(
        self,
        current_water_table_ft: float,
        borewell_yield_lps: float,
        daily_pump_hours: float,
        crop_name: str,
        farm_acres: float
    ) -> Dict[str, Any]:
        """Calculates farm-level borewell discharge and feasibility for a farmer family."""
        current_water_table_mbgl = current_water_table_ft * FEET_TO_METERS
        daily_discharge_m3 = (borewell_yield_lps * 3600.0 * daily_pump_hours) / 1000.0
        
        crop_demand = self.calculate_crop_water_demand(crop_name, farm_acres)
        water_deficit_m3 = crop_demand["daily_demand_m3"] - daily_discharge_m3

        return {
            "current_water_table_mbgl": round(current_water_table_mbgl, 2),
            "current_water_table_ft": current_water_table_ft,
            "daily_borewell_supply_m3": round(daily_discharge_m3, 2),
            "crop_daily_demand_m3": crop_demand["daily_demand_m3"],
            "daily_water_deficit_m3": round(max(0.0, water_deficit_m3), 2),
            "is_deficit": water_deficit_m3 > 0.0
        }
