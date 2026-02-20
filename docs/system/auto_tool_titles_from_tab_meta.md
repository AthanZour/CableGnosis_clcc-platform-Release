# Auto Titles for Overview Tool Tiles (from `TAB_META`)

This change removes hardcoded tool titles (e.g. `html.H5("HVDC Anomaly Detection & Event Classification")`) from overview tiles and replaces them with an automatic lookup from each tool’s `TAB_META["label"]`, keyed by the tool id used in the hyperlink target.

---

## What was implemented

### 1) A shared tool registry

A lightweight registry stores the mapping:

- **tool id → TAB_META**
- Provides helpers to fetch `label` (and/or full meta) by tool id.

Create:

`tabs_core/tool_registry.py`

```python
# tabs_core/tool_registry.py

_TOOL_ID_TO_META = {}

def set_tool_meta(tool_id_to_meta: dict):
    global _TOOL_ID_TO_META
    _TOOL_ID_TO_META = tool_id_to_meta or {}

def tool_label(tool_id: str, default: str | None = None) -> str:
    meta = _TOOL_ID_TO_META.get(tool_id) or {}
    return meta.get("label") or default or tool_id

def tool_meta(tool_id: str) -> dict:
    return _TOOL_ID_TO_META.get(tool_id) or {}
```

---

### 2) Populate the registry in `app.py`

After indexing all service/tool tabs, publish the mapping to the registry:

```python
# Index service/tool tabs: id -> meta, label -> id
for tool in get_service_tabs():
    meta = tool.TAB_META or {}
    tid = meta.get("id")
    lbl = (meta.get("label") or "").strip()
    if tid:
        TOOL_ID_TO_META[tid] = meta
    if lbl:
        TOOL_LABEL_TO_ID[lbl.lower()] = tid

from tabs_core.tool_registry import set_tool_meta
set_tool_meta(TOOL_ID_TO_META)
```

**Important:** this must run **after** `TOOL_ID_TO_META` is fully populated and **before** overview layouts use `tool_label(...)`.

---

### 3) Use the tool id (target) as the single source of truth in overview tiles

**Correct pattern:**

```python
from tabs_core.tool_registry import tool_label

target_cat_id = "svc-hvdc-anomaly-detection"

html.Div(
    className="wp-tile wp-tile-link",
    children=[
        html.H5(tool_label(target_cat_id)),  # auto from TAB_META["label"]
        html.P("SCADA-like operational monitoring with integrity cues and early alerting."),
        html.A(
            "Open tool →",
            href="#",
            id={"type": "tool-link", "target": target_cat_id},
            className="wp-link-muted",
        ),
    ],
)
```

✅ The title updates automatically whenever the referenced tool’s `TAB_META["label"]` changes.

---

## Common pitfall (what we fixed)

❌ Don’t try to “declare” a Python variable as a prop on `html.Div`, e.g.:

```python
html.Div(
    target_cat_id="svc-hvdc-anomaly-detection",  # NOT a variable declaration
    children=[...]
)
```

That’s just a keyword argument passed to the component (and is not supported unless it’s `data-*` / `aria-*`).

---

## Optional: attach target id to the DOM element (data attribute)

If you really want the tile `Div` to carry the id:

```python
target_cat_id = "svc-hvdc-anomaly-detection"

html.Div(
    **{"data-target": target_cat_id},
    className="wp-tile wp-tile-link",
    children=[...],
)
```

---

## Result

- Overview titles are no longer duplicated/hardcoded.
- The hyperlink `target` (tool id) drives both navigation and display name.
- Tool renames happen once: in the tool tab’s `TAB_META["label"]`.
