from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time
import numpy as np
import pandas as pd

import shutil
from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils.paths import PARTNER_DATA_DIR
from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

"""
HVDC Data Utilization & Validation Analytics (Demo / Review-Safe)

What this tool is (today):
- A lightweight, review-facing analytics playground that visualises *indicative* dataset integration
  and *demo* metrics using synthetic / placeholder streams.
- It is meant to show how the platform will expose data-integration visibility and “readiness cues”
  before deeper monitoring / diagnostics tools are opened.

What this tool is NOT (today):
- It does NOT certify validation outcomes, does NOT provide pass/fail verdicts,
  and does NOT claim that pilot validation procedures have been executed (WP6 execution starts later).

How to interpret the views:
- Pie / Sankey / correlation blocks are demonstrators of “what will be measured and inspected”
  as partner/pilot datasets mature, rather than a completed validation workflow.

Why it is useful for M18:
- Shows a coherent *evidence navigation concept* for data integration: “what data exists, how it flows,
  and which cues will later support validation packaging” (without asserting final results).
"""

# ---------------------------------------------------------------------
# SERVICE METADATA OPTIONS
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-hvdc-data-utilization-validation",
    "label": "HVDC Data Utilization & Validation Analytics",
    "type": "service",

    # Keep close to other analytics services
    "order": 201,

    # Originates in monitoring tasks, used for validation and demos
    "workpackages": ["WP4", "WP5", "WP6"],

    # Cross-cutting by nature
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
        "Cable Performance & Optimization"
    ],

    # Not structured yet
    "subcategories": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

# -----------------------------
# Demo dataset configuration
# -----------------------------
DATA_DIR = PARTNER_DATA_DIR
DATA_DIR.mkdir(parents=True, exist_ok=True)

# We'll generate/append a few small CSVs and always read the latest N files
CSV_PREFIX = "partner_cable_metrics"
NUM_FILES = 5
ROWS_PER_FILE = 60

# Cable-relevant dummy metrics (common HV cable insulation / construction indicators)
# (names are for demo; units are indicative)
CABLE_METRICS = [
    ("insulation_thickness_mm", "Insulation thickness (mm)"),
    ("insulation_layers", "Insulation layers (#)"),
    ("relative_permittivity_epsr", "Relative permittivity εr (-)"),
    ("dielectric_strength_kv_per_mm", "Dielectric strength (kV/mm)"),
    ("tan_delta", "Dielectric loss (tanδ) (-)"),
    ("volume_resistivity_ohm_cm", "Volume resistivity (Ω·cm)"),
]

TAB_PREFIX = "svc-hvdc-data-utilization-validation"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "kpis", "label": "KPIs"},
        {"id": "realtime", "label": "Real-Time"},
        {"id": "pmu", "label": "PMU"},
    ],
}

def _metric_keys() -> list[str]:
    return [k for k, _ in CABLE_METRICS]


def _metric_label(key: str) -> str:
    for k, lbl in CABLE_METRICS:
        if k == key:
            return lbl
    return key


