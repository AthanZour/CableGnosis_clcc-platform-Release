"""
Monitoring Module – Version 3.0.3
=================================

Demo Real-Time Monitoring Logic for Power Cable Applications
------------------------------------------------------------

This module implements a DEMO real-time monitoring view for a power cable
(e.g. HV / HVDC), intended for partner demonstrations and backend-ready UI
prototyping.

The implementation is GENERIC and NON-UCY-SPECIFIC:
any partner working on power cables, energy assets or similar infrastructure
could adopt the same logic and data flow.


------------------------------------------------------------
HIGH-LEVEL DESIGN OVERVIEW
------------------------------------------------------------

This monitoring module follows a SCADA-like, deterministic architecture:

1. Synthetic data are generated continuously (demo mode).
2. Raw samples are persisted to CSV files (one per metric).
3. Data are NORMALIZED and CLEANED on READ, not on write.
4. Aggregation and windowing are applied on a clean, time-consistent series.
5. Plotly figures are rebuilt from scratch on every refresh.

The design explicitly avoids:
- timing race conditions
- duplicated timestamps
- visual artifacts (double bars / stacking)
- dependency on refresh jitter


------------------------------------------------------------
TIME HANDLING (CRITICAL DESIGN DECISION)
------------------------------------------------------------

Raw data generation may produce:
- zero, one, or multiple samples per second
- due to callback timing jitter or backend behavior

Key principles:

- CSV timestamps have second-level resolution (HH:MM:SS).
- Multiple raw samples may exist for the same second.
- These raw samples are NOT plotted directly.

Normalization logic enforces:

1) Collapse all samples that fall in the SAME SECOND:
       → mean(value) per second
2) Resample to a STRICT 1-second grid:
       → resample("1S")
3) Forward-fill missing seconds:
       → ffill()

Result:
- EXACTLY one value per second
- No gaps
- No duplicated timestamps

This step is mandatory and prevents all known bar duplication artifacts.


------------------------------------------------------------
AGGREGATION LOGIC (1s / 2s / 5s)
------------------------------------------------------------

Aggregation is always applied AFTER per-second normalization.

Pipeline:

    Raw CSV
      → per-second mean
      → strict 1-second grid (resample + ffill)
      → OPTIONAL aggregation (2s / 5s windows)
      → tail(WINDOW_SIZE)
      → visualization

Important:
- Aggregation is TIME-BASED, not row-count-based.
- Refresh rate controls how often new samples are generated,
  NOT the correctness of aggregation.


------------------------------------------------------------
DATA PERSISTENCE (DEMO MODE)
------------------------------------------------------------

- Data are stored in CSV files (e.g. load, temperature).
- CSVs act as RAW INPUT buffers, not presentation-ready datasets.
- CSV files may be reset on monitoring startup to avoid legacy artifacts.
- File size is kept small (rolling window).

Data integrity guarantees:
- No NaN / null values are written.
- All values are forced numeric.
- Invalid generated values are replaced by safe fallback values.


------------------------------------------------------------
LOAD & TEMPERATURE MODELS
------------------------------------------------------------

Load model:
- Hybrid stochastic model:
    • Normal operating fluctuations around a base load.
    • Occasional higher-load "stress" events.
- Rate limiting is applied to avoid unrealistic jumps.

Temperature model:
- Temperature is derived from load (thermal dependency).
- Higher load → higher temperature.
- Changes are smoothed using a stricter rate limit to simulate
  thermal inertia.


------------------------------------------------------------
PLOTTING & VISUALIZATION (PLOTLY)
------------------------------------------------------------

Strict plotting rules:

- FULL figure replacement on every update.
- Exactly ONE bar trace per graph.
- No incremental updates.
- No trace reuse.
- No extendData.

Plotly is treated as a pure renderer:
    "This figure fully describes the graph state right now."

This guarantees:
- no stacked bars
- no ghost bars
- stable behavior across refresh rates


------------------------------------------------------------
TIME AXIS DISPLAY RULES
------------------------------------------------------------

For readability:

- First visible sample → full HH:MM:SS
- Minute change → full HH:MM:SS
- Intermediate samples → seconds only

This preserves temporal context without clutter.


------------------------------------------------------------
UI & TAB STRUCTURE NOTES
------------------------------------------------------------

Monitoring & KPIs Tab – Flask Popup Version (with wrapper):

- Vertical submenus under tabs
- Open Toolbox        → /toolbox
- Import Data         → /import
- PMU Settings        → /coordinates
- Power cable image (PNG/JPG) instead of SVG
- Clickable PMU coordinates
- CSS isolation via monitoring-tab wrapper


------------------------------------------------------------
INTENDED USAGE & EXTENSIBILITY
------------------------------------------------------------

This module is DEMO-oriented but backend-ready.

Safe future extensions:
- Replace CSV reads with API calls (same normalization logic).
- Replace synthetic generators with real measurements.
- Add EMA / smoothing after normalization.
- Add alert thresholds and KPIs.

DO NOT:
- Plot raw CSV rows directly.
- Remove per-second normalization.
- Tie correctness to refresh timing.


------------------------------------------------------------
END OF DESIGN NOTES – Monitoring v3.0.3
------------------------------------------------------------
"""

