\# SCADA Orchestrator – Search Assist Pattern



\## Overview



This document describes the design, implementation, and rationale

behind the Orchestrator Search Assist pattern used in the SCADA UI.



The pattern replaces a traditional dropdown selector with a unified,

operator-driven control that combines status display, assistive search,

and explicit selection.



The implementation is deterministic, stateless between sessions,

and aligned with SCADA / HMI interaction principles.



---



\## Core Principles



\- Explicit operator actions only

\- No implicit or hidden UI state

\- Deterministic behavior on every interaction

\- Clear separation between:

&nbsp; - Orchestration state

&nbsp; - Temporary assistive input



The search field is not treated as application state.

It exists purely as a transient assistive mechanism.



---



\## Search Assist Semantics



\### What the Search Is

\- A temporary keyword probe

\- A visual aid to surface relevant options

\- A non-persistent helper tool



\### What the Search Is NOT

\- A filter that alters application state

\- A stored query

\- A user preference



Typical usage assumes short keyword probes (2–3 characters),

sufficient for disambiguation without introducing persistence.



---



\## Lifecycle Behavior



The Orchestrator Panel follows a session-based interaction model:



\- Opening the panel starts a new interaction session

\- Closing the panel ends the session



As a result:

\- The search input is cleared on panel open

\- The search input is cleared on panel close



This guarantees that every interaction begins from a known,

neutral state with zero residual context.



---



\## Rendering Strategy



The list of orchestration options is rendered deterministically

on every callback invocation.



Key guarantees:

\- The options container has a single owning callback

\- Each render produces a complete, fresh component tree

\- No DOM elements are reused across different visual scopes



---



\## Duplicate ID Prevention



When search matches and the full option list are displayed

simultaneously, each visual instance is assigned a unique

pattern-matching ID scope.



This prevents:

\- Duplicate component IDs in the DOM

\- React reconciliation artifacts

\- Option duplication after repeated open/close cycles



Selection logic relies exclusively on the option value,

not on the visual scope in which it appears.



---



\## Intentional Design Decisions



The following behaviors are explicitly intentional:



\- The search input does not persist across sessions

\- The panel does not auto-close on typing

\- The panel does not auto-close on selection

\- The panel closes only through explicit operator action



These decisions prioritize operator clarity and trust

over convenience shortcuts.



---



\## Summary



The Orchestrator Search Assist pattern provides:



\- Clear orchestration status visibility

\- Fast, low-cognitive-load option discovery

\- Explicit, deterministic interactions

\- SCADA-grade safety against hidden state



This pattern is suitable for reuse wherever transient

assistive search is required without introducing

persistent UI state.