def _get_tz_display() -> str:
    now = datetime.now().astimezone()

    # UTC offset
    offset_sec = now.utcoffset().total_seconds()
    hours = int(offset_sec // 3600)
    minutes = int((offset_sec % 3600) // 60)
    sign = "+" if hours >= 0 else "-"
    offset = f"UTC{sign}{abs(hours):02d}:{abs(minutes):02d}"

    # DST / Standard
    is_dst = time.localtime().tm_isdst > 0
    season = "Daylight Saving Time" if is_dst else "Standard Time"

    # Controlled timezone short code (NO locale dependency)
    if hours == 2 and not is_dst:
        tz_code = "EET"
    elif hours == 3 and is_dst:
        tz_code = "EEST"
    else:
        tz_code = "Local"

    return f"{offset} ({season} | {tz_code})"


def _csv_path(idx: int) -> Path:
    return PARTNER_DATA_DIR / f"{CSV_PREFIX}.{idx}.csv"


def _rotate_files_if_needed(max_rows_per_file: int = 100) -> None:
    """
    Keep files small:
    - We write to the "latest" file (highest index that exists, else 1).
    - If it's above max_rows_per_file, we rotate (increment index up to NUM_FILES, then shift).
    """
    # Determine current file index
    existing = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
    if not existing:
        # create first file
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(1), index=False)
        return

    # latest by numeric suffix
    def _idx(p: Path) -> int:
        try:
            return int(p.stem.split(".")[-1])
        except Exception:
            return 1

    existing = sorted(existing, key=_idx)
    latest = existing[-1]
    latest_idx = _idx(latest)

    # If latest too large, rotate
    try:
        rows = sum(1 for _ in open(latest, "r", encoding="utf-8")) - 1  # minus header
    except Exception:
        rows = max_rows_per_file + 1

    if rows <= max_rows_per_file:
        return

    # rotation: if we already have NUM_FILES, shift down (2->1, 3->2, ...)
    if latest_idx >= NUM_FILES:
        # rotate DOWNWARDS to avoid overwrite (Windows-safe)
        for i in range(NUM_FILES - 1, 0, -1):
            src = _csv_path(i)
            dst = _csv_path(i - 1)
            if src.exists():
                try:
                    if dst.exists():
                        dst.unlink()  # remove destination first
                    shutil.move(src, dst)
                except (PermissionError, FileExistsError, FileNotFoundError):
                    return
        # new latest becomes NUM_FILES
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(NUM_FILES), index=False)
    else:
        # create next file
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(latest_idx + 1), index=False)


def _generate_dummy_frame(n: int) -> pd.DataFrame:
    """
    Generates cable-like dummy metrics with some realistic-ish ranges and correlations.
    Not meant to be physically exact; just plausible demo data.
    """
    rng = np.random.default_rng()

    insulation_thickness = rng.normal(25, 4, n).clip(12, 40)
    layers = rng.integers(3, 8, n)

    epsr = rng.normal(2.4, 0.12, n).clip(2.0, 3.0)

    diel_strength = (rng.normal(32, 4, n) + (epsr - 2.4) * (-6)).clip(18, 45)

    tan_delta = np.abs(rng.normal(3e-4, 2e-4, n)).clip(5e-5, 3e-3)

    log_rho = rng.normal(16.5, 0.7, n)
    rho = (10 ** log_rho).clip(1e12, 1e19)

    df = pd.DataFrame(
        {
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * n,
            "insulation_thickness_mm": insulation_thickness,
            "insulation_layers": layers.astype(float),
            "relative_permittivity_epsr": epsr,
            "dielectric_strength_kv_per_mm": diel_strength,
            "tan_delta": tan_delta,
            "volume_resistivity_ohm_cm": rho,
        }
    )
    return df


def _read_last_files(n_files: int = 2) -> pd.DataFrame:
    """
    Read the last n_files (by index) and merge them.
    """
    paths = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
    if not paths:
        return pd.DataFrame(columns=["timestamp"] + _metric_keys())

    def _idx(p: Path) -> int:
        try:
            return int(p.stem.split(".")[-1])
        except Exception:
            return 0

    paths = sorted(paths, key=_idx)[-n_files:]
    frames = []
    for p in paths:
        try:
            df = pd.read_csv(p)
            frames.append(df)
        except Exception:
            continue

    if not frames:
        return pd.DataFrame(columns=["timestamp"] + _metric_keys())

    df_all = pd.concat(frames, ignore_index=True)
    for k in _metric_keys():
        df_all[k] = pd.to_numeric(df_all.get(k, np.nan), errors="coerce")
    df_all = df_all.dropna(subset=_metric_keys(), how="any")
    return df_all