"""
HVDC Operational Telemetry Validation & Alerting Tool (Service Tab)

Purpose (project-facing):
- Provides an operational, SCADA-like monitoring environment for HVDC cable
  systems, combining real-time telemetry visualization, data normalization,
  and KPI computation.
- Focuses on validation of measurement relevance, temporal consistency,
  and operational correctness of incoming data streams (e.g. PMU / SCADA).
- Supports early alerting and operator situational awareness by exposing
  clean, time-aligned signals and derived indicators.

Platform role:
- Acts as a bridge between WP4 monitoring concepts and platform-level
  operational usage, supporting WP5 validation and WP6 demonstration
  activities.
- Designed as an onboarding-ready tool, enabling gradual transition from
  synthetic/demo data to real field measurements without architectural changes.

Notes:
- This tool is not a workflow entry point, but a reusable operational
  capability provided by the platform.
"""
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from logic.data import _synth_series, _indicator, _chart
from pathlib import Path
import pandas as pd
from datetime import datetime
from utils.paths import MONITORING_DIR
import requests
from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

TAB_META = {
    "id": "svc-hvdc-operational-monitoring",

    "label": "HVDC Operational Telemetry Validation & Alerting",

    "type": "service",
    "order": 200,

    # Core monitoring WP + strong validation / demo usage
    "workpackages": ["WP4", "WP5", "WP6"],

    # This tool spans monitoring, awareness, and performance assessment
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
        "Cable Performance & Optimization"
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.3 (demo, backend-ready)",
    "status": "active"
}

TAB_PREFIX = "svc-hvdc-operational-monitoring"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "kpis", "label": "KPIs"},
        {"id": "realtime", "label": "Real-Time"},
        {"id": "pmu", "label": "PMU"},
    ],
}

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------

CSV_PATHS = {
    "load": MONITORING_DIR / "ucy_load.csv",
    "temp": MONITORING_DIR / "ucy_temp.csv",
}
WINDOW_SIZE = 30  # number of bars shown

RANGES = {
    "load": {"min": 0, "max": 1200, "unit": "A"},
    "temp": {"min": 20, "max": 90, "unit": "°C"},
}

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

def ensure_csv(metric):
    path = CSV_PATHS[metric]
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        df = pd.DataFrame(columns=["timestamp", "value"])
        df.to_csv(path, index=False)   

def reset_csvs():
    for path in CSV_PATHS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(columns=["timestamp", "value"])
        df.to_csv(path, index=False)
     
def generate_temp_from_load(current):
    """
    Thermal behaviour model:
    - High load  -> temperature increases
    - Medium    -> roughly stable
    - Low load  -> temperature decreases
    """
    r_load = RANGES["load"]
    r_temp = RANGES["temp"]

    # normalize load 0..1
    norm = current / r_load["max"] if r_load["max"] else 0

    # baseline operating temperature
    base = 55.0

    # dynamic adjustment (±15 °C)
    delta = (norm - 0.5) * 30.0

    temp = base + delta

    # clamp to physical limits
    return np.clip(temp, r_temp["min"], r_temp["max"])

def apply_rate_limit(prev, new, max_pct):
    if prev is None or prev == 0:
        return new
    max_delta = prev * max_pct
    return np.clip(new, prev - max_delta, prev + max_delta)

def generate_value(metric):
    r = RANGES[metric]

    if metric == "load":
        # base operating point
        base = 550

        # normal fluctuation
        normal = np.random.normal(500, 80)

        # occasional stress event (20% πιθανότητα)
        stress = 0
        if np.random.rand() < 0.2:
            stress = np.random.uniform(300, 400)

        value = base + normal + stress

        return np.clip(value, r["min"], r["max"])

    else:
        return np.random.uniform(r["min"], r["max"])


