"""
tab_menu_orchestrator.py
============================================================
Reusable tab menu orchestrator for Dash-based applications.

Purpose:
- Provides a standard, reusable tool-menu (tab-level navigation)
- Supports hide / show behavior
- Designed to be imported and used by individual tab modules
- Keeps rendering logic centralized and declarative

Important:
- This module does NOT own TAB_META or TAB_MENU_META
- Each tab defines its own metadata and passes it in
- This file should remain UI-agnostic and orchestration-focused
============================================================
"""

"""
INTEGRATION GUIDE
------------------------------------------------------------
This module is a UI utility library.
It does NOT define a Dash tab by itself.

To use it inside a tab module:

1. Define TAB_MENU_META locally in your tab file
2. Import the required helpers:
       from roots.tabs_core.tab_menu_orchestrator import (
           render_tab_menu,
           render_section,
           register_tab_menu_callbacks,
       )

3. Inside your tab layout():
       html.Div(
           children=[
               render_tab_menu(TAB_PREFIX, TAB_MENU_META),
               render_section(...),
               ...
           ]
       )

4. During app initialization, register callbacks:
       register_tab_menu_callbacks(app, TAB_PREFIX)

Important:
• This module assumes the CSS contract is loaded
• DOM ids are derived from TAB_PREFIX
• This file must remain domain-agnostic
------------------------------------------------------------
"""

from dash import html, dcc


# ============================================================
# TAB MENU META – EXAMPLE / REFERENCE ONLY
# ============================================================
# NOTE:
# This dictionary is NOT used directly by the orchestrator.
# It exists purely as:
#   • documentation-by-example
#   • a copy/paste starting point for new tabs
#   • a reference for the expected menu schema
#
# Each tab MUST define its own TAB_MENU_META locally.
# ============================================================

TAB_MENU_META_EXAMPLE = {
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
# CONSTANTS / CONVENTIONS
# ============================================================

# NOTE:
# The prefix MUST be provided by the consuming tab.
# It is used to namespace DOM ids safely across tabs.
#
# Example:
#   TAB_PREFIX = "svc-lifecycle"
#
# This module assumes the prefix is passed explicitly.
# ============================================================


# ============================================================
# TAB MENU RENDERER
# ============================================================

def render_tab_menu(tab_prefix: str, menu_meta: dict):
    """
    Render the sticky tab-level tool menu.

    Parameters
    ----------
    tab_prefix : str
        Unique prefix for the tab (used for DOM id namespacing)

    menu_meta : dict
        Dictionary describing the menu structure.
        Expected shape:
        {
            "default": "overview",
            "items": [
                {"id": "overview", "label": "Overview"},
                ...
            ]
        }

    Returns
    -------
    dash.html.Div
        Fully rendered tab menu container (including hide/show controls)
    """

    return html.Div(
        id=f"{tab_prefix}-tab-tool-menu-container-shell",
        className="tab-tool-menu-container",
        children=[
            # ----------------------------------------------------
            # Internal UI state (menu visibility)
            # ----------------------------------------------------
            dcc.Store(
                id=f"{tab_prefix}-menu-visible",
                data=True
            ),

            # ----------------------------------------------------
            # Main segmented menu
            # ----------------------------------------------------
            html.Div(
                id=f"{tab_prefix}-menu",
                className="tab-tool-menu",
                children=[
                    *[
                        html.Button(
                            item["label"],
                            className="tab-tool-menu-item",
                            **{"data-target": item["id"]},
                        )
                        for item in menu_meta.get("items", [])
                    ],

                    # --------------------------------------------
                    # Hide menu control
                    # --------------------------------------------
                    html.Button(
                        html.Div(
                            className="tab-menu-hide-icon-wrapper",
                            children=html.Img(
                                src="/assets/hide_tab_menu.png",
                                alt="Hide menu",
                                className="tab-menu-icon",
                            ),
                        ),
                        id=f"{tab_prefix}-menu-hide",
                        className="tab-tool-menu-hide",
                    ),
                ],
            ),

            # ----------------------------------------------------
            # Collapsed "show menu" control
            # ----------------------------------------------------
            html.Div(
                id=f"{tab_prefix}-menu-show-wrapper",
                className="tab-tool-menu-show-wrapper",
                children=html.Button(
                    html.Img(
                        src="/assets/show_menu.png",
                        alt="Show menu",
                        className="tab-menu-icon",
                    ),
                    id=f"{tab_prefix}-menu-show",
                    className="tab-tool-menu-collapsed",
                    style={"display": "none"},
                ),
            ),
        ],
    )


# ============================================================
# GENERIC SECTION RENDERER
# ============================================================

def render_section(section_id: str, title: str, content: list):
    """
    Render a standard content section inside a tab.

    Parameters
    ----------
    section_id : str
        DOM id of the section (used for menu targeting)

    title : str
        Section title (rendered as H4)

    content : list
        List of Dash components forming the section body

    Returns
    -------
    dash.html.Div
        Rendered section block
    """

    return html.Div(
        id=section_id,
        style={"padding": "48px 0"},
        children=[
            html.H4(title),
            *content
        ],
    )

# ============================================================
# CALLBACKS – TAB MENU HIDE / SHOW
# ============================================================
# NOTE:
# • These callbacks manage ONLY UI visibility state
# • No coupling to app logic, data, or navigation
# • Safe to register from any tab module
# • Relies on a consistent DOM id contract
# ============================================================

from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate


def register_tab_menu_callbacks(app, tab_prefix: str):
    """
    Register hide / show callbacks for a tab tool menu.

    Parameters
    ----------
    app : dash.Dash
        Dash application instance

    tab_prefix : str
        DOM id prefix used by the tab menu.
        Must match the ids used in render_tab_menu().
        Example:
            tab_prefix = "svc-lifecycle"
    """

    @app.callback(
        Output(f"{tab_prefix}-menu", "style"),
        Output(f"{tab_prefix}-menu-show", "style"),
        Output(f"{tab_prefix}-menu-visible", "data"),
        Input(f"{tab_prefix}-menu-hide", "n_clicks"),
        Input(f"{tab_prefix}-menu-show", "n_clicks"),
        State(f"{tab_prefix}-menu-visible", "data"),
        prevent_initial_call=True,
    )
    def _toggle_tab_menu(hide_clicks, show_clicks, visible):
        """
        Toggle visibility of the tab menu.

        Behavior:
        • Hide button collapses the menu and reveals the show control
        • Show button restores the menu
        • State is stored in a dcc.Store (menu-visible)

        Returns
        -------
        tuple:
            (
                menu_style: dict,
                show_button_style: dict,
                visible: bool
            )
        """

        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # ----------------------------------------------------
        # HIDE MENU
        # ----------------------------------------------------
        if trigger_id.endswith("menu-hide"):
            return (
                {
                    "visibility": "hidden",
                    "opacity": 0,
                    "pointerEvents": "none",
                    "height": 0,
                    "overflow": "hidden",
                },
                {
                    "visibility": "visible",
                    "opacity": 1,
                    "pointerEvents": "auto",
                },
                False,
            )

        # ----------------------------------------------------
        # SHOW MENU
        # ----------------------------------------------------
        if trigger_id.endswith("menu-show"):
            return (
                {
                    "visibility": "visible",
                    "opacity": 1,
                    "pointerEvents": "auto",
                    "height": "auto",
                },
                {
                    "visibility": "hidden",
                    "opacity": 0,
                    "pointerEvents": "none",
                },
                True,
            )

        raise PreventUpdate