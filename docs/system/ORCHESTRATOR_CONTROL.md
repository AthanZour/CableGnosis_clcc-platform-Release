# Orchestrator Control – SCADA Unified Search



## Overview

The Orchestrator Control replaces the traditional dropdown-based

mode selector with a SCADA-grade, unified search control that combines

status display and mode selection.



The change is strictly limited to the presentation layer.

All orchestration logic remains intact and backward-compatible.



---



## Design Rationale



In SCADA / HMI systems:

- Implicit UI behavior is discouraged

- Operators must retain full control

- Configuration state must be explicit and observable



The Orchestrator Control follows these principles by ensuring that:

- Mode changes occur only through explicit user action

- No automatic UI hiding or state transitions occur

- The current orchestration mode is always visible



---



## Architecture



### Single Source of Truth

The orchestration mode is stored exclusively in:

- `dcc.Dropdown(id="tab-view-mode")` (hidden)



All application logic continues to depend on this value.



---



### Unified Search Control

The visible control combines:

- A search input (always available)

- A muted status label: `Orchestrator | <Current Mode>`



When the operator types, the label disappears and the input behaves

as a standard search field.



---



### Inline Selection Panel

- Opens explicitly via operator interaction

- Non-modal, inline, and deterministic

- Displays:

nbsp; - Additive search suggestions

nbsp; - Full list of orchestration modes

- Disabled modes are visible but non-interactive



---



## Intentional Non-Features

The following behaviors are deliberately excluded:

- Automatic panel closing on typing

- Automatic panel closing on programmatic state changes

- Modal dialogs



These decisions align with SCADA operator trust and safety models.



---



## Extensibility

The design supports future enhancements without refactor, including:

- Metadata-driven search

- Favorites

- Keyboard navigation

- Outside-click dismissal (optional)



---



## Summary


The Orchestrator Control provides a safer, clearer, and more

operator-friendly interaction model while preserving all existing

business logic.


## Search Behavior (SCADA Rationale)

The search field in the Orchestrator Control is intentionally
non-persistent and session-scoped.

### Design Intent
The search input functions as a temporary keyword assistant
rather than a persistent filter or query state.

Typical usage assumes short keyword probes (2–3 characters)
to quickly surface relevant orchestration modes.

### Behavior
- The search input is cleared:
  - When the orchestrator panel is opened
  - When the orchestrator panel is closed
- No search text is preserved between panel interactions

### Rationale
In SCADA / HMI systems:
- Hidden or residual UI state is discouraged
- Operators must always understand why a specific view is shown
- Each interaction should be deterministic and self-contained

Persisting search text across panel sessions can introduce
ambiguity and cognitive load. Clearing the input ensures that
each interaction starts from a known, neutral state.

This behavior is intentional and should not be modified unless
a fundamentally different interaction model is required.