def load_data(metric, window_sec=1):
    ensure_csv(metric)
    path = CSV_PATHS[metric]

    df = pd.read_csv(path)

    if df.empty or "timestamp" not in df.columns or "value" not in df.columns:
        return pd.DataFrame(columns=["timestamp", "value"])

    # ------------------------------------------------------------------
    # Parse timestamp → datetime (assumes HH:MM:SS)
    # ------------------------------------------------------------------
    df = df.copy()
    df["dt"] = pd.to_datetime(df["timestamp"], format="%H:%M:%S", errors="coerce")
    df = df.dropna(subset=["dt", "value"])

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    # ------------------------------------------------------------------
    # 1) Collapse multiple samples per second → MEAN
    # ------------------------------------------------------------------
    df = (
        df.groupby("dt", as_index=True)["value"]
        .mean()
        .to_frame()
    )

    # ------------------------------------------------------------------
    # 2) Resample to EXACT 1-second grid
    #    Missing seconds → forward-fill
    # ------------------------------------------------------------------
    df = df.resample("1s").ffill()

    # ------------------------------------------------------------------
    # 3) Optional aggregation (2 sec / 5 sec)
    # ------------------------------------------------------------------
    if window_sec > 1:
        df = (
            df.resample(f"{window_sec}s")
              .mean()
        )

    # ------------------------------------------------------------------
    # 4) Final formatting
    # ------------------------------------------------------------------
    df = df.tail(WINDOW_SIZE)
    df["timestamp"] = df.index.strftime("%H:%M:%S")
    df = df.reset_index(drop=True)[["timestamp", "value"]]

    return df
    
import pandas as pd
import requests
from datetime import datetime

import pandas as pd
import requests
from datetime import datetime

def fetch_metric_df(metric: str, window_sec: int = 1) -> pd.DataFrame:
    """
    Fetch metric data from API and normalize it exactly like load_data().
    Returns DataFrame with columns: ["timestamp", "value"]
    """
    SERVER_BASE_URL = "http://127.0.0.1:8050"
    API_BASE = "/api/services/monitoring"
    try:
        r = requests.get(
            f"{SERVER_BASE_URL}{API_BASE}/{metric}",
            timeout=1
        )
        if not r.ok:
            return pd.DataFrame(columns=["timestamp", "value"])

        payload = r.json()

        t = payload.get("t", [])
        v = payload.get("v", [])

        if not t or not v:
            return pd.DataFrame(columns=["timestamp", "value"])

        # ------------------------------------------------------------------
        # Build DataFrame from API payload
        # ------------------------------------------------------------------
        df = pd.DataFrame({
            "timestamp": t,
            "value": v,
        })

    except Exception:
        return pd.DataFrame(columns=["timestamp", "value"])

    # ------------------------------------------------------------------
    # SAME CLEANING LOGIC AS load_data()
    # ------------------------------------------------------------------
    df = df.copy()

    # Parse timestamp → datetime (HH:MM:SS)
    df["dt"] = pd.to_datetime(
        df["timestamp"],
        format="%H:%M:%S",
        errors="coerce"
    )

    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.dropna(subset=["dt", "value"])

    if df.empty:
        return pd.DataFrame(columns=["timestamp", "value"])

    # ------------------------------------------------------------------
    # 1) Collapse duplicates per second → MEAN
    # ------------------------------------------------------------------
    df = (
        df.groupby("dt", as_index=True)["value"]
        .mean()
        .to_frame()
    )

    # ------------------------------------------------------------------
    # 2) Resample to EXACT 1-second grid → forward-fill
    # ------------------------------------------------------------------
    df = df.resample("1s").ffill()

    # ------------------------------------------------------------------
    # 3) Optional aggregation (2s / 5s)
    # ------------------------------------------------------------------
    if window_sec > 1:
        df = df.resample(f"{window_sec}s").mean()

    # ------------------------------------------------------------------
    # 4) Final formatting (IDENTICAL to load_data)
    # ------------------------------------------------------------------
    df = df.tail(WINDOW_SIZE)
    df["timestamp"] = df.index.strftime("%H:%M:%S")
    df = df.reset_index(drop=True)[["timestamp", "value"]]

    return df

