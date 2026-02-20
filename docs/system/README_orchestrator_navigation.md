# Orchestrator Navigation Fixes (Dash) — README

This document summarizes the changes made to fix orchestrator tool navigation and prevent `DuplicateIdError`
when multiple overview pages link to the same tool/tab.

---

## 1) Problem

### A. Duplicate IDs (Dash error)
Dash raised:

- `dash.exceptions.DuplicateIdError: Duplicate component id found in the initial layout: {"type":"tool-link","target":"..."}`

Root cause: multiple overview layouts created identical dict-ids for hyperlinks like:

```python
id={"type": "tool-link", "target": "<tool-id>"}
```

When multiple tabs/pages are present in the initial layout, Dash requires **every component id** to be unique.

### B. Orchestrator "Tools" results not clickable
After updating callbacks to match the new id structure, the orchestrator search results (tool hits)
still used the old id shape, so clicks did not trigger navigation.

### C. Wrong navigation in `per_category` and no mode switch from `per_wp`
- In `per_category`, clicking a tool from another category did not switch to the correct category.
- In `per_wp`, clicking a category-overview tool did nothing (did not switch to `per_category`).

---

## 2) Solution Overview

### A. Make tool-link IDs unique everywhere
All tool hyperlinks now use **four keys**:

- `type`: `"tool-link"`
- `target`: tool/tab id (string)
- `src`: where the link was created (page/service identifier)
- `uid`: unique per-link id

**New standard**
```python
id={"type": "tool-link", "target": target_tool_id, "src": SERVICE_ID, "uid": sid("link-<name>")}
```

This prevents duplicate IDs even if multiple pages link to the same `target`.

### B. Update Dash pattern-matching callbacks
In `app.py`, callbacks that listen to tool links must match the exact id shape.
Inputs were updated from:

```python
Input({"type": "tool-link", "target": ALL}, "n_clicks")
Input({"type": "tool-link", "target": ALL}, "n_clicks_timestamp")
```

to:

```python
Input({"type": "tool-link", "target": ALL, "src": ALL, "uid": ALL}, "n_clicks")
Input({"type": "tool-link", "target": ALL, "src": ALL, "uid": ALL}, "n_clicks_timestamp")
```

The navigation logic continues to read:
```python
tool_id = resolve_tool_id(tid.get("target"))
```
so extra keys do not affect routing.

### C. Fix orchestrator tool hits to use the new id shape
Orchestrator “tool hits” now also include `src/uid`:

```python
id={
  "type": "tool-link",
  "target": hit["tool_id"],
  "src": "orchestrator",
  "uid": f"orch-{hit['tool_id']}",
}
```

### D. Correct behaviour for per-category navigation
When clicking a tool link in `per_category`, the app now may **switch the selected category**
to the category that owns the tool (based on `TOOL_ID_TO_META[tool_id]["categories"]`).

### E. Mode switch from per-wp → per-category for category overview links
A small callback (e.g. `force_per_wp_on_tool_link`) is used to switch the orchestrator mode to
`per_category` when the clicked tool is a category-overview tool (has categories but not workpackages).

---

## 3) What changed (high-level checklist)

### Overview pages (wp/category overviews)
✅ All `tool-link` component ids changed to include `src` + `uid`.

Example:
```python
id={"type": "tool-link", "target": target_wp4_dt, "src": SERVICE_ID, "uid": sid("link-wp4-dt")}
```

### app.py
✅ Callback Inputs updated to match `{"type","target","src","uid"}`.

✅ Orchestrator tool hits updated (search results).

✅ `per_category` behaviour improved to route to the correct category when a tool belongs elsewhere.

✅ Optional mode switch added for category-overview tool links.

---

## 4) Compatibility with future features (Favorites, etc.)

### ✅ Yes — compatible, with one important rule:
Any **new clickable option that should behave like a tool link** must either:

1) Use the same tool-link id schema:
```python
id={"type": "tool-link", "target": "<tool-id>", "src": "<feature>", "uid": "<unique>"}
```

or

2) Use a **different `type`** and have its own callback, e.g.:
```python
id={"type": "favorite-link", "target": "<tool-id>", "uid": "..."}
```

#### Why this is future-proof
- Dash pattern-matching is based on dict keys.
- Because we standardized tool navigation on `type="tool-link"` with `target/src/uid`,
  you can add as many new tool-link sources (favorites, recent, recommended, etc.) as you want
  without collisions as long as `uid` is unique.

### Recommended pattern for Favorites
If favorites trigger normal navigation to a tool:
```python
id={"type": "tool-link", "target": tool_id, "src": "favorites", "uid": f"fav-{tool_id}"}
```

If favorites need extra behaviour (toggle pin/unpin, reorder, etc.), use a different type:
```python
id={"type": "favorite-toggle", "target": tool_id, "uid": f"fav-toggle-{tool_id}"}
```

### Extra note: avoiding duplicates
- `uid` must be unique among all tool-links in the initial layout.
- Using `sid("...")` inside a page/module is a good default.
- For dynamically generated lists (favorites), prefix the uid with the feature name:
  - `fav-<tool_id>`
  - `recent-<tool_id>`
  - `rec-<tool_id>-<rank>`

---

## 5) Quick smoke tests

1. Open app fresh → no `DuplicateIdError`.
2. Orchestrator → search tools → click a tool hit → navigates.
3. per_category → click tool from another category → switches category and opens tool.
4. per_wp → click a category overview tool (e.g. Human Engagement Overview) → switches to per_category and opens.

---

## 6) TL;DR

- Standardize all navigation links on:
  `{"type":"tool-link","target":..., "src":..., "uid":...}`
- Ensure callbacks match the same keys.
- New features like Favorites are fully compatible as long as they follow the same schema (or use a different `type`).
