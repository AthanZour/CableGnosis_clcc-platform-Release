\# Return to Menu – Future Implementations



This document describes \*\*potential future extensions\*\* of the

"Return to Menu" navigation feature.



The current implementation is intentionally minimal and non-intrusive.

Future enhancements are expected to focus on \*\*user configurability\*\*

and \*\*alternative presentation modes\*\*, without altering the core

scroll-based trigger logic.



---



\## 1. Alternative Visual Presentation Modes



The current implementation uses a \*\*full-width drop-down ribbon\*\*

aligned to the top of the viewport.



Future variants may include:



\### 1.1 Centered Square / Floating Panel



\- A square or rectangular container positioned:

&nbsp; - at the center of the screen, or

&nbsp; - slightly offset (e.g. upper-center)

\- Appears on scroll-up or via explicit trigger

\- Suitable for:

&nbsp; - touch-heavy interfaces

&nbsp; - accessibility-focused layouts

&nbsp; - simplified demo modes



\### 1.2 Left-Aligned or Off-Screen Entry



\- The component may be positioned:

&nbsp; - partially off-screen (left or right)

&nbsp; - fully hidden until interaction

\- Intended to reduce visual noise for expert users

\- Could slide in only when strongly triggered



---



\## 2. User-Controlled Visibility Settings



A \*\*Settings\*\* entry may be introduced to allow users to control

how aggressively the feature appears.



\### 2.1 "Show Less / Show More" Control



A simple UI control (e.g. slider or toggle) may be added with semantics:



\- \*\*Show More\*\*

&nbsp; - The component appears after minimal upward scroll

&nbsp; - Suitable for new or exploratory users



\- \*\*Show Less\*\*

&nbsp; - The component requires:

&nbsp;   - a longer upward scroll

&nbsp;   - or multiple consecutive scroll-up events

&nbsp; - Intended for experienced users who prefer fewer interruptions



\### 2.2 Behavioral Interpretation



"Show Less" does \*\*not\*\* hide the feature permanently.



Instead, it modifies internal thresholds such as:

\- required scroll distance

\- scroll velocity

\- number of upward scroll events



Example logic:

\- Default: appear after small upward scroll

\- Show Less: appear only after significant scroll-up activity



---



\## 3. Settings Interaction Model



\### 3.1 Settings Entry Point



\- A small \*\*Settings\*\* button may be introduced:

&nbsp; - within the ribbon

&nbsp; - or in a global UI settings area



\### 3.2 Persistence



User preferences may be persisted via:

\- localStorage

\- session storage

\- or server-side profile settings (future)



The current implementation remains stateless by design.



---



\## 4. Architectural Constraints (Intentional)



Any future implementation must preserve the following principles:



\- No dependency on Dash callbacks

\- No modification of `app.py`

\- Client-side behavior only (JS + CSS)

\- Non-blocking and non-modal interaction

\- Graceful degradation if JavaScript is unavailable



---



\## 5. Versioning Strategy



Each major interaction model should be implemented as a \*\*separate variant\*\*

rather than incremental patches.



Example:



```text

variants/ui\_navigation/return\_to\_menu/

├─ ribbon\_scroll\_v2/        (current)

├─ floating\_panel\_v1/       (future)

├─ side\_entry\_v1/           (future)

└─ return\_to\_menu\_future.md