def append_data(metric, value):
    ensure_csv(metric)

    if value is None or not np.isfinite(value):
        if metric == "load":
            value = np.random.uniform(400, 700)
        else:
            value = np.random.uniform(
                RANGES["temp"]["min"],
                RANGES["temp"]["max"],
            )

    ts = datetime.now().strftime("%H:%M:%S")
    path = CSV_PATHS[metric]

    with open(path, "a") as f:
        f.write(f"{ts},{float(value)}\n")


def build_figure(df, metric):
    """
    Build a CLEAN bar chart figure.
    - Always returns a BRAND NEW figure
    - Exactly ONE bar trace
    - No state, no accumulation
    """

    # --- guard: αν δεν έχουμε δεδομένα ---
    if df is None or df.empty or "timestamp" not in df.columns:
        now = datetime.now().strftime("%H:%M:%S")
        df = pd.DataFrame([[now, 0.0]], columns=["timestamp", "value"])

    # --- enforce schema & safety ---
    df = df.copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0.0)

    r = RANGES[metric]

    timestamps = df["timestamp"].astype(str).tolist()
    values = df["value"].astype(float).tolist()

    # ------------------------------------------------------------------
    # X-axis tick logic
    # ------------------------------------------------------------------
    tick_vals = []
    tick_text = []

    for i, ts in enumerate(timestamps):
        if i == 0:
            tick_vals.append(ts)
            tick_text.append(ts)                 # full HH:MM:SS
        elif ts.endswith(":00"):
            tick_vals.append(ts)
            tick_text.append(ts)                 # minute change
        else:
            tick_vals.append(ts)
            tick_text.append(ts[-2:])            # seconds only

    # ------------------------------------------------------------------
    # BUILD FIGURE (ONE TRACE ONLY)
    # ------------------------------------------------------------------
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=timestamps,
            y=values,
            marker=dict(
                color=values,
                colorscale=[
                    [0.0, "#2c7bb6"],   # blue
                    [0.5, "#abd9e9"],   # light blue
                    [0.75, "#fdae61"],  # orange
                    [1.0, "#d7191c"],   # red
                ],
                cmin=r["min"],
                cmax=r["max"],
                showscale=True,
                colorbar=dict(
                    orientation="h",
                    x=0.45,              # slightly left of center
                    xanchor="center",
                    y=-0.55,
                    len=0.75,
                ),
            ),
        )
    )

    # ------------------------------------------------------------------
    # LAYOUT
    # ------------------------------------------------------------------
    fig.update_layout(
        height=340,
        margin=dict(l=40, r=20, t=30, b=80),
        yaxis=dict(
            range=[r["min"], r["max"]],
            title=f"{metric.capitalize()} ({r['unit']})",
        ),
        xaxis=dict(
            title="Time",
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_text,
        ),
        bargap=0.15,
        paper_bgcolor="#fafafa",
        plot_bgcolor="#fafafa",
        showlegend=False,
    )

    return fig

