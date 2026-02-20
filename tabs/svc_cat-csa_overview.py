"""
Cable System Awareness (CSA) — Category Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a consolidated, category-level narrative for Cable System Awareness (CSA).
- Acts as an anchor page under the CSA category, explaining:
  • what this category covers,
  • what signals/KPIs are typically reviewed here,
  • how CSA links monitoring views, anomaly/event awareness, and context.

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
    
_ALL_HERO_IMAGES = _assets_image_list("cat_csa")

TAB_META = {
    "id": "svc-csa-overview",
    "label": "Cable System Awareness Overview",
    "type": "service",

    # Keep it relatively early within the CSA tool strip
    "order": 33,

    # Category overview: not tied to a single WP
    "workpackages": [],

    # Anchored strictly to this category label (must match category tab label logic)
    "categories": [
        "Cable System Awareness"
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

target_csa_ta = "svc-hvdc-telemetry-analytics"
target_csa_ad_ec = "svc-hvdc-anomaly-detection"
target_csa_dtv = "svc-hvdc-data-timeline"
target_csa_st = "svc-service-topology"

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
                            html.H2("Cable System Awareness (CSA) — Category Overview"),
                            html.P(
                                "A structured entry point to CSA: situational awareness, context, and operational understanding of the monitored cable system.",
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
                                    html.Span("CSA", className="wp-badge wp-badge-strong"),
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
                                                html.Li("A coherent system view across telemetry, context, and events."),
                                                html.Li("Operational awareness (what is happening now, and what changed)."),
                                                html.Li("Interpretation support: context markers that help read analytics safely."),
                                            ],
                                            className="wp-list",
                                        ),
                                        html.P(
                                            "Subcategories: • Pre-Fault Detection • Alarming • Preparation.",
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
                    html.H3("Scope of Cable System Awareness"),
                    html.P(
                        "CSA groups views that help stakeholders understand the monitored system at a glance. "
                        "The focus is situational awareness: operational state, context, and event cues that explain what the system is doing.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Situational view"),
                                    html.P("High-level status, trends, and key indicators that summarise system behaviour."),
                                    html.P("Emphasis: clarity and fast orientation."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Context & traceability"),
                                    html.P("Context markers (operating regime, time windows, known conditions) that frame interpretation."),
                                    html.P("Emphasis: explainability and consistent terminology."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Event awareness"),
                                    html.P("Anomaly/event cues that highlight deviations and support operational follow-up."),
                                    html.P("Emphasis: actionable flags and narrative relevance."),
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
                    html.H3("Signals & KPIs typically reviewed in CSA"),
                    html.P(
                        "CSA pages typically combine raw measurements with derived indicators and event cues. "
                        "The goal is to support a shared understanding of system behaviour before deep-dive analysis.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Operational status & trends"),
                                    html.Ul(
                                        [
                                            html.Li("System-level operational trends (e.g., load/current/voltage behaviour)."),
                                            html.Li("Stability cues and deviations (short-term vs sustained changes)."),
                                            html.Li("Time-windowed summaries that support quick orientation."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Event & integrity cues"),
                                    html.Ul(
                                        [
                                            html.Li("Event/anomaly flags and indicative classification cues."),
                                            html.Li("Data integrity signals that affect trust in interpretation."),
                                            html.Li("Context markers (scenario tags, regimes, stakeholder-relevant labels)."),
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
                            html.Span("Exact KPI definitions and labels are expected to be driven by metadata/configuration and the selected context (link/pilot)."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SUB-AREAS =================
            html.Div(
                id=sid("sec-subareas"),
                className="wp-section",
                children=[
                    html.H3("CSA sub-areas (how the category is structured)"),
                    html.P(
                        "CSA can be interpreted through three practical sub-areas. These are not separate workflows; "
                        "they are complementary views that support a coherent system-awareness story.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Monitoring & overview"),
                                    html.P("A single place to see the system status and the most important trends."),
                                    html.P("Typical output: ‘what is happening now’ in a consistent language."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Anomaly / event awareness"),
                                    html.P("Deviation cues that highlight unusual behaviour and support operational attention."),
                                    html.P("Typical output: event flags, indicative labels, and pointers for follow-up."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Context & preparation"),
                                    html.P("Context framing for interpretation (time windows, regimes, scenario narratives)."),
                                    html.P("Typical output: traceable assumptions and explanation-oriented summaries."),
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
                        "Quick access to the most relevant tools for Cable System Awareness, including timeline and platform inspection views.",
                        className="wp-par",
                    ),
            
                    # -------- CSA --------
                    html.H4("Cable System Awareness (CSA)"),
                    html.P(
                        "System-level orientation: operational status, event awareness, and timeline/context views.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(                                
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_csa_ta)),
                                    html.P("SCADA-like operational monitoring with integrity cues and early alerting."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_csa_ta, "src": SERVICE_ID, "uid": sid("link-csa-ta")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_csa_ad_ec)),
                                    html.P("Event/anomaly cues that support situational awareness and follow-up."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_csa_ad_ec, "src": SERVICE_ID, "uid": sid("link-csa-ad-ec")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_csa_dtv)),
                                    html.P("Timeline-centric view for navigating events, windows, and supporting evidence."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_csa_dtv, "src": SERVICE_ID, "uid": sid("link-csa-dtv")},
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
                                    html.H5(tool_label(target_csa_st)),
                                    html.P("Platform-level awareness of services and availability (demo/inspection)."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_csa_st, "src": SERVICE_ID, "uid": sid("link-csa-st")},
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
                    html.H3("How CSA connects across the project"),
                    html.P(
                        "CSA is intentionally cross-cutting: it provides a shared situational language that other categories and Work Packages can reference. "
                        "It supports consistent interpretation across tools without hardcoded coupling between components.",
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
                                            html.Li("It groups tools by the user goal: system understanding and context."),
                                            html.Li("It stays independent from timeline: tools can still map to WPs for reporting."),
                                            html.Li("It keeps the platform extensible (new CSA tools join via TAB_META only)."),
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
                                            html.Li("A consistent story for stakeholders (operator/engineer/reviewer)."),
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
                            html.P("End of CSA category overview. Use this page to orient the viewer before opening detailed tools."),
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