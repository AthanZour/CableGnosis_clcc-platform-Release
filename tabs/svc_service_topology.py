"""
Service Topology & Runtime Overview Tool

Purpose:
- Provides a platform-level overview of active services, their relationships,
  and runtime status within the CABLEGNOSIS Life Cycle Center.
- Supports system-level situational awareness by exposing how platform services
  are deployed, interconnected, and made available to higher-level tools.
- Intended primarily for validation, demonstration, and system inspection,
  rather than for operational monitoring of HVDC assets.

Project context:
- Supports integration, validation, and demonstration activities by allowing
  stakeholders to understand the internal structure and availability of
  CABLEGNOSIS platform services.
- This tool represents a platform capability and is not an end-user workflow
  nor a Work Package entry point.
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
    "id": "svc-service-topology",

    "label": "Service Topology & Runtime Overview",

    "type": "service",

    # χαμηλό relative priority – δεν είναι primary analytic tool
    "order": 240,

    # Συνδέεται κυρίως με integration, validation και demo
    "workpackages": ["WP1", "WP5", "WP6"],

    # Καθαρό platform awareness tool
    "categories": [
        "Cable System Awareness",
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active",
}

TAB_PREFIX = "svc-service-topology"

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
        "Placeholder for Microservices Dashboard.",
        style={"padding": "20px"},
    )

def layout():
    return menu_layout()
    
def register_callbacks(app):
    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)