reset_csvs()
# ----------------------------------------------------------------------------- 
# Layout 
# ----------------------------------------------------------------------------- 
def layout_content():
    return html.Div(
        className="monitoring-tab",
        children=[
            html.Div(
                className="monitoring-tab",
                children=[

                    # ===========================================================
                    # HVDC Monitoring & Diagnostic Center – Overview & KPIs
                    # ===========================================================
                    html.H3("HVDC Monitoring & Diagnostic Center (M&D)"),
                    html.P(
                        "Operational overview of HVDC cable telemetry, supporting "
                        "PMU-based validation, pre-fault awareness and demonstration "
                        "of monitoring concepts for long HVDC links.",
                        style={"color": "#444", "marginBottom": "12px"},
                    ),

                    html.H4("Operational Situation Overview – HVDC Link"),
                    html.P(
                        "High-level indicators summarising the operational status, "
                        "availability and telemetry quality of the monitored HVDC link. "
                        "KPIs are indicative and provided for demonstration purposes.",
                        style={"color": "#555", "marginBottom": "10px"},
                    ),

                    html.P(
                        "!Values are indicative and may come from synthetic / replayed streams; "
                        "the goal is to demonstrate the KPI logic and UI behaviour, not certified operational compliance.",
                        style={
                          "color": "#64748b",
                          "marginBottom": "10px",
                          "fontWeight": 550,   # ή "550"
                          "fontSize": "14px",
                        },
                    ),

                    # ===========================================================
                    # HVDC Telemetry Integrity & KPIs
                    # ===========================================================
                    html.H5("HVDC Telemetry Integrity & Validation KPIs"),
                    
                    html.P(
                        "Real-time assessment of HVDC telemetry integrity, indicating compliance "
                        "with strict data acquisition requirements. The primary indicator reflects "
                        "temporal consistency, jitter tolerance and communication latency across "
                        "the full set of collected measurements.",
                        style={"color": "#555", "marginBottom": "10px"},
                    ),
                    
                    html.Div(
                        [
                            html.Button("Compute Integrity Snapshot", id="mon-generate-btn", n_clicks=0),
                            html.Button(
                                "Open M&D Toolbox",
                                id="mon-open-toolbox",
                                n_clicks=0,
                                style={"marginLeft": "10px"},
                            ),
                            dcc.Checklist(
                                id="mon-show-chart",
                                options=[{"label": "Show integrity trend", "value": "show"}],
                                value=[],
                                style={"display": "inline-block", "marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "10px"},
                    ),
                    
                    # === PRIMARY KPI (existing indicator logic reused) ===
                    html.Div(
                        className="hvdc-integrity-indicator",
                        children=[
                            dcc.Graph(
                                id="mon-uptime-indicator",
                                className="hvdc-indicator-graph",
                                style={"height": "120px"},
                                config={"displayModeBar": False},
                            )
                        ],
                    ),
                    
                    # === SECONDARY STATIC INDICATORS (placeholders) ===
                    html.Div(
                        className="hvdc-kpi-strip",
                        children=[
                            html.Div(
                                [
                                    html.Div("Latency Compliance", className="hvdc-kpi-title"),
                                    html.Div("✔ Within limits", className="hvdc-kpi-value"),
                                ],
                                className="hvdc-kpi-box",
                            ),
                            html.Div(
                                [
                                    html.Div("Jitter Stability", className="hvdc-kpi-title"),
                                    html.Div("✔ Stable", className="hvdc-kpi-value"),
                                ],
                                className="hvdc-kpi-box",
                            ),
                            html.Div(
                                [
                                    html.Div("Timestamp Consistency", className="hvdc-kpi-title"),
                                    html.Div("100 %", className="hvdc-kpi-value"),
                                ],
                                className="hvdc-kpi-box",
                            ),
                            html.Div(
                                [
                                    html.Div("Packet Loss", className="hvdc-kpi-title"),
                                    html.Div("< 0.1 %", className="hvdc-kpi-value"),
                                ],
                                className="hvdc-kpi-box",
                            ),
                        ],
                    ),
                    
                    html.Div(
                        [dcc.Graph(id="mon-uptime-chart", style={"height": "300px"})],
                        id="mon-chart-wrap",
                        style={"display": "none"},
                    ),

                    dcc.Store(id="mon-popup-dummy"),

                    html.Hr(style={"margin": "30px 0"}),

                    # ===========================================================
                    # HVDC Link & PMU Context
                    # ===========================================================
                    html.H4("HVDC Link & PMU Context", style={"marginBottom": "10px"}),

                    html.P(
                        "Contextual view of the monitored HVDC link, including PMU "
                        "placement, nominal operating parameters and asset-level "
                        "information relevant for monitoring and diagnostics.",
                        style={"color": "#555", "marginBottom": "10px"},
                    ),

                    html.Div(
                        id="submenu-overlay",
                        n_clicks=0,
                        style={
                            "position": "fixed",
                            "top": 0,
                            "left": 0,
                            "width": "100vw",
                            "height": "100vh",
                            "background": "transparent",
                            "zIndex": 900,
                            "display": "none",
                        },
                    ),
                    
                    dcc.Store(
                        id="submenu-state",
                        data=None,   # ποιο submenu είναι ανοιχτό
                    ),
                    
                    # Ribbon Menu (SCADA-style interaction layer)
                    html.Div(
                        className="ribbon-container",
                        children=[
                            # --- M&D HOME TAB ---
                            html.Div(
                                className="ribbon-tab",
                                id="tab-home",
                                n_clicks=0,
                                children=[
                                    "M&D Home",
                                    html.Div(
                                        id="submenu-home",
                                        className="submenu",
                                        children=[
                                            html.Div("New Session", className="menu-item"),
                                            html.Div("Save Snapshot", className="menu-item"),
                                            html.Div("Open Session", className="menu-item"),
                                            html.Div("Exit", className="menu-item"),
                                        ],
                                    ),
                                ],
                            ),
                            # --- TELEMETRY DATA TAB ---
                            html.Div(
                                className="ribbon-tab",
                                id="tab-data",
                                n_clicks=0,
                                children=[
                                    "Telemetry Data",
                                    html.Div(
                                        id="submenu-data",
                                        className="submenu",
                                        children=[
                                            html.Div("Ingest Telemetry", className="menu-item", id="data-import"),
                                            html.Div("Export Snapshot", className="menu-item"),
                                        ],
                                    ),
                                ],
                            ),
                            # --- LINK VIEW TAB ---
                            html.Div(
                                className="ribbon-tab",
                                id="tab-view",
                                n_clicks=0,
                                children=[
                                    "Link View",
                                    html.Div(
                                        id="submenu-view",
                                        className="submenu",
                                        children=[
                                            html.Div("Zoom In", className="menu-item"),
                                            html.Div("Zoom Out", className="menu-item"),
                                        ],
                                    ),
                                ],
                            ),
                            # --- PMU / PDC SETTINGS TAB ---
                            html.Div(
                                className="ribbon-tab",
                                id="tab-settings",
                                n_clicks=0,
                                children=[
                                    "PMU / PDC Settings",
                                    html.Div(
                                        id="submenu-settings",
                                        className="submenu",
                                        children=[
                                            html.Div("PMU Configuration", className="menu-item", id="settings-pmu"),
                                            html.Div("Display Options", className="menu-item"),
                                            html.Div("System Information", className="menu-item"),
                                        ],
                                    ),
                                ],
                            ),
                            # --- PMU SELECTOR ---
                            html.Div(
                                [
                                    html.Label("Active PMU:", style={"marginRight": "6px"}),
                                    dcc.Dropdown(
                                        id="ucy-pmu-select",
                                        options=[
                                            {"label": "PMU #1", "value": "pmu1"},
                                            {"label": "PMU #2", "value": "pmu2"},
                                        ],
                                        value="pmu1",
                                        clearable=False,
                                        style={"width": "150px"},
                                    ),
                                ],
                                style={"marginLeft": "auto", "display": "flex", "alignItems": "center"},
                            ),
                        ],
                    ),

                    # HVDC Link Visualisation
                    html.Div(
                        className="cable-container",
                        children=[
                            html.Img(src="/assets/pmu_left.png", className="pmu-icon left"),
                            html.Img(src="/assets/hvdc_line.png", className="cable-img"),
                            html.Img(src="/assets/pmu_right.png", className="pmu-icon right"),
                        ],
                    ),


                    
                    
                    # ===========================================================
                    # Real-Time HVDC Telemetry Monitoring
                    # ===========================================================
                    html.H4("Real-Time HVDC Telemetry Streams", style={"marginTop": "20px"}),

                    html.Div(
                        style={"margin": "20px 0"},
                        children=[
                            html.Div(
                                style={"display": "flex", "gap": "20px", "alignItems": "center"},
                                children=[
                                    dcc.Dropdown(
                                        id="rt-metric",
                                        options=[
                                            {"label": "Conductor Loading (A)", "value": "load"},
                                            {"label": "Estimated Cable Temperature (°C)", "value": "temp"},
                                        ],
                                        value="load",
                                        clearable=False,
                                        style={"width": "260px"},
                                    ),
                                    dcc.Dropdown(
                                        id="rt-refresh",
                                        options=[
                                            {"label": "1s sampling", "value": 1000},
                                            {"label": "2s sampling", "value": 2000},
                                            {"label": "5s sampling", "value": 5000},
                                        ],
                                        value=1000,
                                        clearable=False,
                                        style={"width": "180px"},
                                    ),
                                    html.Div(id="rt-clock", style={"fontWeight": "bold"}),
                                ],
                            ),

                            dcc.Graph(id="rt-graph"),

                            html.Div(
                                id="rt-minmax",
                                style={"marginTop": "8px", "color": "red"},
                            ),

                            dcc.Interval(id="rt-interval", interval=1000, n_intervals=0),
                        ],
                    ),

                    dcc.Store(
                        id="pmu-live-buffer",
                        data=[],
                    ),
                    dcc.Interval(
                        id="pmu-live-interval",
                        interval=1000,  # 300 ms
                        n_intervals=0,
                    ),
                                        
                    # ===========================================================
                    # PMU Telemetry Stream (Demo)
                    # ===========================================================
                    html.H4("PMU Telemetry Stream (Demo)", style={"marginTop": "20px"}),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(
                                        html.A(
                                            "PMU Coordinates: (34.700123, 33.312345)",
                                            id="pmu-coords-display",
                                            href="https://www.google.com/maps?q=34.700123,33.312345",
                                            target="_blank",
                                            style={"color": "#0044cc", "textDecoration": "none"},
                                        )
                                    ),
                                    html.P("Nominal Voltage Level: 132 kV"),
                                    html.P("Operating Current: 450 A"),
                                    html.P("Grid Frequency: 50 Hz"),
                                ],
                                className="pmu-info",
                            ),
                            html.Div(
                                [
                                    html.Button("Generate / Refresh Telemetry", id="ucy-gen-btn", n_clicks=0),
                                    dcc.Graph(
                                        id="ucy-data-graph",
                                        style={"height": "320px", "marginTop": "10px"},
                                    ),
                                ],
                                className="pmu-chart",
                            ),
                        ],
                        style={"padding": "10px"},
                    ),
                ],
                style={"padding": "20px"},
            )
        ],
        style={"padding": "20px"},
    )

