# Progressive Navigation Shell with Mini-Bar Control

## Context

The platform operates as a **single-page, preloaded Dash application** with:

- Persistent navigation elements (Work Package bar, secondary service bar)
- Meta-driven tab discovery (WP / Category / Service)
- Multiple active client-side JavaScript listeners
  (e.g. drag-to-scroll, overview interactions)

The application is not page-based; navigation elements do not reset on scroll.
As content grows vertically, keeping the full navigation permanently visible
introduces unnecessary visual noise.

---

## Observed UX Issue

In the current interaction model:

- Navigation bars are relatively short in length
- Their continuous visibility provides limited value during content exploration
- Vertical scrolling naturally shifts user focus away from navigation

As a result, **showing the full menu by default is suboptimal** and
counterproductive to focus-driven interaction.

---

## Design Goal

Introduce a **progressive navigation shell** that:

- Collapses the full navigation by default
- Displays a **minimal, unobtrusive mini-bar** when needed
- Allows explicit user action to return to or expand the full menu
- Preserves all existing navigation containers and logic

This approach prioritizes content focus while keeping navigation
readily accessible.

---

## Proposed Interaction Model

### Default State
- Full navigation (WP bar + secondary bar) is visually hidden
- User interacts directly with page content

### Scroll-Up Awareness
- A thin, discreet mini-bar appears when the user scrolls upward
- The mini-bar provides:
  - *Return to menu / Return to top*
  - (Future) *Expand full navigation*

### Explicit Expansion
- Full navigation reappears only upon deliberate user action
- No automatic re-expansion occurs

---

## Technical Implementation Principles

### 1. Visual Toggle Only (No Structural Changes)

- Navigation elements remain mounted in the DOM
- Visibility is controlled via CSS transforms / display toggles
- No components are destroyed or recreated

This guarantees:
- Stable state
- No Dash re-rendering
- No loss of context

---

### 2. Client-Side Scroll Listener

A dedicated JavaScript listener:

- Observes scroll direction (`window.scrollY`)
- Controls visibility of:
  - the full navigation shell
  - the mini-bar

The listener:
- Is independent of Dash callbacks
- Does not interact with application state
- Does not require reinitialization on mode switches

---

## Coexistence with Existing JavaScript Listeners

The platform already includes active JS listeners, such as:

- Drag-to-scroll handlers for horizontal tab bars
- Pointer and interaction listeners within service components
- Overview-specific clientside logic

The progressive navigation shell is explicitly designed to:

- Avoid re-binding or duplicating listeners
- Avoid periodic reloads or safety re-initializations
- Avoid interference with existing interaction logic

All listeners remain bound to their respective containers and continue to
operate unchanged.

---

## Why Periodic Reloads Are Avoided

Re-initializing navigation behavior on scroll or context changes would:

- Risk duplicate event bindings
- Introduce unpredictable interaction behavior
- Conflict with Dash’s single-page rendering model

Given that:
- Navigation containers persist
- Tabs are preloaded
- UI state is stable

**Periodic reloads provide no additional safety and are intentionally avoided.**

---

## Future Extension (Non-Breaking)

The mini-bar design allows future enhancements without architectural changes:

- Expand / collapse full navigation
- Keyboard shortcuts
- Context indicators (active WP / Category)

All extensions remain within the visual layer.

---

## Summary

The progressive navigation shell:

- Reduces visual noise by default
- Preserves immediate access to navigation
- Respects existing JavaScript listeners
- Requires no changes to core architecture
- Aligns with control-center and engineering UI principles

This is a deliberate UX refinement built on top of a stable, meta-driven platform.