\# Tab Metadata Conventions



\## Purpose



This document defines the conventions and responsibilities of metadata used

by tabs (tools/services) within the platform.



The goal is to clearly separate \*\*platform-level orchestration concerns\*\*

from \*\*tool-level internal behavior\*\*, ensuring modularity, scalability,

and long-term maintainability.



---



\## Metadata Types Overview



Two distinct metadata categories are used:



\- `TAB\_META` – platform-facing metadata

\- Tool-specific metadata (e.g. `TAB\_MENU\_META`) – tool-internal metadata



These metadata types serve \*\*different architectural roles\*\* and must not be mixed.



---



\## TAB\_META (Platform-Level Metadata)



\### Role



`TAB\_META` is used exclusively by the \*\*application orchestrator\*\* (`app.py`)

to discover, categorize, and organize tabs.



It defines \*\*what the tab is\*\*, not how it behaves internally.



\### Typical Responsibilities



\- Tab identifier and label

\- Ordering and grouping

\- Work Package association

\- High-level categories

\- Versioning and status



\### Characteristics



\- Read by `app.py`

\- Stable over time

\- Independent of UI implementation details

\- Does \*\*not\*\* contain tool logic or routing



\### Example



```python
TAB_META = {
    "id": "svc-hvdc-asset-degradation",
    "label": "HVDC Asset Degradation & Remaining Life Estimation",
    "type": "service",
    "order": 220,
    "workpackages": ["WP4", "WP5", "WP6"],
    "categories": [
        "Cable Performance & Optimization",
        "Monitoring & Analytics",
    ],
    "version": "v0.1",
    "status": "active",
}


Tool-Level Metadata (e.g. TAB_MENU_META)
Role

Tool-level metadata defines internal behavior and structure of a tab.
It is owned and consumed by the tab itself, not by the application shell.

Typical Use Cases

Tool menus and sections

Internal navigation or routing

UI behavior specific to the tool

Contextual configuration

Characteristics

Defined inside the tab module

Not visible to app.py

Free to evolve independently

Encapsulates tool-specific knowledge

Example

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "inputs", "label": "Inputs"},
        {"id": "analysis", "label": "Analysis"},
        {"id": "results", "label": "Results"},
    ],
}

Architectural Rule

TAB_META describes how the platform sees the tab.
Tool-level metadata describes how the tab sees itself.

Mixing these responsibilities is explicitly discouraged.

Benefits of This Separation

Clear ownership boundaries

Fully autonomous tabs (plugin-like behavior)

No coupling between tool internals and platform orchestration

Easier evolution of UI and tools over time

Summary

This metadata separation is a design decision, not a technical limitation.
It enables scalable growth of the platform while preserving clarity and control.