\# UI – Planned / Future Features


This document tracks UI features that are intentionally not implemented yet,

but are part of the agreed UX and architectural roadmap.

These features are non-blocking and do not affect core system functionality.



---



\## 1. Tab Context – Expand / Collapse (Show more / Show less)

\### Description

The inline tab context header currently displays a compact summary:

\- Mode (e.g. Per Work Package, Per Category)

\- Selected entity (WP / Category)


A toggle mechanism will be added to:

\- Expand the inline context to show additional explanatory text

\- Collapse it back to a minimal, distraction-free state


\### Requirements

\- Per-tab state (independent per active tab)

\- No dependency on markdown files

\- Safe fallback if no extra content is available

\- No impact on navigation or tool rendering



\### Status

Planned – Not implemented



---



\## 2. Info Icon (?) – Modal with Full Description


\### Description

Clicking the info icon (`?`) in the tab context header will open an internal modal

(panel, not browser alert) displaying extended information.



\### Content Sources

\- Optional Markdown files (if present)

\- Programmatic metadata (tool/service version, scope, associations)



\### Behavior

\- If markdown is missing:

&nbsp; - Show a friendly placeholder message

&nbsp; - Never throw errors

\- Modal must be non-blocking and easily dismissible



\### Status

Planned – Not implemented



---



\## 3. Tab Context Positioning (Right-aligned)


\### Description

The tab context header (inline mode + selected entity + info icon)

will be right-aligned within the tab header area to reduce visual dominance.


\### Notes

\- This is a pure CSS/layout concern

\- No Python or callback changes required


\### Status

Planned – Pending CSS refinement



---



\## 4. White Background for Full Tab Content Area

\### Description

The entire tab content area should be explicitly styled with a white background

to visually separate content from the application shell.



\### Notes

\- To be handled at container level via CSS

\- No impact on individual tab modules



\### Status

Planned – Pending CSS refinement

