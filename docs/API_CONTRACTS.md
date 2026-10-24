# UrjaGram DEVTech Platform
## Inter-Module API Contracts & Schemas: AquaGram-Water
**Standard:** UrjaGram Sustainable Development Framework (USDF) v1.0  
**Data Standards:** Metric units in all headers, ISO 8601 timestamps, explicit village code.

---

### 1. Inbound Contract from Vibhor (Weather Module)
```json
{
  "village_id": "IN-MH-NAG-KATLABODI",
  "timestamp": "2026-10-24T06:00:00Z",
  "forecast_period_days": 10,
  "daily_forecast": [
    {
      "date": "2026-10-25",
      "expected_rainfall_mm": 0.0,
      "reference_et0_mm_day": 4.6,
      "max_temperature_celsius": 33.5,
      "heat_alert": false
    }
  ]
}
```

---

### 2. Outbound Contract to Vamsi (Crop Choice Module)
```json
{
  "village_id": "IN-MH-NAG-KATLABODI",
  "timestamp": "2026-10-24T18:00:00Z",
  "season": "Rabi 2026-27",
  "hydrological_limits": {
    "water_table_mbgl": 15.8,
    "projected_aquifer_runout_days": 167.9,
    "max_sustainable_irrigation_depth_mm": 280.0,
    "water_quota_per_acre_m3": 420.0,
    "crop_restrictions": [
      "NO_SUGARCANE",
      "NO_PADDY",
      "RESTRICT_WHEAT_TO_DRIP_ONLY",
      "RECOMMENDED_PULSES_CHANA_TUR"
    ]
  }
}
```

---

### 3. Inbound Contract from Devanshu (Solar Pumping Module)
```json
{
  "village_id": "IN-MH-NAG-KATLABODI",
  "timestamp": "2026-10-24T18:00:00Z",
  "solar_pump_installations": [
    {
      "farmer_code": "Farmer-KB-01",
      "pump_capacity_hp": 5.0,
      "solar_pv_kwp": 4.8,
      "available_solar_pumping_hours": 6.5,
      "recommended_pump_window": "09:30 to 16:00"
    }
  ]
}
```

---

### 4. Outbound Contract to Raj Patil (NetZero Module)
```json
{
  "village_id": "IN-MH-NAG-KATLABODI",
  "timestamp": "2026-10-24T18:00:00Z",
  "subsystem": "water_pumping_scope2",
  "metrics": {
    "active_agricultural_borewells": 42,
    "average_pumping_depth_mbgl": 15.8,
    "daily_water_extracted_m3": 1495.0,
    "daily_energy_consumption_kwh": 1252.78,
    "annual_grid_energy_kwh": 187917.0,
    "grid_emission_factor_kg_co2_per_kwh": 0.82,
    "annual_emissions_tco2e_per_year": 138.68,
    "avoided_solar_emissions_tco2e_per_year": 15.41
  },
  "compliance": {
    "standard": "IPCC Guidelines & CEA Baseline CO2 Database India",
    "status": "AUDITED_SIMULATION"
  }
}
```
