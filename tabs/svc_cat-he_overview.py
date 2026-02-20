"""
Human Engagement (HE) — Category Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a consolidated, category-level narrative for Human Engagement (HE).
- Acts as an anchor page under the HE category, explaining:
  • what this category covers,
  • what “human-in-the-loop” signals are typically reviewed here,
  • how HE supports interpretation, review, and stakeholder-ready outputs.

Platform role:
- This is a category-level overview (not a WP deliverable page).
- It is designed to be meta-driven and reusable across contexts (different links/pilots),
  with minimal or no changes to interrelated components.
- Hyperlink routing is enabled via meta-driven tool links (safe fallback if a tool is missing).

svc_cat-he_overview
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
    
_ALL_HERO_IMAGES = _assets_image_list("cat_he")

TAB_META = {
    "id": "svc-he-overview",
    "label": "Human Engagement Overview",
    "type": "service",

    # Keep it relatively early within the HE tool strip (after CSA/MA)
    "order": 34,

    # Category overview: not tied to a single WP
    "workpackages": [],

    # Anchored strictly to this category label (must match category tab label logic)
    "categories": [
        "Human Engagement"
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

target_he_csc = "svc-cable-structure-context"
target_he_asd = "svc-hvdc-asset-degradation"

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
                            html.H2("Human Engagement (HE) — Category Overview"),
                            html.P(
                                "A structured entry point to HE: human-in-the-loop review, explainability, collaboration, and stakeholder-ready outputs.",
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
                                    html.Span("HE", className="wp-badge wp-badge-strong"),
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
                                            html.Li("Human-in-the-loop review: validation, sign-off, and confidence building."),
                                            html.Li("Explainability & narrative support: turning signals into a readable story."),
                                            html.Li("Stakeholder delivery: reporting, summarisation, and collaboration cues."),
                                        ],
                                        className="wp-list",
                                    ),
                                    html.P(
                                        "Subcategories: • Predictive Maintenance • Accurate Fault Location • Repairs • Cable Ageing.",
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
                    html.H3("Scope of Human Engagement"),
                    html.P(
                        "HE groups the interaction-oriented views that sit between analytics and decisions. "
                        "It focuses on how users interpret results, capture decisions, document evidence, and communicate outcomes "
                        "to different stakeholder roles (operators, engineers, asset managers).",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Interpretation support"),
                                    html.P("Explainable summaries that make analytics actionable and readable."),
                                    html.P("Emphasis: clarity, consistent terminology, and traceable reasoning."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Human-in-the-loop review"),
                                    html.P("Review steps, decisions, and status markers (e.g., accepted / pending / needs follow-up)."),
                                    html.P("Emphasis: accountability and evidence packaging."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Stakeholder-ready outputs"),
                                    html.P("Reporting, handover notes, and collaboration cues that support communication."),
                                    html.P("Emphasis: role-appropriate output and reuse across WPs/categories."),
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
                    html.H3("Signals & KPIs typically reviewed in HE"),
                    html.P(
                        "HE focuses less on raw telemetry and more on the quality of interaction around insights: "
                        "how well insights are explained, reviewed, and translated into decisions. "
                        "Signals can be indicative (demo-ready) and are expected to be driven by metadata/configuration.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-2",
                        children=[
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Review & workflow cues"),
                                    html.Ul(
                                        [
                                            html.Li("Review status (draft / reviewed / approved) and ownership markers."),
                                            html.Li("Annotation/notes coverage for key events, windows, or scenarios."),
                                            html.Li("Follow-up actions: assigned items, handover readiness, and closure cues."),
                                        ],
                                        className="wp-list",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-card",
                                children=[
                                    html.H4("Explainability & trust cues"),
                                    html.Ul(
                                        [
                                            html.Li("Confidence / uncertainty indicators (where applicable)."),
                                            html.Li("Evidence links: supporting charts, windows, assumptions, and thresholds."),
                                            html.Li("Consistency checks: terminology alignment and interpretation warnings."),
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
                            html.Span("Exact HE labels (statuses, roles, review steps) should be driven by configuration and the selected context (link/pilot)."),
                        ],
                    ),
                ],
            ),

            # ================= SECTION: SUB-AREAS =================
            html.Div(
                id=sid("sec-subareas"),
                className="wp-section",
                children=[
                    html.H3("HE sub-areas (how the category is structured)"),
                    html.P(
                        "HE can be interpreted through three practical sub-areas. These are complementary: "
                        "together they help turn analytics into decisions and stakeholder communication.",
                        className="wp-par",
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Explainability & narratives"),
                                    html.P("Readable summaries that explain what changed and why it matters."),
                                    html.P("Typical output: narrative blocks, assumptions, and interpretation guidance."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Review & collaboration"),
                                    html.P("Human workflow around insights: review states, comments, and accountability cues."),
                                    html.P("Typical output: review status, notes, responsibilities, and follow-up prompts."),
                                ],
                            ),
                            html.Div(
                                className="wp-tile",
                                children=[
                                    html.H5("Reporting & handover"),
                                    html.P("Packaging outcomes for stakeholders and reuse across the project."),
                                    html.P("Typical output: report-ready summaries, handover notes, and evidence bundles."),
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
                            "Quick access to tools that support stakeholder context, review-ready views, and asset-oriented communication.",
                            className="wp-par",
                        ),
            
                    # -------- HE --------
                    html.H4("Human Engagement (HE)"),
                    html.P(
                        "Stakeholder-facing context and asset-oriented views that complement CSA narratives.",
                        className="wp-par",
                        style={"marginTop": "18px"},
                    ),
                    html.Div(
                        className="wp-grid-3",
                        children=[
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[
                                    html.H5(tool_label(target_he_csc)),
                                    html.P("Context framing and structure-oriented view to support communication and understanding."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_he_csc, "src": SERVICE_ID, "uid": sid("link-he-csc")},
                                        className="wp-link-muted",
                                    ),
                                ],
                            ),
                            html.Div(
                                className="wp-tile wp-tile-link",
                                children=[                                    
                                    html.H5(tool_label(target_he_asd)),
                                    html.P("Asset-oriented indicators that support stakeholder narratives and decisions."),
                                    html.A(
                                        "Open tool →",
                                        href="#",
                                        id={"type": "tool-link", "target": target_he_asd, "src": SERVICE_ID, "uid": sid("link-he-asd")},
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
                    html.H3("How HE connects across the project"),
                    html.P(
                        "HE is cross-cutting by design: it supports consistent interpretation and communication across categories. "
                        "While other categories generate analytics, HE helps capture the human decision layer around them.",
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
                                            html.Li("It groups tools by user goal: understanding, deciding, and communicating."),
                                            html.Li("It stays independent from timeline (while still supporting WP reporting)."),
                                            html.Li("It standardises how insights are explained and signed-off across tools."),
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
                                            html.Li("Comparable stakeholder outputs across different analytics categories."),
                                            html.Li("Reusable narrative and review patterns with minimal UI ripple effects."),
                                            html.Li("A clean path to extend orchestration (e.g., templates, saved views) later."),
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
                            html.P("End of HE category overview. Use this page to orient the viewer before opening detailed tools."),
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