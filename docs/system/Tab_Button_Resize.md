# Tab Button Resize (Primary & Secondary Orchestration Bars)

## Goal
Enable manual width resizing of tab buttons (`.tab-btn`) inside the **primary** (`.wp-tab-bar`) and **secondary** (`.tool-tab-bar`) orchestration bars, without modifying Dash callbacks or breaking existing functionality.

---

## What Was Added

### 1) CSS Patch
Adds a resize handle and ensures tab buttons can take explicit widths.

**Patch (add to `core.css` or a dedicated patch file):**
```css
/* Make tab buttons resizable by JS (width controlled) */
.wp-tab-bar .tab-btn,
.tool-tab-bar .tab-btn {
  position: relative;
  flex: 0 0 auto;         /* allow explicit width */
}

/* Add a visible resize handle on the right edge */
.tab-btn .resize-handle {
  position: absolute;
  top: 0;
  right: 0;
  width: 10px;
  height: 100%;
  cursor: ew-resize;
  opacity: 0.35;
}

.tab-btn .resize-handle:hover {
  opacity: 0.75;
}

/* Optional: show a subtle grip */
.tab-btn .resize-handle::after {
  content: "";
  position: absolute;
  top: 25%;
  left: 4px;
  width: 2px;
  height: 50%;
  background: #9ca3af;
  border-radius: 2px;
}
```

---

### 2) JavaScript (Dash `assets/`)
Creates the handle for each `.tab-btn`, applies pointer-drag resizing, and persists widths using `localStorage`.

**File:** `assets/tab_resize.js`

```js
(function () {
  const STORAGE_KEY = "cablegnosis_tab_widths_v1";

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }
  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  // Choose a stable key per button
  // BEST: use element.dataset.tabId if exists
  // FALLBACK: use text content (works but less stable)
  function getBtnKey(btn, barType) {
    const id = btn.getAttribute("data-tab-id") || btn.id;
    if (id) return `${barType}:${id}`;
    const txt = (btn.textContent || "").trim().slice(0, 80);
    return `${barType}:text:${txt}`;
  }

  function ensureHandles(containerSelector, barType) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const state = loadState();

    container.querySelectorAll(".tab-btn").forEach((btn) => {
      // Apply saved width if exists
      const key = getBtnKey(btn, barType);
      if (state[key]) {
        btn.style.width = `${state[key]}px`;
      }

      // Inject handle once
      if (btn.querySelector(".resize-handle")) return;
      const h = document.createElement("span");
      h.className = "resize-handle";
      h.title = "Drag to resize";
      btn.appendChild(h);

      // Drag logic
      let startX = 0;
      let startW = 0;
      let dragging = false;

      h.addEventListener("pointerdown", (e) => {
        dragging = true;
        startX = e.clientX;
        startW = btn.getBoundingClientRect().width;

        h.setPointerCapture(e.pointerId);
        e.preventDefault();
        e.stopPropagation();
      });

      h.addEventListener("pointermove", (e) => {
        if (!dragging) return;
        const dx = e.clientX - startX;
        const newW = Math.max(120, Math.min(520, Math.round(startW + dx))); // knobs
        btn.style.width = `${newW}px`;
      });

      h.addEventListener("pointerup", (e) => {
        if (!dragging) return;
        dragging = false;

        const key2 = getBtnKey(btn, barType);
        const w = Math.round(btn.getBoundingClientRect().width);
        const st = loadState();
        st[key2] = w;
        saveState(st);

        e.preventDefault();
        e.stopPropagation();
      });

      h.addEventListener("pointercancel", () => { dragging = false; });
    });
  }

  // Dash re-renders parts of DOM, so we re-ensure handles:
  // 1) on load
  // 2) on mutations (when tabs change)
  function boot() {
    ensureHandles(".wp-tab-bar", "wp");
    ensureHandles(".tool-tab-bar", "tool");

    const obs = new MutationObserver(() => {
      ensureHandles(".wp-tab-bar", "wp");
      ensureHandles(".tool-tab-bar", "tool");
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  window.addEventListener("load", boot);
})();
```

---

## Notes / Guarantees
- **No Dash callbacks were modified.**
- Resize logic is **presentation-only** (tab behavior remains unchanged).
- Width persistence uses **`localStorage`**; removing `localStorage` entries resets widths.
- Works for both bars: `.wp-tab-bar` and `.tool-tab-bar`.

---

## Customization
- Change min/max widths in JS: `Math.max(120, Math.min(520, ...))`
- Improve stability by adding `data-tab-id` attributes to `.tab-btn` elements if desired.
