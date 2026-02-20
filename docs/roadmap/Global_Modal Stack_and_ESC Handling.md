\# Planned Enhancement: Global Modal Stack \& ESC Handling (SCADA Standard)



\## Summary

Introduce a global, stack-based modal management mechanism to ensure consistent and safe handling of modal dialogs across the application. The primary goal is to support \*\*ESC-to-close behavior that always targets the most recently opened modal\*\*, in line with SCADA / industrial UI standards.



This enhancement will replace ad-hoc ESC handlers tied to single components and provide a scalable foundation for future modals (e.g. Preferences, About, Alarm Details).



---



\## Problem Statement

Current ESC handling:

\- Targets a \*\*single, hard-coded modal\*\*

\- Does not scale when multiple modals/popovers are introduced

\- Cannot determine which modal was opened last

\- Risks either:

&nbsp; - Closing nothing

&nbsp; - Closing the wrong modal

&nbsp; - Closing multiple modals simultaneously



This behavior is \*\*not acceptable for SCADA-grade UIs\*\*, where context and operator intent must be preserved.



---



\## Proposed Solution: Global Modal Stack



\### Core Concept

Maintain a \*\*global modal stack\*\* in the browser:

\- Each modal \*\*registers itself when opened\*\*

\- Each modal \*\*unregisters itself when closed\*\*

\- The ESC key \*\*always closes the last (top) modal\*\*



This mirrors established patterns used in industrial HMIs and enterprise control software.



---



\## Behavioral Rules (SCADA-Compliant)



\- ESC closes \*\*only one modal\*\*

\- The modal closed is \*\*always the most recently opened\*\*

\- No cascading or bulk closing

\- Non-modal UI elements (dropdowns, tooltips) are unaffected

\- Behavior is deterministic and predictable



---



\## Technical Outline



\### Global JavaScript Modal Registry

\- A global stack (`window.\_\_modalStack`) stores modal identifiers

\- Utility functions:

&nbsp; - `registerModal(modalId)`

&nbsp; - `unregisterModal(modalId)`



\### ESC Key Handling

\- Global keydown listener

\- On `Escape`:

&nbsp; - If stack is non-empty

&nbsp; - Close the modal at the top of the stack

&nbsp; - Trigger closure via the modal’s backdrop element



---



\## Integration with Dash



\- Each modal/popover:

&nbsp; - Calls `registerModal("<modal-id>")` when opened

&nbsp; - Calls `unregisterModal("<modal-id>")` when closed

\- Closure is still handled by Dash callbacks

\- JS layer is \*\*control-only\*\*, not state-owning



---



\## Benefits



\- Scales cleanly to multiple modals

\- Preserves operator context

\- Eliminates fragile, duplicated ESC logic

\- Aligns with SCADA and industrial UX principles

\- Provides a reusable modal infrastructure



---



\## Planned Use Cases



\- Platform / Version information popover

\- Preferences / Settings dialog

\- About system dialog

\- Alarm details modal

\- Future diagnostic or configuration panels



---



\## Status

\*\*Planned\*\* – to be implemented as a shared utility and reused by all modal-capable components.



---

