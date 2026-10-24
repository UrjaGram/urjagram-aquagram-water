"""
Unified Master Pipeline for AquaGram-Water.
Coordinates Hydrology -> NBSS&LUP Soil -> Jev Decisions -> LLM Advisory -> NetZero Accounting.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from .config import DATA_DIR, VILLAGE_ID, VILLAGE_NAME, FEET_TO_METERS
from .hydrology import HydrologyEngine
from .nbsslup import NBSSLUPSoilService
from .jev_engine import JevDecisionEngine, AlertLevel
from .llm_agent import LLMAdvisoryAgent
from .netzero_emitter import NetZeroEmitter

class AquaGramWaterPipeline:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        
        # Load baseline datasets
        with open(self.data_dir / "katlabodi_baseline.json", "r", encoding="utf-8") as f:
            self.baseline = json.load(f)

        with open(self.data_dir / "partner_farmer.json", "r", encoding="utf-8") as f:
            self.partner_farmer = json.load(f)

        # Initialize core services
        self.soil_service = NBSSLUPSoilService(self.data_dir / "nbsslup_soils_katol.json")
        self.hydrology = HydrologyEngine(
            baseline_storage_m3=self.baseline["hydrogeology"]["current_storage_m3"],
            safe_yield_threshold_m3=self.baseline["hydrogeology"]["total_estimated_extractable_reserve_m3"] * 0.15
        )
        self.llm_agent = LLMAdvisoryAgent()

    def run_assessment(
        self,
        current_water_table_ft: Optional[float] = None,
        daily_rainfall_mm: float = 0.0,
        consecutive_dry_days: int = 18,
        active_pump_hours: Optional[float] = None
    ) -> Dict[str, Any]:
        """Runs the complete end-to-end village assessment pipeline."""
        
        # 1. Resolve State Variables
        wt_ft = current_water_table_ft or self.baseline["hydrogeology"]["water_table_ft"]
        wt_mbgl = wt_ft * FEET_TO_METERS
        pump_hours = active_pump_hours or self.baseline["hydrogeology"]["power_supply_hours_per_day"]

        # 2. Run Hydrological Balance
        village_daily_draw = self.baseline["hydrogeology"]["average_pumping_draw_m3_per_day"]
        water_balance = self.hydrology.compute_daily_water_balance(
            rainfall_mm=daily_rainfall_mm,
            pumping_draw_m3=village_daily_draw,
            domestic_draw_m3=self.baseline["hydrogeology"]["domestic_draw_m3_per_day"]
        )

        # 3. Partner Farmer Diagnostics
        farm_plan = self.partner_farmer["current_cropping_plan"]
        farm_crop = farm_plan["rabi_crop_planned"]
        farm_acres = farm_plan["rabi_acres"]
        
        farm_runout = self.hydrology.compute_single_farm_runout(
            current_water_table_ft=wt_ft,
            borewell_yield_lps=1.5,
            daily_pump_hours=pump_hours,
            crop_name=farm_crop,
            farm_acres=farm_acres
        )

        # 4. Soil Intelligence & Recharge Siting
        soil_unit = self.partner_farmer.get("soil_series", "NBSS-KAT-02").split()[0].strip()
        if soil_unit not in self.soil_service.soil_units:
            soil_unit = "NBSS-KAT-02"
        soil_profile = self.soil_service.get_soil_profile(soil_unit)
        recharge_siting = self.soil_service.evaluate_recharge_structure_siting(soil_unit, slope_percent=3.5)

        # 5. Jev System-One Classification + Hard Safety Guardrails
        jev_prelim = JevDecisionEngine.classify_status(
            water_table_mbgl=wt_mbgl,
            days_of_water_left=water_balance["days_of_water_remaining"],
            consecutive_dry_days=consecutive_dry_days
        )
        
        final_level, directive, guardrail_rationale = JevDecisionEngine.enforce_hard_safety_guardrails(
            jev_decision=jev_prelim,
            current_water_table_mbgl=wt_mbgl
        )

        # 6. LLM Advisory (Bilingual)
        advisories = self.llm_agent.generate_advisories(
            farmer_data=self.partner_farmer,
            hydrology_metrics={
                "current_water_table_ft": wt_ft,
                "days_of_water_remaining": water_balance["days_of_water_remaining"]
            },
            soil_profile=soil_profile,
            alert_level=final_level.value,
            action_directive=directive.value
        )

        # 7. NetZero Emission Stream for Raj Patil
        borewells_count = self.baseline["hydrogeology"]["agricultural_borewells_count"]
        netzero_data = NetZeroEmitter.calculate_pumping_emissions(
            pump_hp=self.baseline["hydrogeology"]["average_pump_hp"],
            daily_hours_run=pump_hours,
            borewells_count=borewells_count,
            days_per_year=150,
            solar_fraction=0.10  # 10% solar penetration baseline
        )

        # 8. Synthesize into UrjaGram Platform Format
        result = {
            "village_id": VILLAGE_ID,
            "village_name": VILLAGE_NAME,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status_code": final_level.value,
            "action_directive": directive.value,
            "guardrail_status": guardrail_rationale,
            "metrics": {
                "water_table_depth_ft": round(wt_ft, 1),
                "water_table_depth_mbgl": round(wt_mbgl, 2),
                "days_of_water_remaining": water_balance["days_of_water_remaining"],
                "usable_storage_m3": water_balance["usable_storage_above_dead_limit_m3"],
                "daily_recharge_m3": water_balance["daily_recharge_m3"],
                "daily_extraction_m3": water_balance["total_extraction_m3"]
            },
            "partner_farmer_analysis": {
                "farmer_code": self.partner_farmer["farmer_code"],
                "crop": farm_crop,
                "acres": farm_acres,
                "daily_crop_demand_m3": farm_runout["crop_daily_demand_m3"],
                "borewell_daily_supply_m3": farm_runout["daily_borewell_supply_m3"],
                "daily_deficit_m3": farm_runout["daily_water_deficit_m3"]
            },
            "soil_and_recharge": {
                "soil_series": soil_profile["series_name"],
                "available_water_capacity_mm_m": soil_profile["available_water_capacity_mm_per_m"],
                "recommended_recharge_structure": recharge_siting["recommended_structure"],
                "convergence_opportunity": recharge_siting["convergence_scheme"]
            },
            "bilingual_advisory": advisories,
            "netzero_stream": netzero_data
        }

        return result
