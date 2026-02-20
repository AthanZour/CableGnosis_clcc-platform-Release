"""
Cable Performance & Optimization (CPO) — Category Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a consolidated, category-level narrative for Cable Performance & Optimization (CPO).
- Acts as an anchor page under the CPO category, explaining:
  • what this category covers,
  • what signals/KPIs are typically reviewed here,
  • how to navigate to the key tools linked to CPO.

Platform role:
- This is a category-level overview (not a WP deliverable page).
- It supports consistent, meta-driven navigation across tools via hyperlinks (tool-link ids),
  while keeping orchestration behavior aligned with the active orchestrator mode.
"""

from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output
from pathlib import Path
import re

from tabs_core.tool_registry import tool_label

def _assets_image_list(
    subfolder: str,
    prefix: str = "/assets/",
) -> str:
    """
    Returns a pipe-separated list of all image URLs in /assets/<subfolder>/ (Dash assets folder).

    Ordering:
    - Files whose names start with TWO digits are sorted by that 2-digit number (00..99).
    - All other files are appended after, preserving discovery order.
    - Fallback images are always appended at the very end (no duplicates).

    Never raises if the folder is missing.
    """
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

    fallback = [
        "/assets/Undersea-Cables.jpeg",
        "/assets/subsea-cables-internet-ai-spooky-pooka-illustration.jpg",
    ]

    assets_root = Path(__file__).resolve().parents[1] / "assets"
    assets_dir = assets_root / subfolder

    images = []
    try:
        if assets_dir.exists() and assets_dir.is_dir():
            discovered = [
                p for p in assets_dir.iterdir()
                if p.is_file() and p.suffix.lower() in exts
            ]

            two_digit = re.compile(r"^(\d{2})")

            numeric = []
            non_numeric = []

            for p in discovered:
                m = two_digit.match(p.name)
                if m:
                    numeric.append((int(m.group(1)), p))
                else:
                    non_numeric.append(p)

            # Sort only the numeric-first group (00..99)
            numeric.sort(key=lambda t: t[0])

            ordered = [p for _, p in numeric] + non_numeric

            images = [f"{prefix}{subfolder}/{p.name}" for p in ordered]
    except Exception:
        images = []

    # Always append fallback at end (no duplicates)
    for f in fallback:
        if f not in images:
            images.append(f)

    return "|".join(images)
    
_ALL_HERO_IMAGES = _assets_image_list("cat_cpo")

TAB_META = {
    "id": "svc-cpo-overview",

    "label": "Cable Performance & Optimization Overview",

    "type": "service",

    # Keep it relatively early within the CPO tool strip
    "order": 32,

    # Category overview: not tied to a single WP
    "workpackages": [],

    # Anchored strictly to this category label (must match category tab label logic)
    "categories": [
        "Cable Performance & Optimization"
    ],

    "subcategories": [],

    # "functions": [],

    "version": "v1.0 (category overview)",
    "status": "active"
}

SERVICE_ID = TAB_META["id"]


def sid(suffix: str) -> str:
    return f"{SERVICE_ID}-{suffix}"


# ------------------------------------------------------------------
# Layout (template-aligned, text adapted for CATEGORY context)
# NOTE: Keep the hero image id suffix "-hero-image_wp_over" for overview.js compatibility.
# ------------------------------------------------------------------

target_cpo_opm = "svc-hvdc-operational-monitoring"
target_cpo_tea = "svc-hvdc-telemetry-analytics"
target_cpo_duv = "svc-hvdc-data-utilization-validation"
target_cpo_asde = "svc-hvdc-asset-degradation"
target_cpo_ad_ec = "svc-hvdc-anomaly-detection"

