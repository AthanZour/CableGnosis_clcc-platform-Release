\# JS-based Overview Tabs — DOM ID Namespacing \& Lifecycle Rules



\## Context



In the CABLEGNOSIS platform, service overview tabs (e.g. WP overviews,

Category overviews) may include JavaScript-driven UI elements

(mouse tracking, drag/zoom, canvas-like interactions, etc.).



Because Dash builds a single global DOM tree at startup,

ALL component ids across ALL discovered tabs must be globally unique,

even if tabs are not visible simultaneously.



This document defines the mandatory rules for JS-based overview tabs.



---



\## Core Rule (Non-negotiable)



Dash component IDs MUST be unique across the entire application.



This applies to:

\- `html.Div(id=...)`

\- `dcc.Input(id=...)`

\- `dcc.Textarea(id=...)`

\- `dcc.Interval(id=...)`

\- any component referenced by JS or callbacks



Duplicate IDs will raise:

`dash.exceptions.DuplicateIdError` at application startup.



---



\## Canonical Identity Model



\- `TAB\_META\["id"]`  

&nbsp; → logical / architectural identifier of the tab  

&nbsp; → used by orchestrator, taxonomy, load order  

&nbsp; → NOT a DOM id



\- Dash component `id=`  

&nbsp; → runtime / DOM identifier  

&nbsp; → MUST be globally unique



\### Correct relationship



DOM ids are DERIVED from `TAB\_META\["id"]`.



---



\## Mandatory Pattern for Overview Services



At the top of each `svc\_\*\_overview.py`:



```python

SERVICE\_ID = TAB\_META\["id"]



def sid(suffix: str) -> str:

&nbsp;   return f"{SERVICE\_ID}-{suffix}"

