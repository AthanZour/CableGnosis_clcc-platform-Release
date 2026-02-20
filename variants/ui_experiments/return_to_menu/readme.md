\# Return to Menu – Progressive Navigation Shell



This folder contains \*\*versioned UI/UX implementations\*\* of the

“Return to menu” navigation helper for the C-LCC Demo Platform.



The component is intentionally implemented as a \*\*pure client-side feature\*\*

(JS + CSS only), with:



\- no dependency on Dash callbacks

\- no modifications to `app.py`

\- no interaction with application state

\- no interference with existing JS listeners



Each version represents a \*\*distinct UX pattern\*\*, not a minor visual tweak.



---



\## Folder Structure



```text

return\_to\_menu/

├─ v1\_floating\_shell/

│  ├─ return\_to\_menu\_shell.js

│  ├─ return\_to\_menu\_shell.css

│  └─ return\_to\_menu.svg

│

├─ v2\_drop\_down\_ribbon/

│  ├─ return\_to\_menu\_shell.js

│  ├─ return\_to\_menu\_shell.css

│  └─ return\_to\_menu.svg

│

└─ README.md


---

## Current Stable Variant (v2)

The currently validated implementation is:

**v2_drop_down_ribbon**

This version is considered **UX-stable** and suitable for demo and review
purposes.

### Key Characteristics

- Full-width drop-down ribbon triggered on **scroll-up**
- Implemented as a **pure client-side enhancement**:
  - JavaScript listener
  - CSS positioning
  - SVG-based ribbon shape
- No Dash callbacks
- No dependency on `app.py`
- No modification of application layout or state

### Visual Design

- The ribbon shape is defined by a **closed SVG path**
  - White fill is applied **only inside the shape**
  - No background overlay or viewport masking
- Stroke color and text color are unified (`#12335A`)
- Thin stroke (`stroke-width: 1.5`) for non-intrusive UI presence
- Text label:
  - `RETURN TO MENU`
  - Uppercase
  - System UI font
  - Non-italic
  - Positioned near the top edge for visual alignment with the SVG line

### Interaction Behavior

- Appears on upward scroll
- Auto-hides after **2.2 seconds** of inactivity
- Hides immediately on:
  - scroll down
  - click outside the ribbon
  - click on the ribbon itself
- Clicking the ribbon performs:
  - smooth scroll to top
  - standard hide behavior (component remains available)

### Asset Dependencies

```text
assets/
├─ return_to_menu.svg
├─ return_to_menu_help.png
├─ return_to_menu_shell.js
└─ return_to_menu_shell.css
