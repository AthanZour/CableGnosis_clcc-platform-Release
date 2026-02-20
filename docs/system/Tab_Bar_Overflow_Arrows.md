# Overflow Arrow Navigation (Primary & Secondary Orchestration Bars)

## Goal
When the **primary** (`.wp-tab-bar`) or **secondary** (`.tool-tab-bar`) tab bar overflows horizontally, show **left/right arrow buttons** to scroll the bar.  
Arrows:
- appear **only when overflow exists**
- become **disabled (greyed-out, non-clickable)** at the scroll edges
- do **not** interfere with existing **drag-to-scroll** behavior

---

## What Was Added

### 1) CSS Patch
Adds arrow button styling and reserves padding so arrows don’t cover tabs.

**Patch (add to `core.css` or a dedicated patch file):**
```css
#wp-bar-container,
#tool-bar-container {
  position: relative; /* anchor for absolute arrows */
}

/* Add side padding so arrows don't cover first/last tab */
#wp-bar-container .wp-tab-bar,
#tool-bar-container .tool-tab-bar {
  padding-left: 22px;
  padding-right: 22px;
}

/* Shared arrow button */
.tabbar-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 28px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  border-radius: 6px;
  padding: 0;
  margin: 0;
  z-index: 50;

  display: none; /* JS toggles based on overflow */

  cursor: pointer;
  user-select: none;
}

/* Left / right placement */
.tabbar-arrow.left  { left: 2px; }
.tabbar-arrow.right { right: 2px; }

/* Icon inside (SVG as background) */
.tabbar-arrow .icon {
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 12px 12px;
  opacity: 0.9;
}

/* Disabled state */
.tabbar-arrow.disabled {
  opacity: 0.35;
  cursor: default;
  pointer-events: none;
}

/* Optional hover feedback */
.tabbar-arrow:not(.disabled):hover {
  background: #f2f6fb;
}
```

---

### 2) JavaScript (Dash `assets/`)
Injects arrow buttons into the bar container, detects overflow, updates disabled states, and scrolls on click.

**File:** `assets/tab_bar_arrows.js`

```js
(() => {
  const TARGETS = [
    {
      hostSelector: "#wp-bar-container",
      barSelector: ".wp-tab-bar",
      leftIcon: "/assets/arrow_left.svg",
      rightIcon: "/assets/arrow_right.svg",
      stepRatio: 0.75, // scroll by 75% of visible width
    },
    {
      hostSelector: "#tool-bar-container",
      barSelector: ".tool-tab-bar",
      leftIcon: "/assets/arrow_left.svg",
      rightIcon: "/assets/arrow_right.svg",
      stepRatio: 0.75,
    },
  ];

  function hasOverflow(bar) {
    return bar.scrollWidth > (bar.clientWidth + 2);
  }
  function atLeft(bar) {
    return bar.scrollLeft <= 0;
  }
  function atRight(bar) {
    return (bar.scrollLeft + bar.clientWidth) >= (bar.scrollWidth - 2);
  }

  function ensureArrows(host, bar, cfg) {
    let leftBtn = host.querySelector(".tabbar-arrow.left");
    let rightBtn = host.querySelector(".tabbar-arrow.right");

    if (!leftBtn) {
      leftBtn = document.createElement("button");
      leftBtn.className = "tabbar-arrow left";
      leftBtn.type = "button";
      leftBtn.setAttribute("aria-label", "Scroll left");
      leftBtn.innerHTML = `<div class="icon"></div>`;
      host.appendChild(leftBtn);
    }

    if (!rightBtn) {
      rightBtn = document.createElement("button");
      rightBtn.className = "tabbar-arrow right";
      rightBtn.type = "button";
      rightBtn.setAttribute("aria-label", "Scroll right");
      rightBtn.innerHTML = `<div class="icon"></div>`;
      host.appendChild(rightBtn);
    }

    // Set icons
    leftBtn.querySelector(".icon").style.backgroundImage = `url("${cfg.leftIcon}")`;
    rightBtn.querySelector(".icon").style.backgroundImage = `url("${cfg.rightIcon}")`;

    // Click handlers
    leftBtn.onclick = () => {
      const step = Math.round(bar.clientWidth * cfg.stepRatio);
      bar.scrollBy({ left: -step, behavior: "smooth" });
    };
    rightBtn.onclick = () => {
      const step = Math.round(bar.clientWidth * cfg.stepRatio);
      bar.scrollBy({ left: step, behavior: "smooth" });
    };

    function refresh() {
      if (!hasOverflow(bar)) {
        leftBtn.style.display = "none";
        rightBtn.style.display = "none";
        return;
      }

      leftBtn.style.display = "block";
      rightBtn.style.display = "block";

      leftBtn.classList.toggle("disabled", atLeft(bar));
      rightBtn.classList.toggle("disabled", atRight(bar));
    }

    bar.addEventListener("scroll", refresh, { passive: true });

    const ro = new ResizeObserver(refresh);
    ro.observe(bar);

    refresh();
  }

  function boot() {
    for (const cfg of TARGETS) {
      const host = document.querySelector(cfg.hostSelector);
      if (!host) continue;

      const bar = host.querySelector(cfg.barSelector);
      if (!bar) continue;

      ensureArrows(host, bar, cfg);
    }

    const mo = new MutationObserver(() => {
      for (const cfg of TARGETS) {
        const host = document.querySelector(cfg.hostSelector);
        if (!host) continue;
        const bar = host.querySelector(cfg.barSelector);
        if (!bar) continue;
        ensureArrows(host, bar, cfg);
      }
    });

    mo.observe(document.body, { childList: true, subtree: true });
  }

  window.addEventListener("load", boot);
})();
```

---

## Drag-to-Scroll Safety
- Arrow buttons are inserted into:
  - `#wp-bar-container` and `#tool-bar-container`
- They are **siblings** of the scrollable bars, not children.
- Existing drag-to-scroll (e.g., `scada_pan.js`) continues to operate on `.wp-tab-bar` / `.tool-tab-bar` without interference.

---

## Assets Required
Place your SVG icons in Dash `assets/`:
- `assets/arrow_left.svg`
- `assets/arrow_right.svg`

(Or change `leftIcon/rightIcon` paths in JS.)

---

## Customization
- Scroll step: `stepRatio` (e.g., `0.5` for smaller steps)
- Arrow dimensions: `.tabbar-arrow` width/height in CSS
- Disabled thresholds: adjust the `+2` / `-2` tolerances in JS if needed
