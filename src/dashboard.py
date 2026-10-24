"""
Lightweight Web Dashboard for AquaGram-Water.
Zero external server dependencies (runs on Python's built-in http.server).
Provides live simulation, real-time gauges, Marathi voice/text advisory, and NetZero streams.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from .pipeline import AquaGramWaterPipeline

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AquaGramOS · Katlabodi Digital Twin</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b1320;
      --surface: #131f33;
      --card: #1c2b45;
      --primary: #0284c7;
      --accent: #38bdf8;
      --text: #f8fafc;
      --muted: #94a3b8;
      --border: #243552;
      --warn: #eab308;
      --danger: #ef4444;
      --success: #10b981;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--text); padding: 24px; }
    .container { max-width: 1200px; margin: 0 auto; }
    header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 24px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
    .brand h1 { font-size: 24px; font-weight: 700; color: #fff; }
    .brand span { font-size: 13px; color: var(--accent); letter-spacing: 0.05em; text-transform: uppercase; }
    .badge { padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 600; background: rgba(56, 189, 248, 0.1); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.3); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 24px; }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
    .card h3 { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
    .card .val { font-size: 28px; font-weight: 700; color: #fff; }
    .card .sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
    .status-box { padding: 16px; border-radius: 8px; font-weight: 600; margin-bottom: 24px; border-left: 4px solid; }
    .status-warning { background: rgba(234, 179, 8, 0.15); border-left-color: var(--warn); color: #fef08a; }
    .status-emergency { background: rgba(239, 68, 68, 0.15); border-left-color: var(--danger); color: #fca5a5; }
    .status-normal { background: rgba(16, 185, 129, 0.15); border-left-color: var(--success); color: #86efac; }
    .section-title { font-size: 16px; font-weight: 600; margin: 24px 0 12px; color: #e2e8f0; }
    .advisory-box { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-bottom: 24px; }
    .advisory-box h4 { color: var(--accent); font-size: 14px; margin-bottom: 6px; }
    .advisory-box p { font-size: 15px; line-height: 1.6; color: #cbd5e1; }
    .controls { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 24px; }
    .controls form { display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-end; }
    .field { display: flex; flex-direction: column; gap: 6px; }
    .field label { font-size: 12px; color: var(--muted); }
    .field input { background: var(--bg); border: 1px solid var(--border); color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 14px; width: 140px; }
    button { background: var(--primary); color: #fff; border: 0; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
    button:hover { background: #0369a1; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <span>UrjaGram Innovations · DEVTech Platform</span>
        <h1>AquaGramOS · Katlabodi Water Intelligence</h1>
      </div>
      <div class="badge">Pilot: Katlabodi, Katol, Nagpur</div>
    </header>

    <div class="controls">
      <form method="GET">
        <div class="field">
          <label>Water Table Depth (ft)</label>
          <input type="number" step="0.5" name="depth" value="{depth}">
        </div>
        <div class="field">
          <label>Rainfall (mm)</label>
          <input type="number" step="1" name="rain" value="{rain}">
        </div>
        <div class="field">
          <label>Dry Days</label>
          <input type="number" name="dry_days" value="{dry_days}">
        </div>
        <div class="field">
          <label>Pump Hours/Day</label>
          <input type="number" step="0.5" name="pump_hours" value="{pump_hours}">
        </div>
        <button type="submit">Run Simulation</button>
      </form>
    </div>

    <div class="status-box {status_class}">
      [SYSTEM STATUS] {status_code} — {action_directive}
      <div style="font-size:12px; font-weight:normal; margin-top:4px;">Safety Guardrail: {guardrail_status}</div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Current Water Table</h3>
        <div class="val">{wt_ft} ft</div>
        <div class="sub">{wt_mbgl} meters below ground</div>
      </div>
      <div class="card">
        <h3>Days of Water Left</h3>
        <div class="val" style="color: {days_color};">{days_left} Days</div>
        <div class="sub">At current extraction rate</div>
      </div>
      <div class="card">
        <h3>Usable Aquifer Storage</h3>
        <div class="val">{usable_storage} m³</div>
        <div class="sub">Dead storage cutoff: 120,000 m³</div>
      </div>
      <div class="card">
        <h3>Pumping Carbon (NetZero)</h3>
        <div class="val">{co2e_yr} tCO₂e/yr</div>
        <div class="sub">Scope 2 emissions for Raj's Ledger</div>
      </div>
    </div>

    <div class="section-title">Field Advisories (Dual AI: Gemini LLM + Jev)</div>
    <div class="advisory-box">
      <h4>मराठी शेतकरी सल्ला (Local Marathi Advisory for Farmer-KB-01)</h4>
      <p>{advisory_marathi}</p>
    </div>
    <div class="advisory-box">
      <h4>Technical Agronomic Summary (English)</h4>
      <p>{advisory_english}</p>
    </div>

    <div class="section-title">ICAR-NBSS&LUP Soil & Recharge Planning</div>
    <div class="grid">
      <div class="card">
        <h3>Soil Classification</h3>
        <div class="val" style="font-size:20px;">{soil_series}</div>
        <div class="sub">Water Capacity: {soil_awc} mm/m</div>
      </div>
      <div class="card">
        <h3>Recharge Recommendation</h3>
        <div class="val" style="font-size:20px;">{recharge_struct}</div>
        <div class="sub">Scheme: {convergence}</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    pipeline = AquaGramWaterPipeline()

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        depth = float(query.get("depth", [51.8])[0])
        rain = float(query.get("rain", [0.0])[0])
        dry_days = int(query.get("dry_days", [18])[0])
        pump_hours = float(query.get("pump_hours", [8.0])[0])

        res = self.pipeline.run_assessment(
            current_water_table_ft=depth,
            daily_rainfall_mm=rain,
            consecutive_dry_days=dry_days,
            active_pump_hours=pump_hours
        )

        status_code = res["status_code"]
        if "EMERGENCY" in status_code:
            s_class = "status-emergency"
            d_color = "#ef4444"
        elif "WARNING" in status_code:
            s_class = "status-warning"
            d_color = "#eab308"
        else:
            s_class = "status-normal"
            d_color = "#10b981"

        m = res["metrics"]
        s = res["soil_and_recharge"]
        b = res["bilingual_advisory"]
        nz = res["netzero_stream"]

        html = HTML_TEMPLATE.format(
            depth=depth,
            rain=rain,
            dry_days=dry_days,
            pump_hours=pump_hours,
            status_class=s_class,
            status_code=status_code,
            action_directive=res["action_directive"],
            guardrail_status=res["guardrail_status"],
            wt_ft=m["water_table_depth_ft"],
            wt_mbgl=m["water_table_depth_mbgl"],
            days_left=m["days_of_water_remaining"],
            days_color=d_color,
            usable_storage=f"{m['usable_storage_m3']:,.0f}",
            co2e_yr=nz["annual_emissions_tco2e_per_year"],
            advisory_marathi=b["marathi_farmer"],
            advisory_english=b["english_technical"],
            soil_series=s["soil_series"],
            soil_awc=s["available_water_capacity_mm_m"],
            recharge_struct=s["recommended_recharge_structure"],
            convergence=s["convergence_opportunity"]
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

def run_server(port=8080):
    server = HTTPServer(("0.0.0.0", port), DashboardHandler)
    print(f"\n[AQUAGRAM DASHBOARD] Running live at: http://localhost:{port}")
    print("Press Ctrl+C to stop.\n")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
