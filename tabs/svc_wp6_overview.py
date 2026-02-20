from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output
from tabs_core.tool_registry import tool_label

"""
WP6 Demonstration & Replicability Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a consolidated overview of WP6 demonstration activities,
  pilot scenarios, and replicability contexts within the CABLEGNOSIS platform.
- Acts as an entry context for understanding how monitoring, analytics,
  and diagnostic tools are showcased and (later) validated during demonstrations.

Platform role:
- Serves as a contextual anchor for WP6, linking demonstration scenarios
  with the underlying platform capabilities without introducing new workflows.
- Designed as a lightweight overview tool supporting dissemination,
  validation readiness (M18), and replication discussions rather than operational use.
"""

TAB_META = {
    "id": "svc-wp6-overview",

    "label": "WP6 Demonstration Overview",

    "type": "service",

    # Keep this high among WP6-related services
    "order": 23,

    # Single WP mapping (contextual anchor)
    "workpackages": ["WP6"],

    # Not assigned to a category
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
# Layout (VISUALLY UNCHANGED – only text updated; ids remain meta-driven)
# ------------------------------------------------------------------

target_wp6_se = "svc-hvdc-scenario-explorer"
target_wp6_dtv = "svc-hvdc-data-timeline"
target_wp6_st = "svc-service-topology"

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
                            html.H2("WP6 Validation, Testing & Evaluation Overview"),
                            html.P("A structured entry point to WP6: how the platform is planned to support validation and testing from M19+ (evidence capture, data-flow checks, and orchestration support), without prescribing WP3/WP6 evaluation methods or review/reporting cues. The structure shown here is indicative and conceptual; it is not a deployment or execution blueprint, but an example of how WP6-related views can be surfaced to C-LCC users.",
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
                                    html.Span("WP6", className="wp-badge wp-badge-strong"),
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
                                    "data-images": (
                                        "/assets/Undersea-Cables.jpeg|"
                                        "/assets/subsea-cables-internet-ai-spooky-pooka-illustration.jpg"
                                    )
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
                                className="wp-card wp6-card-compact",
                                children=[
                                    html.H4("How the platform supports WP6 (from M19+)"),
                                    html.Ul(
                                            [
                                              html.Li("Orchestration support for repeatable runs and consistent evidence packaging (platform scope)."),
                                              html.Li("Data-flow integrity/readiness checks across heterogeneous sources (quality gates, continuity cues, traceable context)."),
                                              html.Li("Execution observability: confirm that integrated tools run as expected and support faster test iterations (without defining validation criteria)."),
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
                                            html.A("Validation flow", href=f"#{sid('sec-scenarios')}", className="wp-jump-btn"),
                                            html.A("Supporting tools", href=f"#{sid('sec-tools')}", className="wp-jump-btn"),
                                            html.A("Replicability", href=f"#{sid('sec-repl')}", className="wp-jump-btn"),
                                        ],
                                    ),
                                    html.P(
                                        "M18 status: platform support plan for WP6 execution from M19+ (evidence capture, data-flow checks, orchestration), not WP6 methodology.",
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
                    html.H3("Partners & roles (WP6 context)"),
                    html.P(
                        "This section summarises who contributes to WP6 planning and execution; this UI highlights only the platform-facing support role (integration, evidence capture, orchestration), not the WP3/WP6 validation methodology.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Coordinator / Platform (platform scope)"),
                                    html.P("Integration stability, test orchestration, evidence views and traceability support."),
                                    html.P("Output: a consistent validation package suitable for review and internal tracking."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Academic & R&D partners (validation logic owners)"),
                                    html.P("Validation logic, indicators/KPIs, and interpretation of results against assumptions."),
                                    html.P("Output: documented checks, expected behaviours, and limits of validity."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Industrial / Pilots (test conditions & acceptance perspective)"),
                                    html.P("Operational realism, test conditions, constraints, and acceptance perspective."),
                                    html.P("Output: pilot-grounded evidence and feedback for refinement of requirements."),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="wp-callout",
                        children=[
                            html.Strong("Note: "),
                            html.Span("Detailed partner assignments are in project documents; this UI focuses on validation-related responsibilities and outputs."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SCENARIOS =================
            html.Div(
                id=sid("sec-scenarios"),
                className="wp-section",
                children=[
                    html.H3("Validation support flow (what the viewer experiences)"),
                    html.P(
                        "WP6 organises testing and validation as a traceable flow: WP6 validation will be executed by the responsible partners; the platform will support it by enabling traceable runs, data readiness checks, and reviewer-readable evidence packaging.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Scenario A — Plan & scope (inputs, assumptions, and evidence needs)"),
                                    html.P("Start from requirements and expected behaviours: what is being validated and under which assumptions."),
                                    html.P("Goal: make the validation plan explicit (scope, checks, and review cues) for M18 readiness."),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/validation.jpg')",
                                            "backgroundSize": "cover",
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
                                    html.H4("Scenario B — Run platform-supported checks & inspect evidence context"),
                                    html.P("Run data integrity / quality gates and validation indicators; inspect results and supporting context."),
                                    html.P("Goal: show how evidence supports (or challenges) the intended capability claims."),
                                    html.Div(
                                        className="wp-media ph wp-media-img",
                                        style={
                                            "backgroundImage": "url('/assets/wp_overview_scenarios/inspection.png')",
                                            "backgroundSize": "cover",
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
                            html.H4("Scenario C — Package evidence & communicate outcomes (method defined by WP6 owners)"),
                            html.P("Package outputs into a clear evaluation story: what passed, what needs refinement, and how results map back to requirements."),
                            html.P("Example explanation"),
                            html.Div(
                                className="wp-media ph wp-media-img",
                                style={
                                    "backgroundImage": "url('/assets/wp_overview_scenarios/communication.jpg')",
                                    "backgroundSize": "cover",
                                    "backgroundPosition": "center",
                                    "backgroundRepeat": "no-repeat",
                                },
                                children="",
                            ),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: TOOLS (WP6) =================
            html.Div(
                id=sid("sec-tools"),
                className="wp-section",
                children=[
                    html.H3("Supporting tools: These tools provide execution support and evidence navigation; they do not define the validation methodology or supports traceability to WP3 requirements (owned by WP3/WP6 partners/ used during validation)."),
                    html.P(
                        "This WP overview acts as a hub; the detailed tools live in their own tabs and are referenced from here as validation support utilities.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp6_se)),
                                    html.P("Define controlled test contexts so that validation checks are interpretable and repeatable."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp6_se,  "src": SERVICE_ID, "uid": sid("link-wp6-se")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp6_dtv)),
                                    html.P("Navigate evidence chronologically: relate checks and outcomes to specific time windows and events."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp6_dtv, "src": SERVICE_ID, "uid": sid("link-wp6-dtv")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_wp6_st)),
                                    html.P("Validation support: verify availability, integration state, and runtime dependencies during tests."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_wp6_st,  "src": SERVICE_ID, "uid": sid("link-wp6-st")},
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
                            html.Span("WP6 is about validation and evaluation: these tools help make tests repeatable and evidence easy to audit."),
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
                        "Replicability is achieved through meta-driven configuration: updates apply universally with minimal (or no) code changes and without breaking interrelated components.",
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
                                    html.H4("What is adjusted per pilot (via metadata)"),
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
                            html.P("End of WP6 overview. Use this page as a guided entry point."),
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