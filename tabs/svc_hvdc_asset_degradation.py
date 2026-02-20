from dash import html
from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

# ============================================================
# TAB META (UNCHANGED – orchestrator-level)
# ============================================================

TAB_META = {
    "id": "svc-hvdc-asset-degradation",
    "label": "HVDC Asset Degradation & Remaining Life Estimation",
    "type": "service",
    "order": 220,
    "workpackages": ["WP4", "WP5", "WP6"],
    "categories": [
        "Human Engagement",
        "Cable Performance & Optimization",
        "Cable System Awareness",
        "Monitoring & Analytics",
    ],
    "version": "v0.1 (demo)",
    "status": "active",
}

# ============================================================
# TAB MENU META (tool-level)
# ============================================================

TAB_PREFIX = "svc-hvdc-asset-degradation"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "inputs", "label": "Inputs"},
        {"id": "analysis", "label": "Analysis"},
        {"id": "results", "label": "Results"},
        {"id": "assumptions", "label": "Assumptions"},
    ],
}

# ============================================================
# LAYOUT CONTENT (review-ready placeholders; no claim of validation)
# ============================================================

def layout_content():
    return html.Div(
        id=f"{TAB_PREFIX}-page",   # tab-scoped id for CSS (safe)
        className="tab-page",
        children=[
            html.H3("Asset Degradation & Remaining Life Estimation (UI placeholder)"),

            html.P(
                "This tab presents the intended UI structure for lifecycle-oriented evidence and remaining-life reasoning. "
                "At M18 it is a presentation placeholder: it does not run degradation models, compute verified KPIs, "
                "or produce pass/fail conclusions."
            ),

            html.Hr(),

            # HERO (put your image in assets/tabs_hero_images/)
            html.Div(
                id=f"{TAB_PREFIX}-hero",
                className="lcc-hero",
                style={
                    "backgroundImage": "url('/assets/tabs_hero_images/svc-hvdc-asset-degradation_hvdc_terminal.jpg')",
                    "backgroundSize": "cover",
                    "backgroundPosition": "center",
                    "backgroundRepeat": "no-repeat",
                },
            ),

            html.Div(
                id=f"{TAB_PREFIX}-note",
                className="lcc-note",
                children=[
                    html.Strong("M18 note: "),
                    html.Span(
                        "The blocks below are indicative placeholders showing how lifecycle evidence and KPIs could be displayed later. "
                        "Values are intentionally not computed."
                    ),
                ],
            ),

            # Indicative KPI placeholders (no logic)
            html.Div(
                id=f"{TAB_PREFIX}-kpi-grid",
                className="lcc-kpi-grid",
                children=[
                    html.Div(
                        className="lcc-kpi-card",
                        children=[
                            html.Div("Remaining-Life Index", className="lcc-kpi-title"),
                            html.Div("—", className="lcc-kpi-value"),
                            html.Div("Indicative placeholder (not computed)", className="lcc-kpi-sub"),
                        ],
                    ),
                    html.Div(
                        className="lcc-kpi-card",
                        children=[
                            html.Div("Stress Accumulation Cue", className="lcc-kpi-title"),
                            html.Div("—", className="lcc-kpi-value"),
                            html.Div("Indicative placeholder (not computed)", className="lcc-kpi-sub"),
                        ],
                    ),
                    html.Div(
                        className="lcc-kpi-card",
                        children=[
                            html.Div("Data Coverage Cue", className="lcc-kpi-title"),
                            html.Div("—", className="lcc-kpi-value"),
                            html.Div("Indicative placeholder (not computed)", className="lcc-kpi-sub"),
                        ],
                    ),
                    html.Div(
                        className="lcc-kpi-card",
                        children=[
                            html.Div("Confidence Cue", className="lcc-kpi-title"),
                            html.Div("—", className="lcc-kpi-value"),
                            html.Div("Indicative placeholder (not computed)", className="lcc-kpi-sub"),
                        ],
                    ),
                ],
            ),

            html.Div(
                id=f"{TAB_PREFIX}-placeholder",
                className="placeholder-box",
                children=[
                    html.P(
                        "Later integration point: degradation models, stress accumulation logic, uncertainty handling, "
                        "and remaining-life evidence blocks.",
                        style={"textAlign": "center"},
                    )
                ],
            ),
        ],
    )

# ============================================================
# LAYOUT SHELL
# ============================================================

def layout():
    return menu_layout()

# ============================================================
# CALLBACK REGISTRATION
# ============================================================

def register_callbacks(app):
    register_tab_menu_callbacks(app, TAB_PREFIX)