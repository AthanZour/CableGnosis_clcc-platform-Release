\# JS Initialization for Overview Services (Dash)



\## Context



The platform uses meta-driven, auto-discovered tabs (Work Packages, Categories, Services).

Some services (e.g. overview / explanatory tabs) include custom JavaScript-based

interactive behavior (cursor tracking, click-based image toggling, etc.).



Because all tabs are preloaded and share a single DOM, special care is required

to avoid duplicate DOM IDs and to ensure stable JS behavior across multiple services.



---



\## Problem Addressed



Originally, JavaScript logic was hardcoded to a single service ID

(e.g. `svc-wp4-overview-box`), which caused:



\- JS behavior to work only for one overview service

\- DOM ID collisions when similar layouts were reused

\- Poor scalability when adding new overview services (WP or Category based)



---



\## Implemented Solution



\### 1. Service-Scoped DOM IDs



Each overview service derives its DOM IDs from its own `TAB\_META\["id"]`:



```python

SERVICE\_ID = TAB\_META\["id"]



def sid(suffix: str) -> str:

&nbsp;   return f"{SERVICE\_ID}-{suffix}"

