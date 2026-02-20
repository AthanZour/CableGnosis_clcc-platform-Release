\# Deprecated UI Orchestrator Context



\## Summary

The contextual text previously rendered in the UI Orchestrator header

has been deprecated and replaced by contextual headers inside each active tab.



\## Status

\- Deprecated: Yes

\- Removed: No

\- Backward compatible: Yes



\## Affected Components

\- app.py

&nbsp; - Output: orchestrator-summary.children

&nbsp; - Layout node: html.Div(id="orchestrator-summary")

\- core.css

&nbsp; - .contextual-info

&nbsp; - .context-strong



\## Reason

The global orchestrator-level context caused unnecessary cognitive load.

Contextual information is now rendered locally inside the active tab,

closer to the actual content it describes.



\## Migration Path

1\. Ensure all contextual information is rendered via `tab-context-header`.

2\. Remove orchestrator-summary output and layout node.

3\. Clean up deprecated CSS selectors in core.css.



\## Planned Removal

TBD (after stabilization of per-category and per-function modes)

