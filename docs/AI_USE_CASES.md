# UrjaGram Sustainable Development Framework (USDF)
## AI Use-Case Shortlist & Decision Matrix: AquaGram-Water
**Author:** Kushagra Singh Kushwah (VNIT Nagpur)  
**Deliverable:** Week 2 AI Use-Case Evaluation  
**Pilot Village:** Katlabodi Gram Panchayat, Katol, Nagpur

---

### 1. Three Shortlisted AI Use Cases

#### Use Case 1: Dynamic Village Water Balance & Aquifer Runout Early Warning
- **User:** Partner Farmer (`Farmer-KB-01`) and Gram Panchayat Sarpanch.
- **Decision:** Whether to permit unrestricted agricultural borewell pumping or enforce staggered/micro-irrigation rationing for Rabi crops.
- **Data Required:**
  - Weekly static water level measurements (feet / mbgl).
  - NBSS&LUP soil moisture retention curve (Katol / Linga series).
  - 10-day IMD rainfall and evapotranspiration forecast ($ET_0$).
  - Power supply availability schedule (8 hours/day).
- **Action Triggered:**
  - Jev System-One classifier categorizes village state into `[NORMAL | ADVISORY | WARNING | EMERGENCY]`.
  - Sends automated SMS/WhatsApp alerts in Marathi advising exact pumping hour ceilings (e.g. *"Cap borewell run to 4 hours per day"*).
  - Enforces hard deterministic safety guardrail: if water table $> 55$ ft mbgl, flood irrigation is locked out.

---

#### Use Case 2: NBSS&LUP Soil-Driven Groundwater Recharge Siting Engine
- **User:** Gram Panchayat, Jal Sakhi cadre, and MGNREGA / Taluka Agriculture Officer.
- **Decision:** Selecting the exact geo-locations and engineering types for artificial recharge structures (check dams vs. percolation tanks vs. farm ponds).
- **Data Required:**
  - ICAR-NBSS&LUP soil series maps (texture, clay %, infiltration rate in mm/hr).
  - Topographic slope and drainage density.
  - Historical monsoon runoff coefficient.
- **Action Triggered:**
  - Generates a prioritized watershed works list for the Gram Panchayat Integrated Investment Plan (GP-IIP).
  - Directs percolation tanks to high-permeability Bhasma uplands (> 30 mm/hr infiltration) and lined farm ponds to low-permeability Linga black clay soils (< 6 mm/hr infiltration).

---

#### Use Case 3: Solar Pumping & Irrigation Harmonization Optimizer
- **User:** Farmers adopting PM-KUSUM solar pumps and Devanshu (Solar module).
- **Decision:** Scheduling irrigation cycles to match solar insolation peaks without exceeding aquifer recharge recovery rates.
- **Data Required:**
  - Hourly solar radiation forecast.
  - Aquifer recovery drawdown curve.
  - Crop stage critical water demand.
- **Action Triggered:**
  - Automated pump scheduling controller allocating solar pumping hours to minimize battery storage requirements and avoid cone-of-depression well interference.

---

### 2. Selection Rationale for the Build

| Criteria | Use Case 1 (Water Balance Early Warning) | Use Case 2 (Recharge Siting) | Use Case 3 (Solar Harmonization) |
| :--- | :--- | :--- | :--- |
| **Urgency for Katlabodi** | **CRITICAL** (Drought active right now) | **HIGH** (Pre-monsoon preparation) | **MEDIUM** (Few solar pumps exist) |
| **Partner Farmer Impact** | Saves standing Rabi Chana crop | Village-scale infrastructure | Secondary optimization |
| **Adherence to Jev Pattern** | Perfect fit (*LLM writes, Jev decides, code acts*) | Spatial rule overlay | Optimization engine |
| **Cross-Module Linkages** | Links to Weather, Crops, NetZero | Links to Soil & Infrastructure | Links to Solar & Energy |

### Final Build Decision:
We select **Use Case 1 (Dynamic Aquifer Runout Early Warning)** as the primary operational build, integrated with **Use Case 2 (NBSS&LUP Recharge Siting)** as the planning layer. This directly protects `Farmer-KB-01` from borewell failure during the 2026–27 drought while equipping the Gram Panchayat with actionable MGNREGA convergence works.
