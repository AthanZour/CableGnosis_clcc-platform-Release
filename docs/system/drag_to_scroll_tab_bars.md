# Drag-to-Scroll Support for Tab Bars

## Context

The platform uses custom horizontal tab bars (Work Packages, Categories, Tools)
with native scrollbars intentionally hidden for UI/UX clarity.

To preserve usability, drag-to-scroll behavior is implemented via JavaScript.

---

## Implemented Behavior

A global, container-based drag-to-scroll mechanism is enabled for:

- `.wp-tab-bar`
- `.tool-tab-bar`

This allows horizontal scrolling using pointer drag
(mouse / touch / pen), without relying on native scrollbars.

---

## Design Principles

- No hardcoded element IDs
- Container-based event delegation
- No dependency on Dash callbacks
- No interference with tab discovery or preloaded layouts
- Click events are preserved unless an actual drag occurs

---

## Technical Notes

Key characteristics of the implementation:

- Uses `pointerdown / pointermove / pointerup`
- Applies a drag threshold to distinguish click vs drag
- Prevents text selection during drag
- Cancels click events **only** when a drag action was detected
- Compatible with preloaded and dynamically shown tabs

---

## Safety & Compatibility

This mechanism is safe to use alongside:

- Meta-driven tab discovery
- Preloaded tab layouts
- Clientside JS services (overview tabs)
- Dynamic tab visibility switching

No DOM mutations or Dash state interactions occur.

---

## Rationale

Removing native scrollbars improves visual clarity.
Drag-to-scroll ensures usability without compromising
architecture or interaction correctness.

This pattern is considered mandatory for SCADA-style
horizontal navigation bars used in the platform.