# -----------------------------
# Figures
# -----------------------------
def _make_pie_fig(seed: int | None = None) -> go.Figure:
    rng = np.random.default_rng(seed)

    labels = ["MQTT", "REST", "OPC UA", "IEC 61850 (mock)"]
    values = rng.integers(10, 50, size=len(labels))
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.45,
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        title="Integration Protocol Mix (Demo)",
    )
    return fig


def _make_sankey_fig(seed: int | None = None) -> go.Figure:
    rng = np.random.default_rng(seed)

    nodes = [
        "Devices (demo)",
        "Edge Gateway (demo)",
        "Partner API (demo)",
        "Data Lake (demo)",
        "Analytics (demo)",
        "Dashboard (demo)",
    ]
    links = [
        (0, 1, int(rng.integers(20, 60))),
        (1, 2, int(rng.integers(10, 50))),
        (2, 3, int(rng.integers(10, 50))),
        (3, 4, int(rng.integers(10, 50))),
        (4, 5, int(rng.integers(10, 50))),
        (1, 5, int(rng.integers(5, 20))),
    ]
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    label=nodes,
                    pad=15,
                    thickness=18,
                ),
                link=dict(
                    source=[s for s, t, v in links],
                    target=[t for s, t, v in links],
                    value=[v for s, t, v in links],
                ),
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        title="Data Integration Path (Demo)",
    )
    return fig


def _make_corr_heatmap(df: pd.DataFrame, order: list[str]) -> go.Figure:
    cols = [c for c in order if c in df.columns]
    if len(cols) < 2 or df.empty:
        fig = go.Figure()
        fig.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            title="Correlation Map (Demo)",
        )
        return fig

    corr = df[cols].corr(method="pearson")

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=[_metric_label(c) for c in corr.columns],
            y=[_metric_label(c) for c in corr.index],
            zmin=-1,
            zmax=1,
            colorscale="RdBu",
            hovertemplate="X: %{x}<br>Y: %{y}<br>Corr: %{z:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        title="Correlation Map (Demo)",
    )
    return fig


def _dropdown_options(disable_key: str | None = None) -> list[dict]:
    opts = []
    for k, lbl in CABLE_METRICS:
        opts.append(
            {
                "label": lbl,
                "value": k,
                "disabled": (disable_key == k),
            }
        )
    return opts


