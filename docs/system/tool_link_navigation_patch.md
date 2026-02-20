# Tool-link navigation from WP overviews (meta-driven, safe integration)

This note documents the changes introduced to support **clickable hyperlinks inside WP overview tabs** that navigate to an **actual tool tab** (service) inside the CABLEGNOSIS orchestrator.

The goal: when a user clicks “Open tool →” in a WP overview, the app should **select** the corresponding tool **even if** the user is currently browsing by **Category** (or a different WP). If the tool is not found, **nothing happens** (safe fallback).


## What we changed (high level)

### 1) App-level registry / resolver (meta-driven)
We added a small, **startup-time** registry that indexes already-loaded `TAB_META`:
- `TOOL_ID_TO_META`: tool_id → TAB_META
- `TOOL_LABEL_TO_ID`: label(lower) → tool_id
- `WP_CODE_TO_WP_TAB_ID`: WP code (e.g., “WP6”) → wp-tab id

And helpers:
- `resolve_tool_id(target)`: accepts either a tool **id** or a tool **label** and returns the tool id (or `None`).
- `choose_wp_for_tool(tool_id, fallback_wp_tab_id)`: picks the WP tab where this tool belongs (based on `TAB_META["workpackages"]`).

**Important:** The registry is built from **loaded metadata** (no hardcoded tool lists).


### 2) Pattern-matching link ids in overview tabs
Overview hyperlinks were converted from plain `href="#"` to pattern ids such as:

```python
html.A(
  "Open tool →",
  href="#",
  id={"type": "tool-link", "target": "svc-hvdc-data-timeline"},
  className="wp-link-muted",
)
```

- `target` can be the **tool id** (`TAB_META["id"]`) or the **label** (`TAB_META["label"]`).
- The resolver handles both.


### 3) Orchestrator callback extension (no breaking changes)
We extended the existing callback that already handles:
- WP button clicks
- Category button clicks
- Tool button clicks

…to also accept:
- `Input({"type": "tool-link", "target": ALL}, "n_clicks")`

When a `tool-link` is clicked:
- Resolve tool id; if not found → **no update**
- Choose WP so the tool becomes visible in the WP tool bar
- Return `(new_wp, tool_id, selected_category)`


### 4) Force view mode to `per_wp` on tool-link navigation
To guarantee the tool is reachable even when the user is in **Category view**, we added a small callback:
- If any `tool-link` is clicked, switch `tab-view-mode-store` to `"per_wp"` (only if not already).

This is the minimum intervention that avoids confusing states like:
- “Tool was selected, but is not visible in current Category tool-bar.”


### 5) Optional scroll-to-top on tool selection
We added a simple clientside callback that scrolls to the top whenever `selected-tool-store` changes.
This improves UX when navigating from deep inside an overview page.


## Why this approach (and not “just open the tab”)

### Problem with “just opening the tool tab without changing orchestration state”
If we only changed the central tool content without touching orchestrator state:
- the **selected tool store** might not match the visible tool-bar
- the user could be in **Category mode**, where the tool list is filtered by category
- result: the UI can end up inconsistent (“tool shown but not selectable/visible”), which is confusing and brittle

Navigation must be **state-consistent** with the orchestrator (WP selection + view mode).


### Benefits of the chosen solution
- **Meta-driven**: no hardcoding of tool lists or WPs; everything comes from `TAB_META`.
- **Safe fallback**: if a tool id/label cannot be resolved → no change (no crash, no unexpected state).
- **Minimal coupling**: overview tabs only emit a “navigation request” via a generic `tool-link` pattern id.
- **Future-proof**: tools can be added/removed/renamed as long as `TAB_META` is updated; links can target id or label.
- **Works across views**: even if the user is browsing by Category, tool-link navigation still works by switching to `per_wp` automatically.
- **Does not break existing callbacks**: we extended orchestrator logic rather than adding parallel navigation systems.


## Implementation notes / gotchas

### Initialization order (NameError)
The registry version that calls helpers (`get_wp_tabs()` etc.) must be placed **after** those helper definitions.
Alternatively, use the “no-helper version” that indexes `TAB_MODULES` directly.

This is a pure **initialization order** issue.


### Link targets
Prefer tool ids (`TAB_META["id"]`) as targets for stability.
Labels are supported but can change more easily.


### Non-invasive principle
We intentionally avoided:
- deep URL routing changes
- forced category clearing
- a separate navigation framework

We only enforced what is necessary for coherent app state:
- select tool
- pick WP that contains it
- ensure mode shows tools by WP (`per_wp`)


## Quick checklist for adding links in any overview tab
1. Replace plain `href="#"` links with a `tool-link` pattern id.
2. Set `target` to tool id (recommended) or label.
3. Done — no new per-overview callbacks required.

---
**File purpose:** maintain an auditable explanation of why navigation requires minimal orchestrator participation and how meta-driven design and future compatibility were preserved.
