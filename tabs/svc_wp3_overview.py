"""
WP3 Requirements Engineering & Validation Planning Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a consolidated overview of WP3: stakeholders, requirements engineering (REQ/NFR),
  reference scenarios, validation criteria, and KPI/evaluation planning.
- Acts as an entry context for understanding how requirements and validation planning guide
  the design and orchestration of the CABLEGNOSIS toolkit and its demonstrators.

Platform role:
- Serves as a contextual anchor for WP3, linking requirements/scenarios/KPIs to the platform
  architecture and tool integration logic.
- Designed as a lightweight overview supporting clarity, traceability and M18 readiness packaging,
  rather than operational execution.
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


_ALL_HERO_IMAGES = _assets_image_list("wp3")

TAB_META = {
    "id": "svc-wp3-overview",
    "label": "WP3 Overview",
    "type": "service",

    # Keep this high among WP3-related services
    "order": 20,

    # Single WP mapping (contextual anchor)
    "workpackages": ["WP3"],

    # Not assigned to a category
    "categories": [],
    "subcategories": [],

    "version": "v0.1 (demo)",
    "status": "active",
}

SERVICE_ID = TAB_META["id"]


def sid(suffix: str) -> str:
    return f"{SERVICE_ID}-{suffix}"


# ------------------------------------------------------------------
# Layout (VISUALLY COMPATIBLE – ids remain meta-driven; text WP3-aligned)
# ------------------------------------------------------------------

target_wp3_se = "Pre-fault_Early-warning_&_Diagnostic-Readiness"
target_wp3_csc = "svc-cable-structure-context"

def layout():
    return html.Div(
        id=sid("root"),
        className="wp-overview-tab wp3_overview-root",
        children=[

            # ================= HEADER =================
            html.Div(
                id=sid("header"),
                className="wp-header wp3_overview-header",
                children=[
                    html.Div(
                        className="wp-header-left",
                        children=[
                            html.H2("WP3 Requirements Engineering & Validation Planning Overview"),
                            html.P(
                                "A structured guide to stakeholders, REQ/NFR baseline, reference scenarios, "
                                "validation criteria, and KPI planning that guide the CABLEGNOSIS toolkit and demonstrators.",
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
                                    html.Span("WP3", className="wp-badge wp-badge-strong"),
                                ],
                            )
                        ],
                    ),
                ],
            ),

            # ================= HERO =================
            html.Div(
                id=sid("hero"),
                className="wp-hero wp3_overview-hero",
                children=[
                    html.Div(
                        id=sid("hero-left"),
                        className="wp-hero-left",
                        children=[
                            html.Div(
                                id=sid("hero-image_wp_over"),
                                className="wp-hero-image wp3_overview-hero-image",
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
                            html.Div(id=sid("cursor"), className="wp-cursor"),
                        ],
                    ),

                    html.Div(
                        id=sid("hero-right"),
                        className="wp-hero-right",
                        children=[
                            html.Div(
                                className="wp-card wp-card-compact wp3_overview-card-compact",
                                children=[
                                    html.H4("What WP3 delivers"),
                                    html.Ul(
                                        [
                                            html.Li("Stakeholder context: who needs what, and why."),
                                            html.Li("REQ/NFR baseline to guide technology and toolkit design."),
                                            html.Li("Reference scenarios with validation criteria and KPI planning."),
                                            html.Li("Architecture guidance for how components orchestrate into the C-LCC."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),

                            html.Div(
                                className="wp-card wp-card-compact wp3_overview-card-compact",
                                children=[
                                    html.H4("Quick jump"),
                                    html.Div(
                                        className="wp-jump wp3_overview-jump",
                                        children=[
                                            html.A("Stakeholders", href=f"#{sid('sec-stakeholders')}", className="wp-jump-btn"),
                                            html.A("REQ & NFR baseline", href=f"#{sid('sec-req')}", className="wp-jump-btn"),
                                            html.A("Scenarios & criteria", href=f"#{sid('sec-scenarios')}", className="wp-jump-btn"),
                                            html.A("KPIs & evaluation plan", href=f"#{sid('sec-kpis')}", className="wp-jump-btn"),
                                            html.A("Traceability", href=f"#{sid('sec-trace')}", className="wp-jump-btn"),
                                            html.A("Replicability", href=f"#{sid('sec-repl')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "Note: This page packages WP3 logic for clarity and integration readiness; "
                                        "it does not claim final KPI results or completed on-site validation.",
                                        className="wp-note",
                                    ),
                                    html.P(
                                        "M18 status: integration & orchestration readiness demonstration (navigation, routing, stable interaction patterns / indicative M18 framing; not final operational workflows).",
                                        className="wp-note-2",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: STAKEHOLDERS =================
            html.Div(
                id=sid("sec-stakeholders"),
                className="wp-section wp3_overview-section",
                children=[
                    html.H3("Stakeholders & context (WP3)"),
                    html.P(
                        "WP3 starts from stakeholders and demonstrators: it frames needs, constraints, and what "
                        "“success” means before tools and analytics are assessed.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3 wp3_overview-grid",
                        children=[
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("TSOs / Operators"),
                                    html.P("Need: reliability, situational awareness, actionable indicators."),
                                    html.P("WP3 output: requirements and evaluation criteria aligned to operations."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("Technology developers / labs"),
                                    html.P("Need: clear REQ/NFR targets and validation boundaries."),
                                    html.P("WP3 output: scenario-driven validation criteria and KPI definitions."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("Platform integrators"),
                                    html.P("Need: orchestration guidance and stable integration assumptions."),
                                    html.P("WP3 output: reference architecture guidance and interface expectations."),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout wp3_overview-callout",
                        children=[
                            html.Strong("WP3 scope: "),
                            html.Span(
                                "requirements engineering + validation planning, including reference scenarios "
                                "and evaluation criteria (economic, technical, environmental KPIs)."
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: REQ/NFR =================
            html.Div(
                id=sid("sec-req"),
                className="wp-section wp3_overview-section",
                children=[
                    html.H3("REQ & NFR baseline (what must be satisfied)"),
                    html.P(
                        "WP3 formulates functional and non-functional requirements and clarifies interrelations "
                        "and orchestration into the C-LCC platform.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2 wp3_overview-grid",
                        children=[
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("Functional requirements (REQ)"),
                                    html.Ul(
                                        [
                                            html.Li("Define required capabilities per demonstrator and tool-chain stage."),
                                            html.Li("Specify expected inputs/outputs, roles, and dependencies."),
                                            html.Li("Bind requirements to reference scenarios and validation criteria."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("Non-functional requirements (NFR)"),
                                    html.Ul(
                                        [
                                            html.Li("Usability and interpretability for stakeholders."),
                                            html.Li("Data integrity, traceability, and reproducibility of results."),
                                            html.Li("Integration constraints: interfaces, modularity, and loose coupling."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout wp3_overview-callout",
                        children=[
                            html.Strong("Practical note: "),
                            html.Span(
                                "The REQ/NFR repository and mapping artefacts are maintained as living references; "
                                "this overview summarises the intent and how it connects to platform orchestration."
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SCENARIOS =================
            html.Div(
                id=sid("sec-scenarios"),
                className="wp-section wp3_overview-section",
                children=[
                    html.H3("Reference scenarios & validation criteria"),
                    html.P(
                        "WP3 defines reference scenarios (use cases) and the validation criteria that will later be "
                        "used to assess demonstrator outcomes.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2 wp3_overview-grid",
                        children=[
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("Scenario blocks"),
                                    html.Ul(
                                        [
                                            html.Li("Context: asset/link, stakeholders, constraints."),
                                            html.Li("Trigger: conditions that initiate the scenario."),
                                            html.Li("Expected behaviour: what services should demonstrate."),
                                        ],
                                        className="wp-list",
                                    ),
                                    # html.Div(className="wp-media ph wp3_overview-media", children="(scenario diagram placeholder)"),
                                                                        # html.Div(className="wp-media ph", children="(chart placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/stakeholders.jpg')",
                                            "backgroundSize": "cover",          # zoom-in / crop
                                            "backgroundPosition": "center",
                                            "backgroundRepeat": "no-repeat",
                                        },
                                        children="",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("Validation criteria"),
                                    html.Ul(
                                        [
                                            html.Li("Acceptance logic: what counts as a successful demonstration."),
                                            html.Li("Evidence types: plots, tables, logs, assumptions."),
                                            html.Li("Link to KPIs: how the evaluation is computed or justified."),
                                        ],
                                        className="wp-list",
                                    ),
                                    # html.Div(className="wp-media ph wp3_overview-media", children="(criteria / evidence placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/criteria.jpg')",
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
                ],
            ),
            

            # ================= SECTION: KPI PLAN =================
            html.Div(
                id=sid("sec-kpis"),
                className="wp-section wp3_overview-section",
                children=[
                    html.H3("KPI & evaluation planning (economic / technical / environmental)"),
                    html.P(
                        "WP3 sets the evaluation criteria for demonstrators, including KPI families and how they "
                        "will be computed and compared against proposal-stage targets during later validation phases.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3 wp3_overview-grid",
                        children=[
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("Technical KPIs"),
                                    html.P("Performance, reliability cues, integrity indicators, and demonstrator-specific metrics."),
                                    html.P("Focus: interpretability + traceable computation logic."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("Economic KPIs"),
                                    html.P("Cost drivers, lifecycle trade-offs, deployment/maintenance considerations."),
                                    html.P("Focus: consistent assumptions and comparable baselines."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp3_overview-tile",
                                children=[
                                    html.H5("Environmental KPIs"),
                                    html.P("Material and lifecycle impacts, recyclability-related indicators where relevant."),
                                    html.P("Focus: evidence packaging and clear boundaries of assessment."),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout wp3_overview-callout",
                        children=[
                            html.Strong("Important: "),
                            html.Span(
                                "At M18 the platform demonstrates integration readiness and the ability to package KPI evidence; "
                                "it does not assert final KPI achievement without the later WP validation cycles."
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: TOOLS (WP3) =================
            html.Div(
                id=sid("sec-tools"),
                className="wp-section",
                children=[
                    html.H3("Tools showcased (WP navigation)"),
                    html.P(
                        "This overview acts as a hub; the detailed tools live in their own tabs and are referenced from here.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(                             
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp3_se)),
                                    html.P(
                                        "Scenario definition and pre-fault preparation blocks used to support consistent validation planning and repeatable walkthroughs.",
                                    ),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp3_se, "src": SERVICE_ID, "uid": sid("link-wp3-se")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp3_csc)),
                                    html.P(
                                        "Cable structure and material context view that anchors terminology and shared understanding across planning and validation activities.",
                                    ),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp3_csc, "src": SERVICE_ID, "uid": sid("link-wp3-csc")},
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
                            html.Span(
                                "Use these shortcuts to move from planning context into concrete scenario definition and shared cable context."
                            ),
                        ],
                    ),
                ],
            ),
            
            
            # ================= SECTION: TRACEABILITY =================
            html.Div(
                id=sid("sec-trace"),
                className="wp-section wp3_overview-section",
                children=[
                    html.H3("Traceability (Use Case ↔ REQ/NFR ↔ Validation ↔ Evidence)"),
                    html.P(
                        "Traceability is the core WP3 value: each requirement should be explainable via a use case, "
                        "validated by criteria, and supported by evidence artifacts.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2 wp3_overview-grid",
                        children=[
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("Traceability chain"),
                                    html.Ul(
                                        [
                                            html.Li("Use cases anchor stakeholder needs and context."),
                                            html.Li("REQ/NFR specify expected capability and constraints."),
                                            html.Li("Validation criteria define what evidence is acceptable."),
                                            html.Li("Platform packaging enables consistent evidence collection."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card wp3_overview-card",
                                children=[
                                    html.H4("How this connects to the platform"),
                                    html.Ul(
                                        [
                                            html.Li("Metadata-driven orchestration ties tools to scenarios and labels."),
                                            html.Li("Loose coupling supports independent tool evolution."),
                                            html.Li("A shared vocabulary reduces ambiguity across WPs."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout wp3_overview-callout",
                        children=[
                            html.Strong("Tip: "),
                            html.Span("If you later add a dedicated mapping viewer tab, link it from here."),
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
                        "Replicability is supported by meta-driven configuration: adjustments are applied universally "
                        "with minimal (or no) changes, without breaking interrelated components.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("What is configured (meta-driven)"),
                                    html.Ul(
                                        [
                                            html.Li("Asset/link context, stakeholder focus, and scenario descriptions."),
                                            html.Li("REQ/NFR mappings, terminology, and validation criteria labels."),
                                            html.Li("KPI thresholds and interpretation cues aligned to each demonstrator."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("How changes propagate"),
                                    html.Ul(
                                        [
                                            html.Li("Universal application across dependent views and tool tabs."),
                                            html.Li("Stable interfaces: minimal manual edits across components."),
                                            html.Li("Consistent packaging of evidence and assumptions for each context."),
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
                            html.P("End of WP3 overview. Use this page as a guided entry point."),
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