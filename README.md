# AquaGram-Water: Village Groundwater & Soil Intelligence Engine
### UrjaGram Sustainable Development Framework (USDF) · DEVTech Platform
**Author:** Kushagra Singh Kushwah (VNIT Nagpur)  
**Organization:** UrjaGram Innovations Pvt. Ltd., Gurugram / Nagpur  
**Leadership:** Amar Nath Sir (Ex-IAS, Founder & CEO, UrjaGram Innovations)  
**Assigned Domain:** Assignment #9 — Water & NBSS&LUP Soil Intelligence  
**Pilot Site:** Gram Panchayat Katlabodi (Katol Block, Nagpur District, Maharashtra)

[![AquaGram-Water CI](https://github.com/kushagrakushwah/urjagram-aquagram-water/actions/workflows/ci.yml/badge.svg)](https://github.com/kushagrakushwah/urjagram-aquagram-water/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Overview & Context

In September 2026, the Government of Maharashtra declared a severe drought across 265 of its 358 talukas (74% of the state). Vidarbha and Nagpur district were among the worst affected. 

**Katlabodi Gram Panchayat** (located in Katol Block, ~40 km from VNIT Nagpur) is a tribal forest-fringe community facing an acute groundwater emergency:
- **100% Groundwater Dependent:** 141.25 hectares (74.3% of net sown area) depend entirely on unmonitored borewells drilled into fractured Deccan basalt.
- **Zero Rainwater Harvesting:** 0% surface storage, no check dams, no percolation tanks.
- **Water Table Sinking:** Depths currently fluctuate between 40 to 60 feet (12 to 18 meters below ground level).
- **The Core Risk:** With an 8-hour daily power rotation for 42 agricultural borewells, the localized aquifer compartment faces exhaustion before Rabi crops (Gram / Chana and Wheat) can mature.

**AquaGram-Water** is the hydrological digital twin module of DEVTech that combines **ICAR-NBSS&LUP (Nagpur)** soil intelligence, **CGWB/GSDA** hydrogeology, and a **Dual AI Decision Architecture** to deliver predictive water budgeting, automated Marathi advisories, and Scope 2 carbon accounting.

---

## 2. The AI Architecture: "LLM Writes, Jev Decides, Code Acts"

Per the UrjaGram platform specification laid out by Amar Nath Sir:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION LAYER                            │
│  • IMD Weather & Rainfall (from Vibhor)                                │
│  • Static Groundwater Depletion Levels (CGWB / GSDA Maharashtra)       │
│  • Soil Series: Texture, Depth & AWC (ICAR-NBSS&LUP Nagpur)            │
│  • Crop Evapotranspiration: Cotton, Tur, Chana (from Vamsi)            │
│  • Solar Pumping Schedules (from Devanshu)                             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PHYSICAL HYDROLOGY ENGINE                            │
│  • Dynamic Daily Balance: ΔS = Rainfall + Recharge - ET_c - Pumping    │
│  • Days of Usable Groundwater Reserve Remaining                        │
│  • Farm-level discharge & deficit diagnostics (Farmer-KB-01)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     DUAL AI DECISION ENGINE                            │
│                                                                        │
│  [1. LLM Agent (Gemini / Offline Template)]                            │
│      └─ Generates plain-language agronomic reasoning & local Marathi    │
│         advisory for the tribal community.                             │
│                                                                        │
│  [2. TypeSafe Jev System-One Classifier]                               │
│      └─ Deterministically maps state vector to discrete action enum:   │
│         [LEVEL_0_NORMAL | LEVEL_1_ADVISORY | LEVEL_2_WARNING |         │
│          LEVEL_3_EMERGENCY]                                            │
│                                                                        │
│  [3. Deterministic Safety Guardrails (Code Acts)]                      │
│      └─ Code safety threshold: If water_table > 16.5 mbgl, minimum     │
│         status is WARNING. Jev can raise, NEVER lower.                 │
│      └─ Restricts borewell pumping hours & mandates drip irrigation.   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      NETZERO & PLATFORM EXPORTS                        │
│  • Pumping electricity Scope 2 emissions (tCO2e/yr) → Raj Patil        │
│  • Water quotas per acre → Vamsi (Crops)                               │
│  • Recharge structure siting (MGNREGA / VB-G RAM G) → Gram Panchayat   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Features

1. **Hydrological Water Balance:** Calculates daily recharge, extraction draw, and days of water left before aquifer dead storage.
2. **ICAR-NBSS&LUP Nagpur Soil Integration:** Incorporates actual soil survey data for Katol block (*Linga*, *Katol*, and *Bhasma* series) including Available Water Capacity (AWC) and steady infiltration rates.
3. **Recharge Siting Engine:** Recommends exact rainwater harvesting structures (percolation tanks on Bhasma uplands vs. lined farm ponds on Linga clays) for MGNREGA / VB-G RAM G convergence.
4. **Partner Farmer Diagnostic:** Evaluates `Farmer-KB-01` (3.5 acres, 1 borewell at 52 ft) to determine if planned Rabi Chana (Gram) sowing can be sustained.
5. **Bilingual Advisory:** Emits technical agronomic reasoning in English and actionable, empathetic advisory in **Marathi**.
6. **NetZero Emission Emitter:** Prepares Scope 2 carbon emission data (CEA India baseline: 0.82 kg CO₂e/kWh) streamed directly to Raj Patil's NetZero ledger.

---

## 4. Directory Structure

```text
urjagram-aquagram-water/
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── data/
│   ├── katlabodi_baseline.json    # Census, livestock, and well census baseline
│   ├── nbsslup_soils_katol.json   # ICAR-NBSS&LUP soil survey layers
│   └── partner_farmer.json        # Profile of Farmer-KB-01
├── docs/
│   ├── DOMAIN_NOTE.md             # Week 1 Deliverable (4-page technical note)
│   ├── AI_USE_CASES.md            # Week 2 Deliverable (Use-case shortlist)
│   └── API_CONTRACTS.md           # Inter-module JSON specifications
├── references/                    # Original field surveys, CSR proposal, briefs
├── src/
│   ├── __init__.py
│   ├── config.py                  # Coordinates, safety thresholds, emission factors
│   ├── hydrology.py               # Water balance & crop demand math
│   ├── nbsslup.py                 # Soil profile lookups & recharge siting
│   ├── jev_engine.py              # Jev System-One classifier & guardrails
│   ├── llm_agent.py               # Generative LLM agent (Gemini + offline fallback)
│   ├── netzero_emitter.py         # Scope 2 carbon accounting engine
│   ├── pipeline.py                # Master orchestrator
│   ├── cli.py                     # Command-line interface
│   └── dashboard.py               # Interactive web dashboard
├── tests/
│   ├── test_hydrology.py
│   ├── test_guardrails.py
│   └── test_netzero.py
├── pytest.ini
├── requirements.txt
├── setup.py
└── README.md
```

---

## 5. Quick Start & Installation

### Prerequisites
- Python 3.9 or higher
- Git

### 1. Clone & Install
```bash
git clone https://github.com/kushagrakushwah/urjagram-aquagram-water.git
cd urjagram-aquagram-water
pip install -r requirements.txt
```

### 2. Run the Unit Test Suite
```bash
pytest
```
*All 5 unit tests should pass in < 0.1s.*

### 3. Run the CLI Simulation
```bash
# Default Katlabodi conditions:
python -m src.cli

# Test severe drought stress scenario:
python -m src.cli --depth 56.5 --dry-days 25

# Output raw JSON for platform ingestion:
python -m src.cli --json
```

### 4. Launch the Interactive Web Dashboard
```bash
python -m src.dashboard
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser to interact with live gauges, water balance sliders, Marathi advisories, and NetZero telemetry!

---

## 6. Sample CLI Output

```text
===========================================================================
  AQUAGRAM-OS: VILLAGE GROUNDWATER & SOIL INTELLIGENCE ENGINE
  UrjaGram Innovations · DEVTech Platform · Pilot: Katlabodi (Katol, Nagpur)
===========================================================================

[AQUIFER STATUS]        : LEVEL_2_WARNING
[ACTION DIRECTIVE]      : RESTRICT_TO_DRIP_SPRINKLER_ONLY_CAP_PUMPING_4_HRS
[SAFETY GUARDRAIL]      : Compliant with safety threshold
---------------------------------------------------------------------------
• Water Table Depth     : 56.5 ft (17.22 mbgl)
• Days of Water Left    : 167.9 days (at current extraction)
• Usable Aquifer Storage: 251,005 m³
• Daily Extraction      : 1,495 m³/day | Recharge: 0 m³/day
---------------------------------------------------------------------------
PARTNER FARMER DIAGNOSTIC (Farmer-KB-01):
• Planned Rabi Crop     : Gram (Chana) (2.0 acres)
• Crop Daily Water Need : 34.6 m³/day
• Borewell Daily Yield  : 43.2 m³/day (Deficit: 0.0 m³/day)
---------------------------------------------------------------------------
ICAR-NBSS&LUP SOIL INTELLIGENCE:
• Local Soil Series     : Katol Series (AWC: 120.0 mm/m)
• Target Recharge Work  : Check Dam / Continuous Contour Trenches (CCT)
• Scheme Convergence    : MGNREGA / VB-G RAM G convergence
---------------------------------------------------------------------------
FARMER ADVISORY (MARATHI):
  काटलाबडी पाणी सतर्कता सूचना (Farmer-KB-01): जमिनीत पाणीपातळी 56.5 फूट खोल गेली आहे.
  Katol Series जमिनीमध्ये ओलावा टिकवण्यासाठी Gram (Chana) पिकाला तुषार किंवा ठिबक
  सिंचनानेच पाणी द्यावे. पंप दररोज जास्तीत जास्त ४ तास चालवावा आणि पाण्याचा अपव्यय टाळावा.

TECHNICAL REASONING (ENGLISH):
  WATER STRESS WARNING for Farmer-KB-01: Groundwater depth is at 56.5 ft on Katol Series.
  Borewell recharge is lagging behind seasonal crop evapotranspiration. Required action:
  Shift Gram (Chana) irrigation to 100% drip or sprinkler mode, cap pump duration to max 4 hours
  per day, and apply organic mulching to prevent evaporation loss.
---------------------------------------------------------------------------
NETZERO CARBON DATA (for Raj Patil):
• Agricultural Pumping  : 138.682 tCO2e/year (1252.78 kWh/day)
• Target Recipient      : Raj Patil (NetZero Module)
===========================================================================
```

---

## 7. Inter-Module Data Contracts

| Connected Module | Lead Intern | Data Exchanged |
| :--- | :--- | :--- |
| **Weather** | Vibhor | Ingests 10-day rainfall forecasts and $ET_0$ values to calculate dynamic aquifer recharge. |
| **Crops** | Vamsi | Exports sustainable irrigation depth ($mm$) and acre quotas to prevent high-water crop failure. |
| **Solar Pumping** | Devanshu | Harmonizes pump operational hours with peak solar insolation windows. |
| **NetZero Platform** | Raj Patil | Streams Scope 2 agricultural pumping emissions ($tCO_2e/yr$) using CEA India baseline factors. |

---

## 8. Author & Academic Engagement
- **Kushagra Singh Kushwah**, Department of Computer Science & Engineering, VNIT Nagpur
- **Academic Mentorship:** Visvesvaraya National Institute of Technology (VNIT), Nagpur
- **Industry & Policy Partner:** UrjaGram Innovations Pvt. Ltd., Cybercity Gurugram & Nagpur
