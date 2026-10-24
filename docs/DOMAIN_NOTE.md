# UrjaGram Sustainable Development Framework (USDF)
## Technical Domain Note: Village Groundwater, Soil Moisture & Hydro-Ecological Intelligence
**Author:** Kushagra Singh Kushwah, B.Tech Intern, VNIT Nagpur  
**Assignment:** Assignment #9 — Water & NBSS&LUP Soil Intelligence  
**Pilot Site:** Gram Panchayat Katlabodi (Villages: Katlabodi, Murli, Dhankundav), Katol Block, Nagpur District, Maharashtra  
**Project Lead:** Amar Nath Sir (Founder & CEO, UrjaGram Innovations Pvt Ltd)  
**Date:** October 2026 (Week 1 Deliverable)

---

### 1. Executive Summary & Village Hydrogeological Context
Gram Panchayat Katlabodi is a forest-fringe tribal settlement of 717 residents (160 households; 52.2% Scheduled Tribes) situated in the Deccan Basaltic terrain of Katol Block, Nagpur District. In September 2026, the Government of Maharashtra declared a severe drought across 265 of its 358 talukas (74% of the state), with Nagpur district identified among the six most vulnerable districts following a monsoon rainfall deficit exceeding 35% and consecutive dry spells stretching over 21 days.

Katlabodi represents an acute hydrological paradox:
1. **Total Land Base:** 671.16 hectares, of which 416.28 ha (62.0%) is designated forest land and 190.10 ha (28.3%) constitutes the net sown area.
2. **Groundwater Over-Reliance:** An extraordinary 74.3% of the cultivated land (141.25 ha) is under protective or perennial irrigation—supplied **100% by unmonitored groundwater extracted from weathered vesicular basalt traps**.
3. **Zero Surface Storage:** The village contains **0% rainwater harvesting infrastructure**, zero check dams, zero percolation tanks, and no perennial surface streams.
4. **Aquifer Stress:** Static water tables currently fluctuate between 40 to 60 feet below ground level (12.2 to 18.3 mbgl). Under current unregulated agricultural extraction (42 borewells energized on an 8-hour daily power rotation), the village risks localized aquifer exhaustion during the upcoming Rabi and Summer seasons.

---

### 2. Key Users, Decisions, and Operational Bottlenecks

| User Group | Operational Role | Key Decisions Faced Today | Failure Mode Today |
| :--- | :--- | :--- | :--- |
| **Small & Marginal Farmers** | Primary water consumers for Cash Crops (Cotton, Tur, Chana, Wheat) | • When to initiate Rabi sowing?<br>• Flood irrigation vs. skipping an irrigation cycle?<br>• How many acres can their single borewell support through March? | Flood irrigation applied blindly based on 8-hr power shift; borewells dry out mid-season, leading to total crop failure. |
| **Gram Panchayat & Water Cadre (Jal Sakhi)** | Custodians of community water supply & drinking borewells | • How to allocate shared groundwater between drinking tanks and farm pumping?<br>• Where to locate rainwater harvesting recharge structures? | Untreated tap water; zero measurement of static water levels; zero water budgeting. |
| **Panchayat Samiti / State Engineers (GSDA/MGNREGA)** | Technical sanctions for watershed works | • Selection of sites for percolation tanks and check dams under MGNREGA / VB-G RAM G. | Sites selected ad-hoc without hydrogeological soil infiltration maps, resulting in silted, non-percolating structures. |

---

### 3. Integration of ICAR-NBSS&LUP Soil Intelligence
A transformative element of this module is the integration of high-resolution soil survey data from the **ICAR National Bureau of Soil Survey and Land Use Planning (NBSS&LUP)**, headquartered in Nagpur.

