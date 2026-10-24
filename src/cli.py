"""
Command Line Interface for AquaGram-Water.
Run instant water balance simulations and get actionable advisories.
"""

import sys
import json
import argparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from .pipeline import AquaGramWaterPipeline

def main():
    parser = argparse.ArgumentParser(
        description="AquaGramOS: Village Groundwater & Soil Intelligence Engine (UrjaGram Innovations)"
    )
    parser.add_argument("--depth", type=float, default=51.8, help="Current water table depth in feet (e.g., 52.0)")
    parser.add_argument("--rain", type=float, default=0.0, help="Forecast/observed daily rainfall in mm (e.g., 0.0)")
    parser.add_argument("--dry-days", type=int, default=18, help="Consecutive days without rainfall")
    parser.add_argument("--pump-hours", type=float, default=8.0, help="Agricultural power/pump hours per day")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format for platform ingestion")

    args = parser.parse_args()
    pipeline = AquaGramWaterPipeline()
    result = pipeline.run_assessment(
        current_water_table_ft=args.depth,
        daily_rainfall_mm=args.rain,
        consecutive_dry_days=args.dry_days,
        active_pump_hours=args.pump_hours
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Formatted Terminal Output
    print("\n" + "=" * 75)
    print(f"  AQUAGRAM-OS: VILLAGE GROUNDWATER & SOIL INTELLIGENCE ENGINE")
    print(f"  UrjaGram Innovations · DEVTech Platform · Pilot: Katlabodi (Katol, Nagpur)")
    print("=" * 75)

    status = result["status_code"]
    color_code = "\033[91m" if "EMERGENCY" in status else ("\033[93m" if "WARNING" in status else "\033[92m")
    reset_code = "\033[0m"

    print(f"\n[AQUIFER STATUS]        : {color_code}{status}{reset_code}")
    print(f"[ACTION DIRECTIVE]      : {result['action_directive']}")
    print(f"[SAFETY GUARDRAIL]      : {result['guardrail_status']}")
    print("-" * 75)

    m = result["metrics"]
    print(f"• Water Table Depth     : {m['water_table_depth_ft']} ft ({m['water_table_depth_mbgl']} mbgl)")
    print(f"• Days of Water Left    : {m['days_of_water_remaining']} days (at current extraction)")
    print(f"• Usable Aquifer Storage: {m['usable_storage_m3']:,.0f} m³")
    print(f"• Daily Extraction      : {m['daily_extraction_m3']:,.0f} m³/day | Recharge: {m['daily_recharge_m3']:,.0f} m³/day")

    print("-" * 75)
    f = result["partner_farmer_analysis"]
    print(f"PARTNER FARMER DIAGNOSTIC ({f['farmer_code']}):")
    print(f"• Planned Rabi Crop     : {f['crop']} ({f['acres']} acres)")
    print(f"• Crop Daily Water Need : {f['daily_crop_demand_m3']} m³/day")
    print(f"• Borewell Daily Yield  : {f['borewell_daily_supply_m3']} m³/day (Deficit: {f['daily_deficit_m3']} m³/day)")

    print("-" * 75)
    s = result["soil_and_recharge"]
    print(f"ICAR-NBSS&LUP SOIL INTELLIGENCE:")
    print(f"• Local Soil Series     : {s['soil_series']} (AWC: {s['available_water_capacity_mm_m']} mm/m)")
    print(f"• Target Recharge Work  : {s['recommended_recharge_structure']}")
    print(f"• Scheme Convergence    : {s['convergence_opportunity']}")

    print("-" * 75)
    b = result["bilingual_advisory"]
    print("FARMER ADVISORY (MARATHI):")
    print(f"  {b['marathi_farmer']}")
    print("\nTECHNICAL REASONING (ENGLISH):")
    print(f"  {b['english_technical']}")

    print("-" * 75)
    nz = result["netzero_stream"]
    print(f"NETZERO CARBON DATA (for Raj Patil):")
    print(f"• Agricultural Pumping  : {nz['annual_emissions_tco2e_per_year']} tCO2e/year ({nz['daily_energy_consumption_kwh']} kWh/day)")
    print(f"• Target Recipient      : {nz['target_recipient']}")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
