# Tool-link Navigation (Scope-aware) – Change Log

**File:** `app.py`  
**Context:** Dash orchestrator navigation for overview-page hyperlinks (`id={"type":"tool-link","target":"..."}`)  
**Goal:** When a user clicks an “Open tool →” link, navigation should prefer the *currently active scope* (current WP or current Category) and only fall back to switching scope when policy allows it.

---

## Summary of what changed

### 1) Added a scope-aware visibility helper
**Added:** `tool_is_visible_in_scope(tool_id, mode, selected_wp, selected_category)`

**Purpose**
- Answers: **“Is this tool already visible in the current orchestrator scope?”**
- Uses the same service builders as the UI (`services_for_wp(...)`, `services_for_category(...)`) so the decision matches what the toolbar actually renders.

**Behaviors**
- `mode == "per_wp"` → checks the currently selected WP’s service list.
- `mode == "per_category"` / `mode == "per_cat"` → checks the currently selected Category’s service list.
- **Safe by design:** returns `False` on missing inputs or any error (never crashes navigation).

**Why it matters**
- Prevents incorrect jumps when a tool is declared in multiple WPs (e.g., `["WP4","WP5"]`) but is *already visible* in the current WP.
- Keeps the user’s mental context stable: “I clicked from WP5 overview, so if the tool is in WP5 scope, stay in WP5.”

---

### 2) Updated tool-link click handling to prefer “stay in scope”
**Change:** In the tool-link click handler logic, navigation now follows a two-step policy:

1. **Scope-first**:  
   If `tool_is_visible_in_scope(...)` is `True`, **do not switch WP/category**, just select the tool.
2. **Policy fallback** (only if not visible in current scope):
   - **Per-category mode:** no scope switching → **no-op** (stay where you are).
   - **Per-WP mode:** scope switching allowed → use `choose_wp_for_tool(...)` to move to a WP where the tool is visible.

This preserves SCADA-style “no unexpected jumps” in category mode and keeps per-WP mode functional for tools that truly belong elsewhere.

---

### 3) Kept `choose_wp_for_tool(...)` as the WP fallback resolver
**Role**
- When per-WP mode must switch scope, `choose_wp_for_tool` selects an appropriate WP tab based on the tool’s `TAB_META["workpackages"]`.
- If none match, it falls back to the currently selected WP (no crash).

**Why this is the right place for switching**
- The overview hyperlink handler should not “guess” WPs directly.
- It defers to a single resolver function, so future policy changes remain centralized.

---

### 4) Optional debug tracing (temporary)
**Added (optional):** A `print(...)` statement that logs:
- mode, selected WP/category, target, resolved tool id, visibility-in-scope, and tool workpackages.

**Usage**
- Keep while testing (local + server), remove once confirmed stable.

---

## Why this approach (instead of “always open the tab and select tool”)

A naïve approach (“just select tool id and let the UI show it”) fails in per-WP/per-category orchestrator modes because:

- The **toolbar list is scope-filtered** (WP or Category).
- If you select a tool that is not in the current toolbar scope, the UI can look inconsistent:
  - the selected tool may not appear in the tool bar,
  - the user loses orientation (“why did it select something I can’t see?”).

This patch makes navigation **policy-driven, deterministic, and user-trust-friendly**:
- **Prefer minimal movement** (stay in the current scope whenever possible).
- Only switch scope when the mode explicitly allows it (per-WP).
- Keep per-category behavior “non-disruptive” (no automatic category switching).

---

## Files touched

- `app.py`  
  - Added `tool_is_visible_in_scope(...)`
  - Updated tool-link click handler to “scope-first” behavior
  - (Optional) Added debug print

---

## Notes / Gotchas

- Ensure the `mode` string used by the orchestrator matches the helper (`"per_wp"`, `"per_category"` or `"per_cat"`).
- In category mode, make sure `services_for_category(...)` receives the right “category label/code” (depending on your category registry). If needed, keep using your existing conversion helper (e.g. `category_label_from_tab_id(...)`).

