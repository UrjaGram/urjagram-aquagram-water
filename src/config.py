"""
Configuration and constants for AquaGram-Water.
Adheres strictly to the UrjaGram Platform standards:
- All units metric in field names
- Hard safety thresholds
- CCTS / CEA India emission factors
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Village Identification
VILLAGE_ID = "IN-MH-NAG-KATLABODI"
VILLAGE_NAME = "Katlabodi"
TALUKA = "Katol"
DISTRICT = "Nagpur"
STATE = "Maharashtra"
LATITUDE = 21.2833
LONGITUDE = 78.5833

# Hydrological and Physical Constants
FEET_TO_METERS = 0.3048
ACRES_TO_HECTARES = 0.404686
M3_PER_HECTARE_MM = 10.0  # 1 mm of water over 1 ha = 10 m^3

# Hard Safety Guardrail Thresholds (mbgl = meters below ground level)
# CGWB / GSDA Vidarbha Deccan Basalt Guidelines:
SAFE_WATER_TABLE_MAX_MBGL = 12.0      # ~39.4 ft
ADVISORY_WATER_TABLE_MBGL = 15.0       # ~49.2 ft
WARNING_WATER_TABLE_MBGL = 16.5        # ~54.1 ft
CRITICAL_EMERGENCY_MBGL = 18.0         # ~59.0 ft

# Grid Carbon Emission Factor (Central Electricity Authority - CEA CO2 Baseline Database India)
# CEA User Guide v19: National grid average is ~0.82 kg CO2 / kWh
CEA_GRID_EMISSION_FACTOR_KG_PER_KWH = 0.82
DIESEL_EMISSION_FACTOR_KG_PER_LITER = 2.68
