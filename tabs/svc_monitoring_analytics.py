"""
HVDC Telemetry Validation & Analytics Tool (Service Tab)

Purpose (project-facing):
- Provides a validation and analytics layer for HVDC cable telemetry data
  originating from PMUs, SCADA systems, and related measurement sources.
- Focuses on data relevance testing, consistency checks, and KPI extraction
  aligned with CABLEGNOSIS use cases and requirements.
- Acts as an intermediate platform tool that bridges WP4 monitoring concepts
  with WP5 validation activities and platform-level analytics.

Data & Requirements context:
- Input data structures and signals are aligned with WP4 monitoring data
  templates (e.g. PMU/SCADA time-series, temperature-related measurements).
- Analytics outputs are mapped to project use cases and validation
  requirements as defined in UC–Req mapping documents.
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
    # Stable identifier (do not bind to UI wording)
    "id": "svc-hvdc-telemetry-analytics",

    # HVDC- and validation-oriented label (not generic monitoring)
    "label": "HVDC Telemetry Validation & Analytics",

    "type": "service",
    "order": 250,

    # Developed in WP4, heavily used in WP5 validation,
    # and potentially reused in demonstrations.
    "workpackages": ["WP4", "WP5", "WP6"],

    # Core analytics + situational awareness + performance insight
    "categories": [
        "Monitoring & Analytics",
        "Cable Performance & Optimization",
        "Cable System Awareness"
    ],

    "subcategories": [],

    # Functions not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

TAB_PREFIX = "svc-hvdc-telemetry-analytics"

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
        className="tab-page",
        children=[
            html.H3("Monitoring & Analytics Service"),

            html.P(
                "This service provides monitoring, data analytics, and KPI "
                "computation capabilities across multiple work packages."
            ),

            html.Hr(),

            html.P(
                "Associated Work Packages: WP4, WP5",
                style={"fontStyle": "italic"}
            ),

            html.P(
                "Associated Categories: Monitoring & Analytics, "
                "Cable Performance & Optimization, Cable System Awareness",
                style={"fontStyle": "italic"}
            ),

            html.Div(
                className="placeholder-box",
                children=[
                    html.P(
                        "Functional components will be integrated here.",
                        style={"textAlign": "center"}
                    )
                ]
            )
        ]
    )
    
def layout():
    return menu_layout()

def register_callbacks(app):
    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)