"""
AI-Assisted Condition & Ageing Evidence Explorer (Service Tab)

Purpose (project-facing):
- Presents an indicative UI structure for AI-assisted condition/ageing evidence exploration
  (signals, simple KPI placeholders, and narrative blocks).
- At M18 this tab is a presentation placeholder: it does not execute ageing models,
  does not compute validated KPIs, and does not produce pass/fail conclusions.
- The intent is to show how future model outputs and evidence blocks could be organised
  for review, traceability, and stakeholder communication.

Project context:
- Supports lifecycle/ageing-related concepts across the platform, with expected alignment
  to WP4/WP5/WP6 activities (monitoring inputs, demonstration packaging, and future validation).
- This is an enabling view for evidence exploration, not an operational control workflow.
"""

from dash import html
from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

# ---------------------------------------------------------------------
# SERVICE METADATA OPTIONS
#
# Possible Work Packages:
#   - WP1 – Requirements & System Framework
#   - WP2 – Advanced Cable Materials & Technologies
#   - WP3 – Superconducting Cable Design & Feasibility
#   - WP4 – Monitoring & Diagnostics
#   - WP5 – Validation, Deployment & Lifecycle Assessment
#   - WP6 – Demonstration & Replicability
#   - WP7 – Dissemination, Exploitation & Impact
#
# Possible Categories:
#   - Monitoring & Analytics
#   - Cable Performance & Optimization
#   - Cable System Awareness
#   - Human Engagement
#
# Functions:
#   - (not defined yet – leave empty)
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-hvdc-anomaly-detection",

    "label": "HVDC AI-Assisted Condition & Ageing Evidence Explorer",

    "type": "service",
    "order": 210,

    # Core development in WP4, strong validation/demo usage
    "workpackages": ["WP4", "WP5", "WP6"],

    # Analytics-driven diagnostics with awareness & performance impact
    "categories": [
        "Cable System Awareness",
        "Monitoring & Analytics",
        "Cable Performance & Optimization"
        ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

TAB_PREFIX = "svc-hvdc-anomaly-detection"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "kpis", "label": "KPIs"},
        {"id": "realtime", "label": "Real-Time"},
        {"id": "pmu", "label": "PMU"},
    ],
}

def layout_content():
    return html.Div(
        id="svc-ai-ageing-evidence-explorer-page",   # tab-scoped anchor for CSS
        className="tab-page",
        children=[
            html.H3("AI-Assisted Condition & Ageing Evidence Explorer (UI placeholder)"),

            html.P(
                "This tab presents the intended UI structure for AI-assisted condition and ageing evidence exploration. "
                "At M18 it is a presentation placeholder: it does not run ageing models, compute verified KPIs, "
                "or produce pass/fail conclusions."
            ),

            html.Hr(),

            html.P(
                "Associated Work Packages: WP4, WP5, WP6",
                style={"fontStyle": "italic"}
            ),

            html.P(
                "Associated Categories: Monitoring & Analytics, "
                "Cable Performance & Optimization, Cable System Awareness",
                style={"fontStyle": "italic"}
            ),

            # Hero image (assets/tabs_hero_images/)
            html.Div(
                className="cae-hero",
                style={
                    "backgroundImage": "url('/assets/tabs_hero_images/svc-ai-ageing-evidence-explorer-page_hvdc.jpg')",
                    "backgroundSize": "cover",
                    "backgroundPosition": "center",
                    "backgroundRepeat": "no-repeat",
                },
            ),

            html.Div(
                className="cae-note",
                children=[
                    html.Strong("M18 note: "),
                    html.Span(
                        "The blocks below are indicative placeholders showing how AI-assisted ageing evidence, "
                        "confidence cues, and reviewer-readable summaries could be displayed later. "
                        "Values are intentionally not computed."
                    ),
                ],
            ),

            html.Div(
                className="placeholder-box tab-placeholder",
                children=[
                    html.H4("Indicative KPI placeholders (not computed)"),
                    html.Div(
                        className="cae-kpi-grid",
                        children=[
                            html.Div(
                                className="cae-kpi-card",
                                children=[
                                    html.Div("Condition cue", className="cae-kpi-title"),
                                    html.Div("—", className="cae-kpi-value"),
                                    html.Div("placeholder", className="cae-kpi-sub"),
                                ],
                            ),
                            html.Div(
                                className="cae-kpi-card",
                                children=[
                                    html.Div("Ageing risk cue", className="cae-kpi-title"),
                                    html.Div("—", className="cae-kpi-value"),
                                    html.Div("placeholder", className="cae-kpi-sub"),
                                ],
                            ),
                            html.Div(
                                className="cae-kpi-card",
                                children=[
                                    html.Div("Data coverage", className="cae-kpi-title"),
                                    html.Div("—", className="cae-kpi-value"),
                                    html.Div("placeholder", className="cae-kpi-sub"),
                                ],
                            ),
                            html.Div(
                                className="cae-kpi-card",
                                children=[
                                    html.Div("Confidence cue", className="cae-kpi-title"),
                                    html.Div("—", className="cae-kpi-value"),
                                    html.Div("placeholder", className="cae-kpi-sub"),
                                ],
                            ),
                        ],
                    ),
                    html.P(
                        "Future extension: model-driven outputs, explanation blocks, and traceable evidence links "
                        "to monitoring/analytics views.",
                        style={"marginTop": "10px"}
                    ),
                ]
            ),
        ]
    )


def layout():
    return menu_layout()

def register_callbacks(app):
    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)