# -----------------------------
# Layout
# -----------------------------
def layout_content():
    tz = _get_tz_display()

    return html.Div(
        className="partner-tab hvdc-duv-tab",
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
                children=[
                    html.H3("HVDC Data Integration & Utilization (Demo)", className="tab-title"),
                    dbc.Badge(f"Timezone: {tz}", color="info", pill=True, style={"fontSize": "0.95rem"}),
                ],
            ),

            # Optional visual placeholder (review-safe) — purely descriptive
            html.Div(
                className="hvdc-duv-hero",
                children=[
                    html.Div(
                        className="hvdc-duv-hero-img",
                        style={
                            "backgroundImage": "url('/assets/tabs_hero_images/svc_hvdc_data_utilization_validation_hero_image.jpg')",
                            "backgroundSize": "cover",
                            "backgroundPosition": "center",
                            "backgroundRepeat": "no-repeat",
                        },
                    ),
                    html.Div(
                        className="hvdc-duv-hero-txt",
                        children=[
                            html.H4("What you see here (M18-ready framing)"),
                            html.Ul(
                                [
                                    html.Li("An indicative view of how partner/pilot datasets will be exposed and inspected."),
                                    html.Li("Demo visuals showing integration visibility (not a completed validation workflow)."),
                                    html.Li("Future extensions: richer evidence markers and cross-tool hand-offs as pilots mature."),
                                ]
                            ),
                            html.P(
                                "Note: Values and flows shown below are demonstrators (synthetic/placeholder) to communicate intended capabilities without claiming pass/fail validation outcomes.",
                                className="hvdc-duv-note",
                            ),
                        ],
                    ),
                ],
            ),

            # Top row: Pie + Sankey with a refresh button (NO routes)
            dbc.Row(
                className="mt-2",
                children=[
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Div(
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                                        children=[
                                            html.Span("Integration Snapshot (Demo)"),
                                            dbc.Button("Refresh (demo)", id="partner-refresh-btn", n_clicks=0, color="primary", size="sm"),
                                        ],
                                    ),
                                    style={"background": "#eef6ff"},
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="partner-pie",
                                        figure=_make_pie_fig(seed=1),
                                        config={"displayModeBar": False},
                                    )
                                ),
                            ],
                            style={"borderRadius": "10px"},
                        ),
                        md=5,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Integration Path (Demo)", style={"background": "#fff3e6"}),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="partner-sankey",
                                        figure=_make_sankey_fig(seed=1),
                                        config={"displayModeBar": False},
                                    )
                                ),
                            ],
                            style={"borderRadius": "10px"},
                        ),
                        md=7,
                    ),
                ],
            ),

            html.Div(
                className="partner-controls",
                children=[
                    html.Div(
                        [
                            html.Img(src="/assets/iot_device.png", className="partner-icon"),
                            html.H4("Devices & Interfaces (Demo)"),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Select Device (placeholder):"),
                            dcc.Dropdown(
                                id="device-dropdown",
                                options=[
                                    {"label": "UCY Thermal Node (demo)", "value": "UCY-001"},
                                    {"label": "UoS Strain Sensor (demo)", "value": "UOS-002"},
                                    {"label": "IWO Magnetic Probe (demo)", "value": "IWO-003"},
                                ],
                                value="UCY-001",
                                className="device-dropdown",
                            ),
                            html.Button("↻ Refresh (demo)", id="device-refresh-btn", n_clicks=0, className="action-button"),
                        ]
                    ),
                ],
            ),

            html.Div(
                id="device-info",
                className="device-info",
                children=[
                    html.H4("Device Information (Demo)"),
                    html.P("Select a device and click refresh to view placeholder details."),
                ],
            ),

            html.Div(
                id="system-summary",
                className="system-summary",
                children=[
                    html.H4("Summary (Demo)"),
                    html.Ul(
                        [
                            html.Li("Active devices shown: 3 (placeholder)"),
                            html.Li("Alerts shown: 0 (placeholder)"),
                            html.Li("Interfaces: MQTT / REST / OPC UA (demo)"),
                            html.Li("Purpose: integration visibility for review (not validation verdicts)"),
                        ]
                    ),
                ],
            ),

            dbc.Card(
                className="mt-3",
                style={"borderRadius": "10px"},
                children=[
                    dbc.CardHeader(
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                            children=[
                                html.Span("Cable Metrics Correlation (Demo)"),
                                dbc.Badge("hover a cell to see value", color="secondary", pill=True),
                            ],
                        ),
                        style={"background": "#f0f7f2"},
                    ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label("Metric A"),
                                            dcc.Dropdown(
                                                id="corr-metric-a",
                                                options=_dropdown_options(disable_key=None),
                                                value=CABLE_METRICS[0][0],
                                                clearable=False,
                                            ),
                                        ],
                                        md=5,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("Metric B"),
                                            dcc.Dropdown(
                                                id="corr-metric-b",
                                                options=_dropdown_options(disable_key=CABLE_METRICS[0][0]),
                                                value=CABLE_METRICS[1][0],
                                                clearable=False,
                                            ),
                                        ],
                                        md=5,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("\u00A0"),
                                            html.Div(
                                                [
                                                    dbc.Button("Show (demo)", id="corr-show-btn", n_clicks=0, color="success", className="me-2"),
                                                    dbc.Button("Refresh Data (demo)", id="corr-refresh-btn", n_clicks=0, color="warning"),
                                                ]
                                            ),
                                        ],
                                        md=2,
                                    ),
                                ],
                                className="g-2",
                            ),
                            html.Hr(),
                            dcc.Graph(
                                id="corr-heatmap",
                                figure=_make_corr_heatmap(pd.DataFrame(), order=_metric_keys()),
                                config={"displayModeBar": False},
                            ),
                            html.Div(
                                id="corr-footnote",
                                style={"fontSize": "0.9rem", "opacity": 0.8},
                                children="Tip: choose two metrics; the same metric is disabled in the other dropdown (demo behaviour).",
                            ),
                        ]
                    ),
                ],
            ),

            dcc.Store(id="partner-data-store"),
            dcc.Store(id="corr-data-seed-store"),
        ],
    )


