import inspect
from dash import html

from tabs_core.tab_menu_renderers import render_tab_menu

def menu_layout():
    """
    Implicit menu layout helper.

    This function MUST be called directly from a tab module.

    The calling module is expected to define:
        - TAB_PREFIX : str
        - TAB_MENU_META : dict (with key 'items')
        - layout_content() -> Dash components

    This is a convention-based API (no arguments by design).
    """

    caller = inspect.getmodule(inspect.stack()[1][0])

    try:
        tab_prefix = caller.TAB_PREFIX
        menu_meta = caller.TAB_MENU_META
        content = caller.layout_content()
    except AttributeError as e:
        raise RuntimeError(
            "menu_layout() requires the calling module to define:\n"
            "  - TAB_PREFIX\n"
            "  - TAB_MENU_META\n"
            "  - layout_content()"
        ) from e

    if not isinstance(menu_meta, dict) or "items" not in menu_meta:
        raise RuntimeError(
            "TAB_MENU_META must be a dict containing an 'items' key"
        )

    return html.Div(
        id=f"{tab_prefix}-root",
        children=[
            html.Div(
                id=f"{tab_prefix}-menu-wrapper",
                children=render_tab_menu(tab_prefix, menu_meta),
            ),
            html.Div(
                id=f"{tab_prefix}-content",
                children=content,
            ),
        ],
    )
