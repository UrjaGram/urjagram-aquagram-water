"""
ICAR-NBSS&LUP Nagpur Soil Intelligence & Recharge Siting Parser.
Interfaces with National Bureau of Soil Survey & Land Use Planning data.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from .config import DATA_DIR

class NBSSLUPSoilService:
    def __init__(self, data_path: Path = None):
        if data_path is None:
            data_path = DATA_DIR / "nbsslup_soils_katol.json"
        
        with open(data_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)
            
        self.soil_units = {u["unit_id"]: u for u in self.dataset["soil_units"]}

    def get_soil_profile(self, unit_id: str) -> Dict[str, Any]:
        """Returns the complete soil profile for an NBSS&LUP mapping unit."""
        return self.soil_units.get(unit_id, self.soil_units["NBSS-KAT-02"])

    def calculate_root_zone_water_storage(self, unit_id: str, rooting_depth_cm: float = 60.0) -> Dict[str, float]:
        """
        Calculates maximum plant-available water holding capacity in mm
        based on NBSS&LUP AWC and actual effective soil depth.
        """
        soil = self.get_soil_profile(unit_id)
        effective_depth_cm = min(rooting_depth_cm, soil["depth_cm"])
        awc_mm_per_m = soil["available_water_capacity_mm_per_m"]
        
        total_awc_mm = (effective_depth_cm / 100.0) * awc_mm_per_m
        return {
            "effective_depth_cm": effective_depth_cm,
            "soil_awc_mm_per_m": awc_mm_per_m,
            "total_root_zone_storage_mm": round(total_awc_mm, 2)
        }

    def evaluate_recharge_structure_siting(self, unit_id: str, slope_percent: float) -> Dict[str, Any]:
        """
        Recommends appropriate rainwater harvesting & groundwater recharge structures
        based on NBSS&LUP infiltration rate, soil texture, and slope.
        """
        soil = self.get_soil_profile(unit_id)
        infiltration_rate = soil["steady_infiltration_rate_mm_per_hr"]
        suitability = soil["recharge_structure_suitability"]

        recommendations = []
        if infiltration_rate > 20.0 and slope_percent < 5.0:
            primary_structure = "Percolation Tank / Recharge Shaft"
            recommendations.append("High infiltration: Ideal for natural percolation tank or aquifer recharge pit.")
        elif infiltration_rate >= 8.0 and slope_percent <= 8.0:
            primary_structure = "Check Dam / Continuous Contour Trenches (CCT)"
            recommendations.append("Moderate clay content: Suitable for check dams on stream lines and field bunding.")
        else:
            primary_structure = "Lined Farm Pond (Shettale)"
            recommendations.append("Heavy swelling Vertisol clay: Low seepage; best for storing surface runoff in plastic-lined farm ponds.")

        return {
            "soil_series": soil["series_name"],
            "clay_percentage": soil["clay_percentage"],
            "infiltration_rate_mm_hr": infiltration_rate,
            "recommended_structure": primary_structure,
            "convergence_scheme": "MGNREGA / VB-G RAM G convergence",
            "specific_advice": recommendations
        }
