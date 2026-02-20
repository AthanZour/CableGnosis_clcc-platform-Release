\# SCADA UI Compression – Orchestrator \& Bars



\## Scope

This document summarizes the UI compression changes applied to the

Tab Orchestrator, Work Package bar, and Tool bar in order to achieve

SCADA / HMI-style density and eliminate unnecessary vertical gaps.



The changes are \*\*CSS-only\*\* (no JS or callback logic modified).



---



\## Problems Identified



\### 1. Excessive vertical gaps

Visible gaps were observed between:

\- Orchestrator header and Primary (WP) bar

\- Primary (WP) bar and Secondary (Tool) bar



Initial assumption that separators were the cause was disproven.

The root cause was a combination of:

\- Container padding

\- Line-height inheritance

\- Button margins

\- Gradient-based separators with transparent zones



---



\### 2. Inconsistent button heights

Single-line tabs appeared visually shorter than multi-line tabs due to

intrinsic height differences.



---



\### 3. Context pill overlapping separator line

The per-tab context pill overlapped technical separator lines due to

inline margin usage and baseline alignment.



---



\## Implemented Fixes



\### A. Uniform Tab Button Height

\- Enforced `min-height` on WP and Tool tab buttons

\- Used flex alignment to center content vertically

\- Allowed natural text wrapping (1–2 lines)



Result:

\- Consistent visual height across all tabs

\- No JS-based height measurement required



---



\### B. Bar-Level Height Control (Primary \& Secondary)

\- Removed margin-driven gaps from tab buttons

\- Normalized `line-height` at bar level

\- Forced bars to behave as compact control strips



Result:

\- Bars define their height explicitly

\- No hidden vertical “air” from typography



---



\### C. Separator Strategy Revision

\- Gradient-based separators were identified as a major source of

&nbsp; invisible spacing due to transparent zones

\- Replaced critical separators with:

&nbsp; - Minimal fixed height

&nbsp; - Simple 1px solid borders where needed



Result:

\- Visual separation preserved

\- Vertical gaps eliminated



---



\### D. Orchestrator Header Compression

\- Reduced padding on `.tab-header-row`

\- Removed bottom padding accumulation

\- Tightened internal gaps between title, lines, and dropdown



Result:

\- Orchestrator behaves as a control header, not a visual section



---



\### E. Context Pill (Mode / Selected)

\- Identified that the visible pill is rendered per-tab

&nbsp; (`tab-context-container` / `tab-context-inline`)

\- Removed inline margin influence

\- Applied controlled vertical positioning using `transform: translateY()`

\- Reduced padding and font size for SCADA density



Result:

\- Pill no longer overlaps separator lines

\- Compact, status-like appearance



---



\## Design Principles Applied



\- SCADA / HMI density over decorative spacing

\- Prefer `min-height` over dynamic measurement

\- Avoid gradient separators in dense UI zones

\- Eliminate margin-based layout gaps; use controlled geometry

\- Use `transform` for optical alignment without layout shifts



---



\## Outcome



\- Orchestrator, WP bar, and Tool bar now visually stack without gaps

\- UI density significantly increased without loss of clarity

\- All changes are reversible and isolated to CSS



---



\## Next Steps

Further improvements can focus on:

\- Line clamping for long tab labels

\- Responsive density scaling (large screens vs laptops)

\- Optional merging of Orchestrator + Primary bar into a single strip

