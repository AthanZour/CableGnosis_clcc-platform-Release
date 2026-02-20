"""
WP4 Architecture & Platform Demonstration Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a consolidated overview of WP4 platform and integration outcomes,
  focusing on the C-LCC unified architecture, implementation approach, and M18 demo framing.
- Acts as an entry context for understanding how the platform orchestrates heterogeneous tools,
  services, and partner contributions without enforcing a single implementation model.

Platform role:
- Serves as a contextual anchor for WP4, linking the platform architecture (frontend orchestration,
  backend services, data layers) with the integrated toolkit tabs.
- Designed as a lightweight overview supporting architectural readiness and integration capability
  (M18), rather than operational or production performance claims.
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
    
_ALL_HERO_IMAGES = _assets_image_list("wp4")

TAB_META = {
    "id": "svc-wp4-overview",

    "label": "WP4 Platform Overview",

    "type": "service",

    # Το βάζουμε ψηλά στα WP4-related services
    "order": 21,

    # Μοναδικό WP
    "workpackages": ["WP4"],

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

target_wp4_otva = "svc-hvdc-operational-monitoring"
target_wp4_ta = "svc-hvdc-telemetry-analytics"
target_wp4_dt = "svc-hvdc-data-timeline"

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
                            html.H2("WP4 C-LCC Platform & Architecture Overview"),
                            html.P(
                                "A quick, structured view of the C-LCC platform: unified architecture, implementation choices, and the M18 demonstration framing for integration readiness.",
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
                                    html.Span("WP4", className="wp-badge wp-badge-strong"),
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
                            # build once (module-level)
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
                                    html.H4("What WP4 delivers"),
                                    html.Ul(
                                        [
                                            html.Li("Unified C-LCC architecture (frontend orchestration, backend services, data layers)."),
                                            html.Li("Integration approach enabling independent tools to coexist (loose coupling)."),
                                            html.Li("Meta-driven orchestration that supports rapid onboarding and evolution (M18 readiness)."),
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
                                            html.A("Architecture & roles", href=f"#{sid('sec-partners')}", className="wp-jump-btn"),
                                            html.A("Demo walk-through", href=f"#{sid('sec-scenarios')}", className="wp-jump-btn"),
                                            html.A("Aligned tools", href=f"#{sid('sec-tools')}", className="wp-jump-btn"),
                                            html.A("Replicability", href=f"#{sid('sec-repl')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "Note: This page packages WP4 integration readiness for M18; it does not claim final operational workflows or completed validation.",
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

            # ================= SECTION: PARTNERS =================
            html.Div(
                id=sid("sec-partners"),
                className="wp-section",
                children=[
                    html.H3("Architecture & roles (WP4 context)"),
                    html.P(
                        "This section summarises the platform-centric roles behind the C-LCC: orchestration, integration, and onboarding of heterogeneous partner tools.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Frontend orchestration"),
                                    html.P("Navigation, context routing, and metadata-driven composition of aligned tools."),
                                    html.P("Output: consistent entry points and evidence-ready views for the M18 demo."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Backend & services layer"),
                                    html.P("APIs, service isolation, and stable interfaces enabling independent tool execution."),
                                    html.P("Output: reliable integration patterns without hard coupling between tools."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Partner tool onboarding"),
                                    html.P("Heterogeneous tools integrated through common conventions and meta descriptors."),
                                    html.P("Output: progressive expansion of platform capabilities without breaking existing tabs."),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout",
                        children=[
                            html.Strong("Note: "),
                            html.Span("Project document details provide full architecture rationale; this UI focuses on how the platform structure supports integration and demonstration."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SCENARIOS =================
            html.Div(
                id=sid("sec-scenarios"),
                className="wp-section",
                children=[
                    html.H3("M18 demonstration walk-through (what the viewer experiences)"),
                    html.P(
                        "WP4 frames a demonstration that highlights architectural readiness: tool integration, orchestration behaviour, and stable interaction patterns across the platform.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Scenario A — Platform entry & navigation"),
                                    html.P("A guided entry: orchestration, selection-driven context, and tool discovery."),
                                    html.P("Goal: show orchestrated composition and integration readiness (not final operational workflows)."),
                                    # html.Div(className="wp-media ph", children="(image / diagram placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/navigation.jpg')",
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
                                    html.H4("Scenario B — Cross-tool continuity"),
                                    html.P("A short chain across tools: consistent context, shared labels, and stable routing."),
                                    html.P("Goal: demonstrate loose coupling and interoperable presentation across integrated services."),
                                    # html.Div(className="wp-media ph", children="(chart placeholder)"),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/continuity.jpg')",
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
                            html.H4("Scenario C — Evolution & onboarding"),
                            html.P("A guided explanation of how new tools are integrated through metadata and interfaces."),
                            html.P("Example Explanation."),
                            # html.Div(className="wp-media ph", children="(map / topology placeholder)"),
                            html.Div(
                                className="wp-media ph wp-media-img",
                                style={
                                    "backgroundImage": "url('/assets/wp_overview_scenarios/onboarding.jpg')",
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

            # ================= SECTION: TOOLS (WP4) =================
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
                                    html.H5(tool_label(target_wp4_otva)),
                                    html.P("SCADA-like monitoring view: integrity KPIs, real-time trends, and basic alerting cues."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp4_otva, "src": SERVICE_ID, "uid": sid("link-wp4-otva")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp4_ta)),
                                    html.P("A lightweight validation/analytics layer: consistency checks and indicative KPI extraction."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp4_ta,   "src": SERVICE_ID, "uid": sid("link-wp4-ta")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp4_dt)),
                                    html.P("Time-ordered view of events and measurements for quick navigation during inspection."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp4_dt,   "src": SERVICE_ID, "uid": sid("link-wp4-dt")},
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
                            html.Span("These are the core WP4-aligned tools used to present monitoring + validation readiness."),
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
                        "Replicability is supported through meta-driven configuration: adjustments are applied consistently with minimal (or no) changes, without breaking interrelated components across the platform.",
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
                                            html.Li("Configuration-first orchestration: behaviour and presentation are driven by metadata."),
                                            html.Li("Consistent propagation: changes apply across dependent views and integrated tools."),
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
                                            html.Li("Asset/link descriptors and integration parameters (names, mappings, inputs)."),
                                            html.Li("Thresholds, labels, and scenario parameters relevant to the context."),
                                            html.Li("Narrative emphasis for stakeholders and the demonstration focus."),
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
                            html.P("End of WP4 overview. Use this page as a guided entry point."),
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