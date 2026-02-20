# WP6 Overview – Interactive Image Switcher

This README documents the **WP6 Overview interactive image mechanism** used in the CABLEGNOSIS platform.

## What this does

- Enables **interactive image switching** inside WP6 overview templates.
- Images are **defined in Python layout**, not hardcoded in JavaScript.
- JavaScript auto-binds on:
  - initial load
  - tab switches
  - dynamic DOM re-rendering (Dash)

## How it works (architecture)

### 1. Python (Dash layout)

Each interactive image container declares its images via a `data-images` attribute:

```python
html.Div(
    id=sid("box"),
    className="wp6-hero-image",
    **{
        "data-images": (
            "/assets/Undersea-Cables.jpeg|"
            "/assets/subsea-cables-internet-ai-spooky-pooka-illustration.jpg"
        )
    },
    style={
        "backgroundImage": "url('/assets/Undersea-Cables.jpeg')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "cursor": "pointer",
    },
)
```

- Images are separated with `|`
- No JS image knowledge required
- Fully WP/tab-isolated

---

### 2. JavaScript (`overview.js`)

- Reads images from `data-images`
- Binds **once per element**
- Left-click cycles images
- Safe auto-rebind via `MutationObserver`
- Compatible with Dash clientside callbacks

Key guarantees:
- No global selectors
- No cross-tab collisions
- No hardcoded assets

---

### 3. CSS (critical)

The image must have **explicit size** to render backgrounds:

```css
[id$="-root"] .wp-hero-image {
    width: 860px;
    height: 420px;

    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;

    border-radius: 12px;
    overflow: hidden;
    display: block;
}
```

Without this, images load but remain invisible.

---

## Why this design is safe

- WP-scoped (no global CSS bleed)
- Asset paths stay in Python (EU-review friendly)
- JS is generic and reusable for all WPs
- Ready for:
  - WP replication
  - additional images
  - future animations (fade / auto-rotate)

---

## Notes

- Cursor tracking intentionally disabled
- Right-click disabled on image area
- Designed to work with tab switching and lazy rendering

---

_End of document_
