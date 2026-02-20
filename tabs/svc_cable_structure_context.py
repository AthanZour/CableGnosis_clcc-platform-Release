"""Cable Components & Structure Tab — placeholder."""
from dash import html
from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks
"""
HVDC Cable Structural & Material Context Tool

Purpose:
- Provides structural and material context of HVDC cable systems to support
  system understanding, feasibility assessment, and interpretation of monitoring
  and diagnostic results.
- Exposes the internal structure of cable components (layers, materials, interfaces)
  as contextual information rather than as an operational monitoring tool.
- Acts as a reference and awareness capability that other platform services can rely on
  for consistent system understanding.

Project context:
- Supports system framework definition, feasibility analysis, and interpretation
  activities across multiple Work Packages.
- This tool is provided by the platform to enhance cable system awareness and is
  not an end-user workflow nor a Work Package entry point.
"""

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
    "id": "svc-cable-structure-context",

    "label": "HVDC Cable Structure & Material Context",

    "type": "service",

    # Πιο “ήσυχο” εργαλείο, όχι primary analytics
    "order": 245,

    # Γενικής χρήσης σε framework, feasibility και demo
    "workpackages": ["WP3"],

    # Καθαρό awareness tool
    "categories": [
        "Cable System Awareness",
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active",
}

TAB_PREFIX = "svc-cable-structure-context"

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
        "Placeholder for cable structure visualization.",
        style={"padding": "20px"},
    )


def layout():
    return menu_layout()

def register_callbacks(app):
    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)