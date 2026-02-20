"""
WP5 Technologies for the Operational Life & Reliability of Cable Systems (Service Tab)

Purpose (project-facing):
- Provides a consolidated overview of WP5 technologies and capabilities that support
  operational life, reliability, degradation understanding, and lifecycle-oriented decision support.
- Acts as an entry context for understanding how WP5-oriented tooling is showcased through
  demos/pilots and how evidence is packaged for M18 readiness.

Platform role:
- Serves as a contextual anchor for WP5, linking lifecycle-oriented concepts (ageing, degradation,
  maintenance-relevant indicators) to the integrated toolkit tabs.
- Designed as a lightweight overview supporting M18 review packaging and demonstration coherence,
  rather than claiming completed validation or final operational performance.
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
    
_ALL_HERO_IMAGES = _assets_image_list("wp5")


TAB_META = {
    "id": "svc-wp5-overview",

    "label": "WP5 Demonstration Overview",

    "type": "service",

    # Το βάζουμε ψηλά στα WP4-related services
    "order": 21,

    # Μοναδικό WP
    "workpackages": ["WP5"],

    # ❗ Δεν ανήκει σε category
    "categories": [],

    "subcategories": [],

    # Functions intentionally not defined
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

SERVICE_ID = TAB_META["id"]

def sid(suffix: str) -> str:
    return f"{SERVICE_ID}-{suffix}"


# ------------------------------------------------------------------
# Layout (UNCHANGED visually – ids only are meta-driven)
# ------------------------------------------------------------------

target_wp5_duv = "svc-hvdc-data-utilization-validation"
target_wp5_asd = "svc-hvdc-asset-degradation"
target_wp5_and = "svc-hvdc-anomaly-detection"

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
                            html.H2("WP5 Demonstration & Replicability Overview"),
                            html.P(
                                "A quick, structured view of WP5 capabilities supporting operational life and reliability of cable systems, showcased through demos/pilots and evidence packaging for M18 readiness.",
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
                                    html.Span("Overview of", className="wp-badge"),
                                    html.Span("WP5", className="wp-badge wp-badge-strong"),
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
                                className="wp-card WP4-card-compact",
                                children=[
                                    html.H4("What WP5 brings"),
                                    html.Ul(
                                        [
                                            html.Li("Lifecycle-oriented indicators and decision support for operational reliability."),
                                            html.Li("Degradation awareness and remaining-life reasoning as demonstrable capabilities."),
                                            html.Li("Evidence packaging for M18 readiness (concepts, assumptions, and traceable outputs)."),
                                        ],
                                        className="wp-list",
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
                                            html.A("Partners & roles", href=f"#{sid('sec-partners')}", className="wp-jump-btn"),
                                            html.A("Demo walk-through", href=f"#{sid('sec-scenarios')}", className="wp-jump-btn"),
                                            html.A("Aligned tools", href=f"#{sid('sec-tools')}", className="wp-jump-btn"),
                                            html.A("Replicability", href=f"#{sid('sec-repl')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "Note: This page provides an indicative M18-ready overview and evidence framing; "
                                        "it does not claim final operational deployment, validated KPI results, or completed WP6 execution.",
                                        className="wp-note",
                                    ),
                                    html.P(
                                        "M18 status: maintenance-oriented evidence packaging & indicative workflows (not final operational deployment).",
                                        className="wp-note-2",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: PARTNERS =================
            html.Div(
                id=sid("sec-partners"),
                className="wp-section",
                children=[
                    html.H3("Partners & roles (WP5 context)"),
                    html.P(
                        "This section summarises who contributes to WP5-focused demonstration packaging: lifecycle interpretation, degradation concepts, and maintenance-relevant evidence outputs.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Technical & R&D partners"),
                                    html.P("Methods and modelling for ageing/degradation reasoning and lifecycle indicators."),
                                    html.P("Output: explainable building blocks and documented assumptions."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Industrial / pilots"),
                                    html.P("Operational constraints, feasibility checks, and stakeholder relevance for WP5 outputs."),
                                    html.P("Output: realistic demonstration framing and feedback loops."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Platform & integration"),
                                    html.P("Integration of WP5-oriented tools into coherent demo slices and evidence-ready views."),
                                    html.P("Output: curated tool-chain views that support the platform's purpose at the current stage of the project."),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout",
                        children=[
                            html.Strong("Note: "),
                            html.Span("Partner list details are provided in project documents; this UI focuses on WP5 demonstration roles and responsibilities."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SCENARIOS =================
            html.Div(
                id=sid("sec-scenarios"),
                className="wp-section",
                children=[
                    html.H3("Demonstration walk-through (what the viewer experiences)"),
                    html.P(
                        "WP5 frames a coherent story around operational life and reliability: from observed behaviour and indicators to lifecycle interpretation and maintenance-relevant insights.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Scenario A — Operational reliability snapshot"),
                                    html.P("A high-level view of indicative operational status and quality cues relevant to reliability."),
                                    html.P("Goal: demonstrate evidence packaging and readiness of lifecycle-oriented indicators (M18 context)."),
                                    # html.Div(className="wp-media ph", children="(image / diagram placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/reliability_wp5_overview.jpg')",
                                            "backgroundSize": "cover",          # zoom-in / crop
                                            "backgroundPosition": "center",
                                            "backgroundRepeat": "no-repeat",
                                        },
                                        children="",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Scenario B — Degradation & remaining-life narrative"),
                                    html.P("A guided transition from observations to lifecycle interpretation (degradation cues, RUL-style reasoning)."),
                                    html.P("Goal: demonstrate explainability and traceable assumptions in lifecycle analytics (readiness)."),
                                    # html.Div(className="wp-media ph", children="(chart placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/degradation_wp5_overview.jpg')",
                                            "backgroundSize": "cover",          # zoom-in / crop
                                            "backgroundPosition": "center",
                                            "backgroundRepeat": "no-repeat",
                                        },
                                        children="",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-card",
                        children=[
                            html.H4("Scenario C — Maintenance-relevant evidence"),
                            html.P("A demonstration of how outputs can be packaged into evidence blocks for stakeholders (what to trust and why)."),
                            html.P("Example Explanation."),
                            # html.Div(className="wp-media ph", children="(map / topology placeholder)"),
                            html.Div(
                                className="wp-media ph wp-media-img",
                                style={
                                    "backgroundImage": "url('/assets/wp_overview_scenarios/Maintenance_wp5_overview.jpg')",
                                    "backgroundSize": "cover",          # zoom-in / crop
                                    "backgroundPosition": "center",
                                    "backgroundRepeat": "no-repeat",
                                },
                                children="",
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: TOOLS (WP5) =================
            html.Div(
                id=sid("sec-tools"),
                className="wp-section",
                children=[
                    html.H3("Tools showcased (WP navigation)"),
                    html.P(
                        "This WP overview acts as a hub; the detailed tools live in their own tabs and are referenced from here.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp5_duv)),
                                    html.P("Visibility of data pipelines and readiness: utilization KPIs and validation-oriented views."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp5_duv, "src": SERVICE_ID, "uid": sid("link-wp5-duv")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[

                                    html.H5(tool_label(target_wp5_asd)),
                                    html.P("Conceptual lifecycle indicators and remaining-life estimation from stress/monitoring signals."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp5_asd, "src": SERVICE_ID, "uid": sid("link-wp5-asd")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[                                    
                                    html.H5(tool_label(target_wp5_and)),
                                    html.P("Early-stage anomaly/event identification to support pre-fault awareness and validation demos."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp5_and, "src": SERVICE_ID, "uid": sid("link-wp5-and")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout",
                        children=[
                            html.Strong("Tip: "),
                            html.Span("This set keeps WP5 focused on validation, lifecycle reasoning, and diagnostic intelligence."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: REPLICABILITY =================
            html.Div(
                id=sid("sec-repl"),
                className="wp-section",
                children=[
                    html.H3("Replicability framing"),
                    html.P(
                        "Replicability is supported through meta-driven configuration: adjustments are applied consistently with minimal (or no) changes, without breaking interrelated components across the toolkit.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("How replication is achieved (meta-driven)"),
                                    html.Ul(
                                        [
                                            html.Li("Configuration-first approach: labels, assumptions, and context are driven by metadata."),
                                            html.Li("Consistent propagation: updates apply across dependent views and linked tools."),
                                            html.Li("Loose coupling: fewer manual edits across interrelated components and services."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("What is adjusted per context (via metadata)"),
                                    html.Ul(
                                        [
                                            html.Li("Asset/link descriptors, lifecycle assumptions, and stakeholder emphasis."),
                                            html.Li("Thresholds, labels, and scenario parameters relevant to the link context."),
                                            html.Li("Evidence packaging focus (what to highlight for reliability/lifecycle decisions)."),
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
                            html.P("End of WP5 overview. Use this page as a guided entry point."),
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
        Input("selected-tool-store", "data"),
    )