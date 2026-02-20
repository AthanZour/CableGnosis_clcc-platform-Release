# Orchestrator navigation policies for tool-link hyperlinks (WP + Category ready, extensible)

This note captures the changes and rationale for enabling **tool-link hyperlinks** across the UI, with **mode-aware** behaviour for the orchestrator.

It also documents the **two-level design**:
1) **What modes exist** (declared in the orchestrator dropdown)
2) **How each mode behaves** (policy registry / helpers)

The purpose is to keep discovery untouched, preserve the existing orchestrator logic, and make hyperlink navigation consistent, safe, and extensible.


## What we achieved (summary)

- A hyperlink pattern (`tool-link`) can be placed **anywhere** (overview tabs, category templates, future components).
- When clicked, navigation attempts to select the referenced tool tab.
- Behaviour is **mode-aware**:
  - **per_wp**: may switch WP so the tool becomes visible and is selected.
  - **per_category**: never switches category; navigates only if the tool is visible in the current category; otherwise **no-op**.
- If the target cannot be resolved to a tool id/label, **nothing happens** (safe fallback).
- Discovery of tabs (`discover_tabs`, `TAB_MODULES`, etc.) remains unchanged.


## Key concepts

### Tool-link pattern (global navigation request)
Any link can emit a navigation request using the pattern id:

```python
html.A(
    "Open tool →",
    href="#",
    id={"type": "tool-link", "target": "svc-hvdc-data-timeline"},  # id or label
    className="wp-link-muted",
)
```

- `target` may be the tool id (`TAB_META["id"]`) or the label (`TAB_META["label"]`).
- The orchestrator resolves the target at app level.


## Two-level orchestrator design

### Level 1: Dropdown declaration (what is selectable)
The dropdown menu lists available modes (today: per_wp, per_category).

- Implemented by the existing `ORCHESTRATOR_OPTIONS` list.
- This acts as an allow-list of enabled modes.

**We do not change discovery.** We only read what is already declared/enabled in this dropdown list.


### Level 2: Behaviour policy (how each mode navigates)
We add an app-level policy registry + helpers:

- `ORCHESTRATOR_MODE_POLICIES`: dict mapping mode → behaviour info
- `mode_is_supported(mode)`: safety check (must be enabled in dropdown AND exist in policies)
- `tool_is_visible_in_current_category(tool_id, selected_category)`: reuses existing categorization logic
  (`category_label_from_tab_id`, `services_for_category`) to avoid parallel models.

This enables future modes (e.g., favorites) to be added by:
- enabling the dropdown option
- adding a policy entry
- adding an appropriate “visibility” helper (if needed)


## Why we don’t “just open the tool tab without changing orchestrator state”

If we only swapped central content to show the tool, but did not update orchestrator state:
- the selected tool might not appear in the current tool-bar
- the app could be in Category mode where tools are filtered by category
- result: inconsistent UI (“tool shown but not visible/selectable”), confusing for reviewers and brittle for code

Therefore navigation must remain **state-consistent** with the orchestrator:
- update selected tool store
- update the contextual store only if allowed by the current mode
- otherwise no-op


## Per-mode behaviour (current)

### per_wp (Per Work Package)
- Resolve tool id
- If tool exists, select it
- If tool belongs to another WP, switch WP so it becomes visible in the WP tool-bar
- Category state remains as-is

### per_category (Per Category)
- Resolve tool id
- If tool exists but is NOT part of current category: **no-op** (stay exactly where you are)
- If tool exists in current category: select it
- Does not switch mode or category


## How this was implemented (minimal intervention)

### A) Registry + helpers (meta-driven, no hardcoding)
At startup, we index loaded `TAB_META` to resolve:
- id → meta
- label → id
- WP code → WP tab id

This enables `resolve_tool_id(target)` and `choose_wp_for_tool(tool_id, fallback_wp)`.

For categories, we intentionally rely on the existing categorization functions already used by the UI.

### B) Extend the existing orchestrator click handler (no parallel navigation)
Instead of adding a separate navigation system, we extended the existing callback that handles:
- WP button clicks
- Category button clicks
- Tool button clicks

…to also handle:
- tool-link clicks

This preserves all previously debugged behaviour and only adds a mode-aware branch for tool-link navigation.

### C) Remove forced mode switching
We previously had a callback that forced mode to `per_wp` on tool-link clicks.
That contradicts the per_category requirement (“stay where you are if link is not in category”), so it was removed or turned into a no-op.

The selected mode now governs behaviour through the mode-aware tool-link branch.


## Initialization order gotcha (the NameError you saw)
If a registry block calls helper functions (e.g., `get_wp_tabs()`), it must be placed **after** those helper definitions in `app.py`.
Alternatively, a “no-helper” registry can index `TAB_MODULES` directly.

This was an initialization order issue, not a logic problem.


## Extending to future modes (example: favorites)

To add a new mode later, you can:
1) Add/enable a dropdown option (Level 1)
2) Add a policy entry (Level 2)
3) Add a visibility check helper if needed (e.g., reads `TAB_META["favorites"]`)

The core click handler remains stable; you either:
- add a small branch for the new mode (conservative approach), or
- later refactor to fully dispatch off the policy dict (only if you want).


## Operational checklist

- Use tool id targets where possible (`TAB_META["id"]`) for stability.
- Use labels only when you accept that labels can change.
- If a tool-link does not resolve, it must be a no-op (safe fallback).
- Per_category must not “teleport” the user to another category or mode.


## orchestrator function #1 select option to adopt this function
vars_to_adopt_function_1 = ["per_wp", "per_category"]
