"""
Live integration test for Gemini AI advisory generation.
"""

import os
import pytest
from src.llm_agent import LLMAdvisoryAgent

def test_live_gemini_advisory_generation():
    agent = LLMAdvisoryAgent()
    assert agent.api_key is not None, "GEMINI_API_KEY must be loaded"

    farmer = {
        "farmer_code": "Farmer-KB-01",
        "current_cropping_plan": {
            "rabi_crop_planned": "Gram (Chana)",
            "rabi_acres": 2.0
        }
    }
    metrics = {
        "current_water_table_ft": 52.0,
        "days_of_water_remaining": 25.0
    }
    soil = {
        "series_name": "Katol Series"
    }

    res = agent.generate_advisories(
        farmer_data=farmer,
        hydrology_metrics=metrics,
        soil_profile=soil,
        alert_level="LEVEL_1_ADVISORY",
        action_directive="PROMOTE_NIGHT_IRRIGATION"
    )

    assert "english_technical" in res
    assert "marathi_farmer" in res
    assert len(res["english_technical"]) > 20
    assert len(res["marathi_farmer"]) > 10