Soil characteristics govern infiltration rates, deep percolation, and available water holding capacity (AWC):
1. **Linga Series (Typic Haplusterts - Deep Black Soil):**
   - High clay content (54%), high smectite mineralogy, high AWC (165 mm/m).
   - Infiltration rate: 5.2 mm/hr (very low).
   - *Hydro-Agronomic Implication:* Exceptional moisture retention for deep-rooted crops (Cotton, Pigeonpea), but highly prone to waterlogging and poor for artificial recharge ponds.
2. **Katol Series (Vertic Ustochrepts - Medium Black Soil):**
   - Silt-clay loam (42% clay), depth ~65 cm, AWC: 120 mm/m.
   - Infiltration rate: 10.5 mm/hr.
   - *Hydro-Agronomic Implication:* Primary cropland for Rabi Chana and Wheat; suitable for field bunding and contour trenches.
3. **Bhasma Upland Series (Lithic Ustorthents - Shallow Gravelly Basalt):**
   - Shallow depth (< 25 cm), high gravel content, high infiltration rate (> 32 mm/hr), low AWC (50 mm/m).
   - *Hydro-Agronomic Implication:* Non-arable for high-water crops; **critical priority zone for building percolation tanks, gabions, and aquifer recharge shafts**.

---

### 4. Government Schemes & Convergence Pathways
The module provides technical grounding to unlock public convergence funds:
- **Jal Jeevan Mission (JJM):** Mandates source sustainability for drinking water; requires strict separation of domestic aquifer zones from agricultural deep pumping.
- **Atal Bhujal Yojana (ABY):** Community-led groundwater management, water security plans (WSPs), and water budgeting.
- **Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop):** 55% subsidy for small/marginal farmers to shift from flood irrigation to micro-drip/sprinkler systems.
- **MGNREGA / VB-G RAM G Convergence:** Public works window (January–May 2027) to excavate prioritized recharge structures before the 2027 monsoon.

---

### 5. Profile of Partner Farmer Family: `Farmer-KB-01`

To ground the software in human reality, every algorithm is tested against an anonymized partner household:
- **Identifier:** `Farmer-KB-01`
- **Location:** South-West Agricultural Cluster, Katlabodi Village
- **Demographics:** 5 family members (3 dependent children); primary livelihood is 3.5 acres of ancestral land.
- **Soil Classification:** Katol Series (Vertic Ustochrepts, Medium Black Soil).
- **Water Infrastructure:** 
  - One open agricultural borewell drilled to 160 feet.
  - Current static water level: 52.0 feet (15.85 mbgl).
  - Pump: 5.0 HP electric submersible operating on an 8-hour rotational night shift (10:00 PM – 6:00 AM).
  - Borewell discharge rate: Dropped from 2.5 inches in July to 1.5 inches in October (~1.5 liters/second).
- **Current Seasonal Dilemma:**
  - Kharif cotton-tur crop harvested with a 30% yield penalty due to drought.
  - Farmer plans to sow 2.0 acres of Rabi Chana (Gram), requiring approximately 2,023 m³ of water over a 105-day cycle.
  - **The Core Decision:** At a discharge rate of 1.5 lps and 8 hours of intermittent power, can the borewell sustain 2.0 acres of Chana without depleting before the pod-filling stage in February?
  - **AquaGram Solution:** The module advises reducing flood-irrigated Chana to 1.2 acres or utilizing drip irrigation across the full 2.0 acres with a strict 4-hour daily pumping ceiling.

---

### 6. Architectural Contribution to UrjaGram DEVTech Platform
Within the larger DEVTech digital twin, AquaGram-Water feeds directly into:
- **Crop Planning (Vamsi):** Provides the sustainable water quota per acre.
- **Weather Integration (Vibhor):** Adjusts depletion curves using real-time IMD rainfall/temperature forecasts.
- **Solar Pumping (Devanshu):** Harmonizes pump draw rates with solar insolation curves.
- **NetZero Platform (Raj Patil):** Streams Scope 2 electricity pumping emissions (calculated via Central Electricity Authority baseline grid factor: 0.82 kg CO₂e/kWh) to compile Katlabodi’s comprehensive carbon balance.
