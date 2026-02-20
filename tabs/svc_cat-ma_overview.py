"""
Monitoring & Analytics (MA) — Category Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a consolidated, category-level narrative for Monitoring & Analytics (MA).
- Acts as an anchor page under the MA category, explaining:
  • what this category covers,
  • what signals/KPIs are typically reviewed here,
  • how MA links telemetry monitoring, validation/quality cues, and analytics readiness.

Platform role:
- This is a category-level overview (not a WP deliverable page).
- It is designed to be meta-driven and reusable across contexts (different links/pilots),
  with minimal or no changes to interrelated components.
- Hyperlink routing is enabled via meta-driven tool links (safe fallback if a tool is missing).
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
    
_ALL_HERO_IMAGES = _assets_image_list("cat_ma")

TAB_META = {
    "id": "svc-ma-overview",
    "label": "Monitoring & Analytics Overview",
    "type": "service",

    # Keep it relatively early within the MA tool strip
    "order": 31,

    # Category overview: not tied to a single WP
    "workpackages": [],

    # Anchored strictly to this category label (must match category tab label logic)
    "categories": [
        "Monitoring & Analytics"
    ],

    "subcategories": [],

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

target_ma_ta = "svc-hvdc-telemetry-analytics"
target_ma_duv = "svc-hvdc-data-utilization-validation"

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
                            html.H2("Monitoring & Analytics (MA) — Category Overview"),
                            html.P(
                                "A structured entry point to MA: monitoring status, analytics readiness, and quality cues that help interpret signals safely.",
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
                                    html.Span("MA", className="wp-badge wp-badge-strong"),
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
                                            html.Li("Monitoring status and telemetry availability at a glance."),
                                            html.Li("Data readiness and integrity cues that gate analytics trust."),
                                            html.Li("Analytics-oriented summaries that help decide where to deep-dive next."),
                                        ],
                                        className="wp-list",
                                    ),
                                    html.P(
                                        "Subcategories: • Data Visualization • Data Analysis • Lab Measurements, Sensors & PMUs.",
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
                                            html.A("Scope", href=f"#{sid('sec-scope')}", className="wp-jump-btn"),
                                            html.A("Signals & KPIs", href=f"#{sid('sec-kpis')}", className="wp-jump-btn"),
                                            html.A("Sub-areas", href=f"#{sid('sec-subareas')}", className="wp-jump-btn"),
                                            html.A("How it connects", href=f"#{sid('sec-conn')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "Tip: This page orients the viewer. Tool hyperlinks will be added in a follow-up step.",
                                        className="wp-note",
                                    ),
                                    html.P(
                                        "Note: This category overview is an orientation page (M18); it does not claim completed tool coverage or final evaluation results.",
                                        className="wp-note-2",
                                    ),
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
                    html.H3("Scope of Monitoring & Analytics"),
                    html.P(
                        "MA groups views that support day-to-day operational monitoring and analytics consumption. "
                        "The emphasis is on readiness: what data exists, whether it is reliable, and what the high-level signals indicate "
                        "before moving into specialised diagnostic or performance tools.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Monitoring readiness"),
                                    html.P("Telemetry availability, coverage, and high-level status indicators."),
                                    html.P("Emphasis: fast orientation and consistent presentation."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Data quality & validation"),
                                    html.P("Integrity cues that affect trust: missing-data patterns, timing issues, and validation flags."),
                                    html.P("Emphasis: transparent gating of analytics confidence."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Analytics consumption"),
                                    html.P("Summaries, indicators, and evidence packaging that guide deeper investigation."),
                                    html.P("Emphasis: traceability and stakeholder-readable outputs."),
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
                    html.H3("Signals & KPIs typically reviewed in MA"),
                    html.P(
                        "MA pages typically combine monitoring signals with data quality cues and analytics-oriented indicators. "
                        "The goal is to provide an operational snapshot that is safe to interpret and easy to communicate.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Monitoring & availability indicators"),
                                    html.Ul(
                                        [
                                            html.Li("Telemetry coverage and continuity (what data is present, and where gaps exist)."),
                                            html.Li("High-level trends and stability cues over selected time windows."),
                                            html.Li("Health/readiness summaries for streams, sensors, or ingestion pipelines."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Integrity cues for analytics trust"),
                                    html.Ul(
                                        [
                                            html.Li("Missing data, latency/jitter, and timestamp consistency effects."),
                                            html.Li("Validation flags that indicate whether indicators/analytics are safe to use."),
                                            html.Li("Context markers (operating regimes, event windows, scenario tags) that frame interpretation."),
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
                            html.Span(
                                "Exact KPI definitions, labels, and thresholds are expected to be driven by metadata/configuration "
                                "and the selected context (link/pilot)."
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SUB-AREAS =================
            html.Div(
                id=sid("sec-subareas"),
                className="wp-section",
                children=[
                    html.H3("MA sub-areas (how the category is structured)"),
                    html.P(
                        "MA can be interpreted through three practical sub-areas. These are complementary views that support "
                        "a coherent monitoring-and-analytics story, from data readiness to evidence packaging.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Monitoring & overview"),
                                    html.P("A single place to see operational status and the most important high-level trends."),
                                    html.P("Typical output: quick orientation for operators and reviewers."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Validation & data readiness"),
                                    html.P("Integrity cues and validation states that determine whether analytics can be trusted."),
                                    html.P("Typical output: readiness flags and data-quality summaries."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Analytics summaries"),
                                    html.P("Derived indicators that help decide where to drill down next (diagnostics, performance, scenarios)."),
                                    html.P("Typical output: evidence-oriented summaries and consistent terminology."),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # ================= SECTION: TOOLS =================
            html.Div(
                id=sid("sec-tools"),
                className="wp-section",
                children=[
                    html.H3("Tools (quick access)"),
                    html.P(
                        "Quick access to monitoring, validation, and analytics tools that support data readiness and operational interpretation.",
                        className="wp-par",
                    ),
                
                    # -------- MA --------
                    html.H4("Monitoring & Analytics (MA)"),
                    html.P(
                        "Deeper validation analytics and utilisation views that often feed CSA interpretation.",
                        className="wp-par",
                        style={"marginTop": "18px"},
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_ma_ta)),
                                    html.P("Validation checks and analytics blocks built on telemetry streams."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_ma_ta,  "src": SERVICE_ID, "uid": sid("link-ma-ta")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_ma_duv)),
                                    html.P("Utilisation/correlation views and validation analytics for interpretation support."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_ma_duv, "src": SERVICE_ID, "uid": sid("link-ma-duv")},
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
                    html.H3("How MA connects across the project"),
                    html.P(
                        "MA is designed as a shared entry point: it supports common monitoring and analytics language across categories and Work Packages. "
                        "It helps stakeholders validate that the data is usable and the context is understood before relying on deeper analytics.",
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
                                            html.Li("It groups tools by the user goal: monitoring readiness and analytics consumption."),
                                            html.Li("It stays independent from timeline: tools can still map to WPs for reporting."),
                                            html.Li("It keeps the platform extensible (new MA tools join via TAB_META only)."),
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
                                            html.Li("A consistent operational snapshot that is easy to communicate."),
                                            html.Li("Meta-driven adjustments across links/pilots with minimal ripple effects."),
                                            html.Li("Clean navigation patterns once hyperlinks are enabled (later step)."),
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
                            html.P("End of MA category overview. Use this page to orient the viewer before opening detailed tools."),
                        ],
                    ),
                ],
            ),

            # Dummy output required by clientside callback
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