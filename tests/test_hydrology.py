"""
Unit tests for Hydrological Balance calculations.
"""

from src.hydrology import HydrologyEngine

def test_water_balance_depletion():
    engine = HydrologyEngine(baseline_storage_m3=300000.0, safe_yield_threshold_m3=100000.0)
    
    # In drought: 0 mm rainfall, 1500 m3 extraction per day
    res = engine.compute_daily_water_balance(rainfall_mm=0.0, pumping_draw_m3=1500.0, domestic_draw_m3=50.0)
    
    assert res["daily_recharge_m3"] == 0.0
    assert res["total_extraction_m3"] == 1550.0
    assert res["net_daily_change_m3"] == -1550.0
    assert res["current_storage_m3"] == 300000.0 - 1550.0
    assert res["days_of_water_remaining"] > 0

def test_crop_water_demand():
    engine = HydrologyEngine()
    chana_demand = engine.calculate_crop_water_demand("Gram (Chana)", area_acres=2.0, reference_et0_mm_day=4.0)
    
    assert chana_demand["crop"] == "Gram (Chana)"
    assert chana_demand["area_hectares"] > 0
    assert chana_demand["daily_demand_m3"] > 0
    assert chana_demand["total_seasonal_demand_m3"] > 0
