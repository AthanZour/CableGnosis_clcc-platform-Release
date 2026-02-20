"""
CABLEGNOSIS Data Timeline Tab (Tab 5)
=====================================
Enhanced interactive timeline module for the CABLEGNOSIS demo platform.

Features:
----------
1. **Chart Type** – Bar / Line / Area selection
2. **Timescale** – 1Y / 3Y / 5Y / 10Y / MAX
3. **Generate & Auto Update** controls
4. Hover + Brush interactivity

All text elements are now in English and aligned with the CABLEGNOSIS
Life Cycle Center visual identity.
"""

import dash
from dash import dcc, html, Input, Output, State, ctx  # <-- add State here
import plotly.graph_objects as go
from pathlib import Path
from logic.synthetic_dataset_generator import generate_synthetic_dataset
from utils.paths import TIMELINE_DIR

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHART_TYPES = {
    "bar": "Bar Chart",
    "line": "Line Chart",
    "area": "Area Chart",
}

TIMESCALES = {
    "1Y": 365,
    "3Y": 365 * 3,
    "5Y": 365 * 5,
    "10Y": 365 * 10,
    "MAX": None,
}


def _generate_df(duration_days: int = 365 * 10):
    """Generate synthetic daily data for demonstration."""
    return generate_synthetic_dataset(
        mode="random",
        num_points=None,
        frequency_per_day=1,
        duration_days=duration_days,
        num_sinusoids=8,
        max_amplitude=60,
        max_dc_offset=20,
        noise_min=-5,
        noise_max=40,
        clip_min=-50,
        clip_max=150,
        save_path = TIMELINE_DIR / "interactive_tab_dataset.json",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_tab():
    """Return the ready-made <dcc.Tab> component (Tab 5)."""
    return dcc.Tab(
        label="Data Timeline Viewer",
        value="tab5",
        style={
            "backgroundColor": "white",
            "padding": "6px 10px",
            "fontSize": "0.9rem",
        },
        selected_style={
            "backgroundColor": "#e6f0ff",
            "borderTop": "2px solid #003366",
            "fontWeight": "bold",
        },
        children=[
            html.Div(
                [
                    html.H3("HVDC (Indicative) Timeline"),
                    html.P(
                        "Visualize and explore synthetic time-series data representing cable monitoring signals.",
                        style={"marginBottom": "15px", "color": "#444"},
                    ),

                    # --------------------------------------------------
                    # Controls – chart type and timescale
                    # --------------------------------------------------
                    html.Div(
                        [
                            # Chart Type Selector
                            html.Div(
                                dcc.RadioItems(
                                    id="it-chart-type",
                                    options=[
                                        {"label": lbl, "value": val}
                                        for val, lbl in CHART_TYPES.items()
                                    ],
                                    value="bar",
                                    labelStyle={
                                        "display": "block",
                                        "padding": "4px 6px",
                                        "backgroundColor": "#fff",
                                        "border": "1px solid #ccc",
                                        "marginBottom": "4px",
                                        "fontSize": "0.9rem",
                                        "cursor": "pointer",
                                    },
                                    inputStyle={"marginRight": "6px"},
                                ),
                                style={
                                    "display": "inline-block",
                                    "verticalAlign": "top",
                                    "marginRight": "10px",
                                },
                            ),

                            # Timescale Selector
                            html.Div(
                                dcc.RadioItems(
                                    id="it-timescale",
                                    options=[{"label": k, "value": k} for k in TIMESCALES.keys()],
                                    value="1Y",
                                    labelStyle={
                                        "display": "inline-block",
                                        "padding": "4px 8px",
                                        "backgroundColor": "#fff",
                                        "border": "1px solid #ccc",
                                        "marginRight": "4px",
                                        "fontSize": "0.9rem",
                                        "cursor": "pointer",
                                    },
                                    inputStyle={"marginRight": "4px"},
                                ),
                                style={
                                    "display": "inline-block",
                                    "verticalAlign": "top",
                                },
                            ),
                        ],
                        style={"marginBottom": "10px"},
                    ),

                    # --------------------------------------------------
                    # Generate / Auto Update Controls
                    # --------------------------------------------------
                    html.Div(
                        [
                            html.Button("Generate / Refresh Data", id="it-generate-btn", n_clicks=0),
                            dcc.Checklist(
                                id="it-auto",
                                options=[{"label": "Auto update", "value": "auto"}],
                                value=[],
                                style={"display": "inline-block", "marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "10px"},
                    ),

                    # --------------------------------------------------
                    # Main Timeline Graph
                    # --------------------------------------------------
                    dcc.Graph(
                        id="it-timeline",
                        clear_on_unhover=True,
                        config={"displayModeBar": True},
                        style={"height": "400px"},
                    ),

                    # Hover Feedback
                    html.Div(
                        id="it-hover-info",
                        style={
                            "marginTop": "10px",
                            "fontWeight": "bold",
                            "fontSize": "1.1rem",
                        },
                    ),

                    # Subset Graph (Brush Selection)
                    dcc.Graph(id="it-subset", style={"height": "300px"}),
                ],
                style={"padding": "20px"},
            )
        ],
    )


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def register_callbacks(app: dash.Dash):
    """Register callbacks for the interactive timeline tab."""

    @app.callback(
        Output("it-timeline", "figure"),
        Input("it-generate-btn", "n_clicks"),
        Input("it-auto", "value"),
        Input("it-chart-type", "value"),
        Input("it-timescale", "value"),
        State("it-timeline", "figure"),   # <-- add this
    )
    def build_timeline(n_clicks, auto_val, chart_type, timescale, current_fig):
        auto = auto_val and "auto" in auto_val
        triggered_id = ctx.triggered_id
    
        # --- NEW: initial load only generates if the graph is empty ---
        if triggered_id is None:
            has_data = bool(current_fig and current_fig.get("data"))
            if has_data:
                raise dash.exceptions.PreventUpdate
            # else: fall through and generate once
    
        # keep existing behaviour: only react to allowed triggers unless auto is enabled
        if not auto and triggered_id not in (
            None,  # <-- allow initial render to pass the guard
            "it-generate-btn",
            "it-chart-type",
            "it-timescale",
        ):
            raise dash.exceptions.PreventUpdate
    
        df = _generate_df()
        days = TIMESCALES.get(timescale)
        if days:
            df = df.tail(days)
    
        if chart_type == "line":
            trace = go.Scatter(
                x=df["timestamp"],
                y=df["value"],
                mode="lines+markers",
                marker=dict(size=6, opacity=0.15),
                hovertemplate="%{x|%d %b %Y}<br><b>%{y}</b> units<extra></extra>",
            )
        elif chart_type == "area":
            trace = go.Scatter(
                x=df["timestamp"],
                y=df["value"],
                mode="lines+markers",
                fill="tozeroy",
                marker=dict(size=6, opacity=0.10),
                hovertemplate="%{x|%d %b %Y}<br><b>%{y}</b> units<extra></extra>",
            )
        else:
            trace = go.Bar(
                x=df["timestamp"],
                y=df["value"],
                hovertemplate="%{x|%d %b %Y}<br><b>%{y}</b> units<extra></extra>",
            )
    
        fig = go.Figure(trace)
        fig.update_layout(
            dragmode="select",
            title="Synthetic Signal Over Time",
            xaxis_title="Date",
            yaxis_title="Signal Amplitude (units)",
            margin=dict(t=40, b=40, l=40, r=20),
        )
        return fig

    # 2) Hover text
    @app.callback(
        Output("it-hover-info", "children"),
        Input("it-timeline", "hoverData"),
    )
    def display_hover(hover_data):
        if hover_data and hover_data.get("points"):
            pt = hover_data["points"][0]
            return f"{pt['x']}: {pt['y']} units"
        return "Hover over a point or bar to see details."

    # 3) Update subset graph (brushed region)
    @app.callback(
        Output("it-subset", "figure"),
        Input("it-timeline", "selectedData"),
    )
    def update_subset(selected):
        if not selected or not selected.get("points"):
            return go.Figure(
                layout=dict(
                    title="Select a range in the timeline above",
                    xaxis_title="Date",
                    yaxis_title="Signal Amplitude",
                )
            )

        xs = [p["x"] for p in selected["points"]]
        ys = [p["y"] for p in selected["points"]]
        fig = go.Figure(go.Bar(x=xs, y=ys))
        fig.update_layout(
            title=f"Selected Data Segment ({len(xs)} days)",
            xaxis_title="Date",
            yaxis_title="Signal Amplitude",
            margin=dict(t=40, b=40, l=40, r=20),
        )
        return fig