def layout():
    return menu_layout()


# -----------------------------
# Callbacks
# -----------------------------
def register_callbacks(app):
    @app.callback(
        Output("partner-pie", "figure"),
        Output("partner-sankey", "figure"),
        Input("partner-refresh-btn", "n_clicks"),
        prevent_initial_call=False,
    )
    def refresh_partner_charts(n):
        seed = int(n or 0) + 1
        return _make_pie_fig(seed=seed), _make_sankey_fig(seed=seed)

    @app.callback(
        Output("device-info", "children"),
        Input("device-refresh-btn", "n_clicks"),
        State("device-dropdown", "value"),
        prevent_initial_call=False,
    )
    def refresh_device_info(n, device_id):
        device_id = device_id or "UCY-001"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            html.H4("Device Information (Demo)"),
            html.Ul(
                [
                    html.Li(f"Device ID: {device_id}"),
                    html.Li("Status: Online (demo)"),
                    html.Li("Sampling: 1 Hz (demo)"),
                    html.Li(f"Last refresh: {now}"),
                ]
            ),
        ]

    @app.callback(
        Output("corr-metric-b", "options"),
        Input("corr-metric-a", "value"),
    )
    def disable_in_b(metric_a):
        return _dropdown_options(disable_key=metric_a)

    @app.callback(
        Output("corr-metric-a", "options"),
        Input("corr-metric-b", "value"),
    )
    def disable_in_a(metric_b):
        return _dropdown_options(disable_key=metric_b)

    @app.callback(
        Output("corr-data-seed-store", "data"),
        Input("corr-refresh-btn", "n_clicks"),
        prevent_initial_call=False,
    )
    def refresh_corr_data(_):
        _rotate_files_if_needed(max_rows_per_file=100)
        paths = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
        if not paths:
            return {"ok": True, "ts": datetime.now().isoformat()}

        def _idx(p: Path) -> int:
            try:
                return int(p.stem.split(".")[-1])
            except Exception:
                return 1

        latest = sorted(paths, key=_idx)[-1]
        df_new = _generate_dummy_frame(ROWS_PER_FILE)
        df_new.to_csv(latest, mode="a", header=False, index=False)
        return {"ok": True, "ts": datetime.now().isoformat()}

    @app.callback(
        Output("corr-heatmap", "figure"),
        Input("corr-show-btn", "n_clicks"),
        State("corr-metric-a", "value"),
        State("corr-metric-b", "value"),
        State("corr-data-seed-store", "data"),
        prevent_initial_call=False,
    )
    def show_corr(n, metric_a, metric_b, _seed_state):
        _rotate_files_if_needed(max_rows_per_file=100)

        df_all = _read_last_files(n_files=2)

        if df_all.empty:
            df = _generate_dummy_frame(ROWS_PER_FILE)
            df.to_csv(_csv_path(1), index=False)
            df_all = _read_last_files(n_files=2)

        all_keys = _metric_keys()
        metric_a = metric_a or all_keys[0]
        metric_b = metric_b or all_keys[1]
        order = [metric_a, metric_b] + [k for k in all_keys if k not in (metric_a, metric_b)]

        return _make_corr_heatmap(df_all, order=order)

    register_tab_menu_callbacks(app, TAB_PREFIX)