"""
HVDC Event & Evidence Timeline Viewer Tab
Uses tab_menu_template (implicit menu_layout)
"""

from dash import html

from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

from tabs_core.interactive_timeline_core import (
    get_tab,
    register_callbacks as interactive_register,
)

# ============================================================
# TAB META (for orchestrator)
# ============================================================

TAB_META = {
    "id": "svc-hvdc-data-timeline",
    "label": "HVDC Event & Evidence Timeline",
    "type": "service",
    "order": 230,
    "workpackages": ["WP4", "WP5", "WP6"],
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
    ],
    "subcategories": [],
    "version": "v0.1 (demo)",
    "status": "active",
}

# ============================================================
# TAB CONFIG (REQUIRED BY menu_layout)
# ============================================================

TAB_PREFIX = "svc-hvdc-data-timeline-1"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "timeline", "label": "Timeline"},
        {"id": "details", "label": "Details"},
    ],
}

def layout_content():
    """
    Main content for the timeline tab.
    menu_layout() will wrap this automatically.
    """
    return [
        # ----------- SAFE PLACEHOLDER (always visible) -----------
        html.Div(
            id=f"{TAB_PREFIX}-placeholder",
            className="timeline_ph_root",
            children=[
                html.Div(
                    className="timeline_ph_header",
                    children=[
                        html.H2("HVDC Event & Evidence Timeline"),
                        html.P(
                            "A time-ordered view intended to support demo walk-throughs (WP4/WP5) and, later, validation packaging (WP6). "
                            "At M18, this tab is a review-safe placeholder: it currently visualises a simple (synthetic) time series to illustrate "
                            "the expected navigation pattern. It does not perform validation or provide pass/fail conclusions."
                        ),
                    ],
                ),

                html.Div(
                    className="timeline_ph_grid",
                    children=[
                        html.Div(
                            className="timeline_ph_card",
                            children=[
                                html.H4("What you can preview now (M18 demo state)"),
                                html.Ul(
                                    [
                                        html.Li("A simple time series view demonstrating time navigation (pan/zoom/selection)."),
                                        html.Li("A placeholder interaction pattern for selecting time windows before opening other tools."),
                                        html.Li("A consistent entry point that will later host richer evidence layers when pilots mature."),
                                    ],
                                    className="timeline_ph_list",
                                ),
                            ],
                        ),
                        html.Div(
                            className="timeline_ph_card",
                            children=[
                                html.H4("What is planned to be added (as pilots progress)"),
                                html.Ul(
                                    [
                                        html.Li("Time-aligned evidence markers (e.g., snapshots, KPIs, flags) as a chronological index."),
                                        html.Li("Quick navigation across datasets and key demonstration moments (events / annotations)."),
                                        html.Li("Direct hand-off links into monitoring, analytics, and diagnostics views based on the selected window."),
                                    ],
                                    className="timeline_ph_list",
                                ),
                            ],
                        ),
                    ],
                ),

                html.Div(
                    id=f"{TAB_PREFIX}-media-slot",
                    className="timeline_ph_media",
                    children=[
                        html.Img(
                            src="/assets/tabs_hero_images/data_timeline_viewer.jpg",
                            className="timeline_ph_media_img",
                            alt="HVDC Event & Evidence Timeline",
                        )
                    ],
                ),
            ],
        ),

        # ----------- EXISTING interactive timeline container (unchanged) -----------
        html.Div(
            id=f"{TAB_PREFIX}-timeline-container",
            children=get_tab(),
        ),
    ]

def layout():
    return menu_layout()

def register_callbacks(app):
    interactive_register(app)
    register_tab_menu_callbacks(app, TAB_PREFIX)