def layout():
    return menu_layout()
# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------
def register_callbacks(app):
    
    
    @app.callback(
        Output("rt-interval", "interval"),
        Input("rt-refresh", "value"),
    )
    def update_interval(val):
        return val

    @app.callback(
        [
            Output("rt-graph", "figure"),
            Output("rt-minmax", "children"),
            Output("rt-clock", "children"),
        ],
        Input("rt-interval", "n_intervals"),
        State("rt-metric", "value"),
        State("rt-refresh", "value"),
    )
    
    def update_realtime(_, metric, refresh_ms):
        # === LOAD ===
        df_load = load_data("load")
        prev_load = df_load["value"].iloc[-1] if not df_load.empty else None
    
        raw_load = generate_value("load")
        load_val = apply_rate_limit(prev_load, raw_load, 0.05)
        append_data("load", load_val)
    
        # === TEMP ===
        df_temp = load_data("temp")
        prev_temp = df_temp["value"].iloc[-1] if not df_temp.empty else None
    
        raw_temp = generate_temp_from_load(load_val)
        temp_val = apply_rate_limit(prev_temp, raw_temp, 0.02)
        append_data("temp", temp_val)
    
        # === DISPLAY ===
        # window_sec = max(1, refresh_ms // 1000)
        # df = load_data(metric, window_sec=window_sec)
        df = fetch_metric_df(metric)
        # print(df)
        # df = fetch_metric_df(metric)
        fig = build_figure(df, metric)
    
        r = RANGES[metric]
        minmax = f"Min {metric}: {r['min']} {r['unit']} | Max {metric}: {r['max']} {r['unit']}"
        clock = datetime.now().strftime("%H:%M:%S")
    
        return fig, minmax, clock
    # KPI chart visibility
    @app.callback(Output("mon-chart-wrap", "style"), Input("mon-show-chart", "value"))
    def toggle_chart(show_vals):
        return {"display": "block"} if "show" in show_vals else {"display": "none"}

    # Generate KPI & chart
    @app.callback(
        [Output("mon-uptime-indicator", "figure"),
         Output("mon-uptime-chart", "figure")],
        Input("mon-generate-btn", "n_clicks"),
    )
    def generate_kpi(n):
        df = _synth_series(days=7 if n else 30, freq_per_day=24)
        last_val = float(round(df["value"].iloc[-1], 2))
    
        fig_indicator = _indicator(last_val)
    
        # 🔴 PATCH: override Indicator title (semantic relabeling)
        fig_indicator.update_traces(
            title={
                "text": (
                    "Real-Time Telemetry Integrity<br>"
                    "<span style='font-size:12px;color:#666'>"
                    "Temporal consistency • Jitter • Latency compliance"
                    "</span>"
                )
            }
        )
    
        return fig_indicator, _chart(df)

    @app.callback(
        [
            Output("ucy-data-graph", "figure"),
            Output("pmu-live-buffer", "data"),
        ],
        Input("pmu-live-interval", "n_intervals"),
        State("pmu-live-buffer", "data"),
    )
    def update_pmu_stream(_, buffer):
        from datetime import datetime, timedelta
        import plotly.graph_objects as go
        import random
    
        # -------------------------------------------------
        # INIT: create 100 time points, 1 per second
        # -------------------------------------------------
        if not buffer:
            now = datetime.now()
            start = now - timedelta(seconds=99)
    
            y = random.uniform(8, 12)
            buffer = []
    
            for i in range(100):
                y += random.uniform(-0.4, 0.6)
                buffer.append({
                    "x": start + timedelta(seconds=i),  # datetime ONLY
                    "y": y,
                })
    
        else:
            # -------------------------------------------------
            # Shift window: drop first, append one new
            # -------------------------------------------------
            last_y = buffer[-1]["y"]
            new_y = last_y + random.uniform(-0.4, 0.6)
    
            now = datetime.now()
    
            buffer = buffer[1:] + [{
                "x": now,   # always NOW
                "y": new_y,
            }]
    
        # -------------------------------------------------
        # Build figure
        # -------------------------------------------------
        xs = [p["x"] for p in buffer]
        ys = [p["y"] for p in buffer]
    
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line=dict(color="#2c3e50", width=2),
            )
        )
    
        fig.update_layout(
            title="Synthetic PMU Data Stream (live demo)",
            xaxis=dict(
                type="date",
                tickformat="%H:%M:%S",
                tickmode="array",
                tickvals=[xs[i] for i in (0, 25, 50, 75, 99)],
            ),
            yaxis=dict(title="Value"),
            margin=dict(l=40, r=20, t=40, b=40),
            paper_bgcolor="#fafafa",
            plot_bgcolor="#fafafa",
            showlegend=False,
        )
    
        return fig, buffer

    @app.callback(
        [
            Output("submenu-home", "style"),
            Output("submenu-data", "style"),
            Output("submenu-view", "style"),
            Output("submenu-settings", "style"),
            Output("submenu-overlay", "style"),
            Output("submenu-state", "data"),
        ],
        [
            Input("tab-home", "n_clicks"),
            Input("tab-data", "n_clicks"),
            Input("tab-view", "n_clicks"),
            Input("tab-settings", "n_clicks"),
            Input("submenu-overlay", "n_clicks"),  # 👈 click outside
        ],
        State("submenu-state", "data"),
    )
    def toggle_submenus(h, d, v, s, overlay_clicks, open_menu):
        ctx = dash.callback_context
    
        hidden = {"display": "none"}
        visible = {"display": "flex", "flexDirection": "column"}
        overlay_on = {
            "display": "block",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100vw",
            "height": "100vh",
            "zIndex": 900,
        }
    
        if not ctx.triggered:
            return hidden, hidden, hidden, hidden, hidden, None
    
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    
        mapping = {
            "tab-home": "home",
            "tab-data": "data",
            "tab-view": "view",
            "tab-settings": "settings",
        }
    
        # 👉 Click έξω
        if trigger == "submenu-overlay":
            return hidden, hidden, hidden, hidden, hidden, None
    
        clicked_menu = mapping.get(trigger)
    
        # toggle ίδιο tab
        if open_menu == clicked_menu:
            return hidden, hidden, hidden, hidden, hidden, None
    
        styles = {
            "home": hidden,
            "data": hidden,
            "view": hidden,
            "settings": hidden,
        }
    
        styles[clicked_menu] = visible
    
        return (
            styles["home"],
            styles["data"],
            styles["view"],
            styles["settings"],
            overlay_on,
            clicked_menu,
        )

    
    # Open Toolbox
    app.clientside_callback(
        """
        function(n_clicks){
            if(!n_clicks) return null;
            window.open('/toolbox','ToolboxWindow',
                        'width=600,height=400,left=200,top=200,resizable=yes,scrollbars=yes');
            return 'opened';
        }
        """,
        Output("mon-popup-dummy", "data"),
        Input("mon-open-toolbox", "n_clicks"),
        prevent_initial_call=True,
    )

    # Import Data popup
    app.clientside_callback(
        """
        function(n_clicks){
            if(!n_clicks) return null;
            window.open('/import','ImportWindow',
                        'width=600,height=500,left=250,top=200,resizable=yes,scrollbars=yes');
            return 'opened';
        }
        """,
        Output("submenu-data", "title"),
        Input("data-import", "n_clicks"),
        prevent_initial_call=True,
    )

    # PMU Settings popup
    app.clientside_callback(
        """
        function(n_clicks){
            if(!n_clicks) return null;
            window.open('/coordinates','CoordWindow',
                        'width=500,height=400,left=280,top=220,resizable=yes,scrollbars=yes');
            return 'opened';
        }
        """,
        Output("submenu-settings", "title"),
        Input("settings-pmu", "n_clicks"),
        prevent_initial_call=True,
    )
    
    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)