def layout():
    return html.Div(
        id=sid("root"),
        className="wp-overview-tab",
        children=[

            # ================= HEADER =================
            html.Div(
                id=sid("header"),
                className="wp-header",
                children=[
                    html.Div(
                        className="wp-header-left",
                        children=[
                            html.H2("Cable Performance & Optimization (CPO) — Category Overview"),
                            html.P(
                                "An entry point to the Cable Performance and Optimization category: what it covers at the cyber level"
                                " of the C-LCC, which sub-capabilities it includes, and where to navigate next.",
                                className="wp-lead",
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-header-right",
                        children=[
                            html.Div(
                                className="wp-badges",
                                children=[
                                    html.Span("Category Overview of", className="wp-badge"),
                                    html.Span("CPO", className="wp-badge wp-badge-strong"),
                                ],
                            )
                        ],
                    ),
                ],
            ),

            # ================= HERO =================
            html.Div(
                id=sid("hero"),
                className="wp-hero",
                children=[
                    html.Div(
                        id=sid("hero-left"),
                        className="wp-hero-left",
                        children=[
                            html.Div(
                                id=sid("hero-image_wp_over"),
                                className="wp-hero-image",
                                **{
                                    # Use '|' to separate image paths; do not end with '|'
                                    "data-images": _ALL_HERO_IMAGES
                                },
                                style={
                                    "backgroundImage": "url('/assets/Undersea-Cables.jpeg')",
                                    "backgroundSize": "cover",
                                    "backgroundPosition": "center",
                                    "cursor": "pointer",
                                },
                            ),
                            html.Div(
                                id=sid("cursor"),
                                className="wp-cursor",
                            ),
                        ],
                    ),
                    html.Div(
                        id=sid("hero-right"),
                        className="wp-hero-right",
                        children=[
                            html.Div(
                                className="wp-card wp-card-compact",
                                children=[
                                    html.H4("What this category is about"),
                                    html.Ul(
                                        [
                                            html.Li("AI and machine-learning methods for assessing cable performance and behaviour."),
                                            html.Li("Fault detection logic and data-driven algorithms supporting decision support."),
                                            html.Li("Optimisation-oriented analysis that connects performance evidence to lifecycle and system design choices."),
                                        ],
                                        className="wp-list",
                                    ),
                                    html.P(
                                        "Subcategories: Machine Learning • AI Algorithms • Fault Detection.",
                                        className="wp-note",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card wp-card-compact",
                                children=[
                                    html.H4("Quick jump"),
                                    html.Div(
                                        className="wp-jump",
                                        children=[
                                            html.A("Scope & subcategories", href=f"#{sid('sec-scope')}", className="wp-jump-btn"),
                                            html.A("Signals & evidence", href=f"#{sid('sec-kpis')}", className="wp-jump-btn"),
                                            html.A("Tools", href=f"#{sid('sec-tools')}", className="wp-jump-btn"),
                                            html.A("How it connects", href=f"#{sid('sec-conn')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "Tip: Use the links below to open tool tabs directly. If a target tool is not available, the click safely does nothing.",
                                        className="wp-note",
                                    ),
                                    html.P(
                                        "M18 status: integration & orchestration readiness demonstration (navigation, routing, stable interaction patterns / indicative M18 framing; not final operational workflows).",
                                        className="wp-note-2",
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SCOPE =================
            html.Div(
                id=sid("sec-scope"),
                className="wp-section",
                children=[
                    html.H3("Scope of Cable Performance and Optimization"),
                    html.P(
                        "This category corresponds primarily to the cyber level of the C-LCC. It groups machine-learning and AI algorithms that support cable performance assessment, fault detection and localisation, and optimisation of lifecycle and system design decisions.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Machine Learning"),
                                    html.P("Data-driven models that extract performance patterns from operational and contextual signals."),
                                    html.P("Typical use: learned indicators, anomaly scoring, feature-based performance profiles."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("AI Algorithms"),
                                    html.P("Algorithmic reasoning blocks that convert data into explainable performance and risk insights."),
                                    html.P("Typical use: structured analytics, model outputs, and decision-support cues."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Fault Detection"),
                                    html.P("Methods for fault detection and localisation that support pre-emptive actions and optimisation."),
                                    html.P("Typical use: detection flags, event classification cues, and evidence packaging."),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: KPIS =================
            html.Div(
                id=sid("sec-kpis"),
                className="wp-section",
                children=[
                    html.H3("Signals & evidence typically reviewed in CPO"),
                    html.P(
                        "CPO pages combine measurements and derived indicators to support AI/ML reasoning. Where KPIs are indicative (demo-ready), they should be interpreted alongside the evidence and assumptions used by the underlying algorithms.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Performance-related signals"),
                                    html.Ul(
                                        [
                                            html.Li("Operational behaviour over time (e.g., load/current/voltage patterns)."),
                                            html.Li("Stability and change cues (trends, excursions, persistent regimes)."),
                                            html.Li("Context markers for modelling (scenario tags, operating regimes, event windows where available)."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Algorithm evidence & trust cues"),
                                    html.Ul(
                                        [
                                            html.Li("Inputs used by models (feature sets, windows, baselines)."),
                                            html.Li("Model outputs (scores, flags, classifications) with supporting context."),
                                            html.Li("Quality/validity cues needed to interpret results (e.g., missing data patterns, validation flags)."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout",
                        children=[
                            html.Strong("Note: "),
                            html.Span("Exact definitions, thresholds, and narrative labels are expected to be metadata-driven and adjusted per link/pilot context."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: TOOLS =================
            html.Div(
                id=sid("sec-tools"),
                className="wp-section",
                children=[
                    html.H3("Tools in this category (open directly)"),
                    html.P(
                        "These links open the actual tool tabs. If a target tool is not available, the click safely does nothing (no forced context switching).",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_cpo_opm)),
                                    html.P("Situational view and integrity cues supporting performance interpretation."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_cpo_opm,  "src": SERVICE_ID, "uid": sid("link-cpo-opm")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[                                    
                                    html.H5(tool_label(target_cpo_tea)),
                                    html.P("Analytics blocks and indicators that build on validated telemetry."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_cpo_tea,  "src": SERVICE_ID, "uid": sid("link-cpo-tea")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[                                    
                                    html.H5(tool_label(target_cpo_duv)),
                                    html.P("Data flows and correlation views supporting utilisation/interpretation."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_cpo_duv,  "src": SERVICE_ID, "uid": sid("link-cpo-duv")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-grid-3",
                        style={"marginTop": "10px"},
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_cpo_asde)),
                                    html.P("Asset-oriented indicators that can be interpreted alongside performance signals."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_cpo_asde, "src": SERVICE_ID, "uid": sid("link-cpo-asde")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[                                    
                                    html.H5(tool_label(target_cpo_ad_ec)),
                                    html.P("Event/diagnostic cues that can affect operational performance narratives."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_cpo_ad_ec,"src": SERVICE_ID, "uid": sid("link-cpo-ad-ec")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: CONNECTIONS =================
            html.Div(
                id=sid("sec-conn"),
                className="wp-section",
                children=[
                    html.H3("How CPO connects across the project"),
                    html.P(
                        "CPO is cross-cutting: AI/ML and fault-related analytics can be reused across multiple Work Packages and pilot contexts. The category view keeps these capabilities grouped by purpose (performance/optimisation), while WP mapping remains available for reporting and deliverables.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Why it is category-driven"),
                                    html.Ul(
                                        [
                                            html.Li("It groups tools by analytical intent (performance assessment, AI/ML reasoning, fault detection)."),
                                            html.Li("It supports reuse across pilots without hard-coded coupling."),
                                            html.Li("It stays extensible: new AI/ML tools join through metadata only."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("What this enables"),
                                    html.Ul(
                                        [
                                            html.Li("A consistent vocabulary for AI/ML outputs and evidence blocks."),
                                            html.Li("Direct tool navigation via hyperlinks with safe fallbacks."),
                                            html.Li("A clean path to future orchestrator modes (e.g., favorites) without rewriting tools."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-footer",
                        children=[
                            html.P("End of CPO category overview. Use this page to orient the viewer and jump into the relevant tools."),
                        ],
                    ),
                ],
            ),

            dcc.Input(id=sid("js-response"), value="", style={"display": "none"}),
        ],
    )


# ------------------------------------------------------------------
# Callbacks (UNCHANGED)
# ------------------------------------------------------------------
def register_callbacks(app):
    app.clientside_callback(
        ClientsideFunction(namespace="overview", function_name="init"),
        Output(sid("js-response"), "value"),
        # Declared @ app.py
        Input("selected-tool-store", "data"),
    )