"""
Generative LLM Reasoning Agent for Bilingual Farmer Advisories (Marathi + English).
Implements the first stage of:
"A language model writes, Jev decides, code acts."
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any

class LLMAdvisoryAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # Check .env file in project root
            env_file = Path(__file__).resolve().parent.parent / ".env"
            if env_file.exists():
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            os.environ["GEMINI_API_KEY"] = self.api_key
                            break

    def generate_advisories(
        self,
        farmer_data: Dict[str, Any],
        hydrology_metrics: Dict[str, Any],
        soil_profile: Dict[str, Any],
        alert_level: str,
        action_directive: str
    ) -> Dict[str, Any]:
        """
        Generates bilingual explainable reasoning:
        1. English Technical Agronomic Summary
        2. Marathi Farmer-Facing Plain Language Advisory
        """
        if self.api_key:
            try:
                res = self._call_gemini_api(
                    farmer_data, hydrology_metrics, soil_profile, alert_level, action_directive
                )
                if res and "english_technical" in res and "marathi_farmer" in res:
                    res["generation_source"] = "LIVE_GEMINI_API (gemini-3.5-flash)"
                    return res
            except Exception as e:
                # Log error and fall back gracefully to template engine
                pass
        
        fallback = self._generate_template_advisories(
            farmer_data, hydrology_metrics, soil_profile, alert_level, action_directive
        )
        fallback["generation_source"] = "DETERMINISTIC_OFFLINE_TEMPLATE"
        return fallback

    def _generate_template_advisories(
        self,
        farmer_data: Dict[str, Any],
        metrics: Dict[str, Any],
        soil: Dict[str, Any],
        alert: str,
        action: str
    ) -> Dict[str, str]:
        """High-fidelity local deterministic generator (offline fallback)."""
        farmer_code = farmer_data.get("farmer_code", "Farmer-KB-01")
        crop = farmer_data.get("current_cropping_plan", {}).get("rabi_crop_planned", "Gram (Chana)")
        acres = farmer_data.get("current_cropping_plan", {}).get("rabi_acres", 2.0)
        water_table_ft = metrics.get("current_water_table_ft", 52.0)
        days_left = metrics.get("days_of_water_remaining", 18.0)
        soil_name = soil.get("series_name", "Katol Series")

        if "EMERGENCY" in alert:
            english = (
                f"CRITICAL AQUIFER ALERT for {farmer_code}: Groundwater table has receded to {water_table_ft:.1f} ft "
                f"(projected reserve depletion in {days_left:.0f} days). In accordance with UrjaGram drought safety protocol, "
                f"flood irrigation for {crop} ({acres} acres) is halted immediately. Divert remaining capacity to drinking water "
                f"and micro-drip protective irrigation only."
            )
            marathi = (
                f"काटलाबडी ग्रामपंचायत अतिदक्षता सूचना: आपल्या विहिरीतील पाणीपातळी {water_table_ft:.1f} फुटांवर गेली आहे. "
                f"पाण्याचा साठा अवघा {days_left:.0f} दिवस पुरेल एवढाच आहे. {crop} पिकाला मोकळे पाणी (पाट पाणी) देणे त्वरित थांबवावे. "
                f"फक्त ठिबक सिंचनाने पाणी द्या किंवा उपलब्ध पाणी जनावरांसाठी सुरक्षित ठेवा."
            )
        elif "WARNING" in alert:
            english = (
                f"WATER STRESS WARNING for {farmer_code}: Groundwater depth is at {water_table_ft:.1f} ft on {soil_name}. "
                f"Borewell recharge is lagging behind seasonal crop evapotranspiration. Required action: Shift {crop} irrigation "
                f"to 100% drip or sprinkler mode, cap pump duration to max 4 hours per day, and apply organic mulching to prevent "
                f"evaporation loss."
            )
            marathi = (
                f"काटलाबडी पाणी सतर्कता सूचना ({farmer_code}): जमिनीत पाणीपातळी {water_table_ft:.1f} फूट खोल गेली आहे. "
                f"{soil_name} जमिनीमध्ये ओलावा टिकवण्यासाठी {crop} पिकाला तुषार किंवा ठिबक सिंचनानेच पाणी द्यावे. "
                f"पंप दररोज जास्तीत जास्त ४ तास चालवावा आणि पाण्याचा अपव्यय टाळावा."
            )
        else:
            english = (
                f"SUSTAINABLE ADVISORY for {farmer_code}: Groundwater table is at {water_table_ft:.1f} ft. "
                f"Water budget permits planned sowing of {acres} acres of {crop}. Maintain soil moisture checks using tensiometer."
            )
            marathi = (
                f"शेतकरी सल्ला ({farmer_code}): विहिरीची पाणीपातळी {water_table_ft:.1f} फुटांवर स्थिर आहे. "
                f"{crop} पेरणीसाठी पाण्याचे नियोजन योग्य आहे. रात्रीच्या सत्रात वीज असताना योग्य प्रमाणात पाणी द्यावे."
            )

        return {
            "english_technical": english,
            "marathi_farmer": marathi
        }

    def _call_gemini_api(self, farmer, metrics, soil, alert, action) -> Dict[str, str]:
        farmer_code = farmer.get("farmer_code", "Farmer-KB-01")
        crop = farmer.get("current_cropping_plan", {}).get("rabi_crop_planned", "Gram (Chana)")
        acres = farmer.get("current_cropping_plan", {}).get("rabi_acres", 2.0)
        water_table_ft = metrics.get("current_water_table_ft", 52.0)
        days_left = metrics.get("days_of_water_remaining", 18.0)
        soil_name = soil.get("series_name", "Katol Series")

        prompt = f"""
You are the Agro-Hydrology AI for UrjaGram DEVTech operating in Katlabodi tribal village, Katol, Nagpur (severe drought region).
Input Data:
- Farmer Code: {farmer_code}
- Planned Rabi Crop: {crop} ({acres} acres)
- Water Table Depth: {water_table_ft} ft
- Aquifer Days Remaining: {days_left} days
- Soil Series: {soil_name}
- Jev Decision Status: {alert}
- Action Directive: {action}

Respond ONLY with a valid JSON object matching this schema:
{{
  "english_technical": "2-sentence agronomic technical explanation of soil moisture status, groundwater draw limits, and protective irrigation.",
  "marathi_farmer": "2-sentence direct, respectful, simple Marathi advisory for the tribal farmer on how to save their borewell water and protect the standing crop."
}}
"""
        models_to_try = ["gemini-3.5-flash", "gemini-2.5-flash-lite", "gemini-3.8-flash"]
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            try:
                res = requests.post(url, json=payload, timeout=12)
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    parsed = json.loads(raw_text)
                    if "english_technical" in parsed and "marathi_farmer" in parsed:
                        return parsed
            except Exception:
                continue

        raise RuntimeError("All Gemini API candidate models exhausted")
