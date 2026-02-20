(() => {
  /*
    Vertical resize for bar CONTAINERS (not buttons).

    CHANGES (requested):
    1) Allow free-drag (no clamp during drag).
       Clamp ONLY on release (pointerup) -> prevents "break" during extreme drags.
    2) While resizing, block ALL clicks so underlying tabs/buttons can't be triggered.

    Notes:
    - Baseline is stored ONCE (data-baseline-height) so min doesn't drift.
    - Persist final height via localStorage.
  */

  const STORAGE_KEY = "cablegnosis_bar_heights_v3";

  const TARGETS = [
    { hostSelector: "#wp-bar-container", key: "wp" },
    { hostSelector: "#tool-bar-container", key: "tool" }, // αν δε θες secondary, σβήστο
  ];

  // ---- Global click blocker while resizing ----
  let RESIZE_ACTIVE = false;

  function clickBlocker(e) {
    if (!RESIZE_ACTIVE) return;
    // Capture-phase blocker: stops clicks on anything while dragging
    e.preventDefault();
    e.stopPropagation();
    if (typeof e.stopImmediatePropagation === "function") {
      e.stopImmediatePropagation();
    }
  }

  // Install once (capture = true)
  document.addEventListener("click", clickBlocker, true);
  document.addEventListener("mousedown", clickBlocker, true);

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function getBaseline(host) {
    const existing = host.getAttribute("data-baseline-height");
    if (existing) return parseInt(existing, 10);

    const h = Math.round(host.getBoundingClientRect().height || host.offsetHeight || 0);
    if (h > 0) host.setAttribute("data-baseline-height", String(h));
    return h;
  }

  function ensureHandles(host, key) {
    let topH = host.querySelector(".tabbar-v-handle.top");
    let botH = host.querySelector(".tabbar-v-handle.bottom");

    if (!topH) {
      topH = document.createElement("div");
      topH.className = "tabbar-v-handle top";
      topH.title = "Drag to resize height";
      host.appendChild(topH);
    }

    if (!botH) {
      botH = document.createElement("div");
      botH.className = "tabbar-v-handle bottom";
      botH.title = "Drag to resize height";
      host.appendChild(botH);
    }

    const baseline = getBaseline(host);
    if (!baseline) return;

    const minH = baseline;
    const maxH = Math.round(baseline * 3);

    // Apply persisted height if exists (clamped)
    const state = loadState();
    if (state[key]) {
      const clamped = Math.max(minH, Math.min(maxH, state[key]));
      host.style.height = `${clamped}px`;
    } else {
      host.style.height = `${Math.round(host.getBoundingClientRect().height)}px`;
    }

    function attachDrag(handleEl, direction) {
      let dragging = false;
      let startY = 0;
      let startH = 0;

      handleEl.addEventListener("pointerdown", (e) => {
        dragging = true;
        RESIZE_ACTIVE = true;

        startY = e.clientY;
        startH = host.getBoundingClientRect().height;

        handleEl.setPointerCapture(e.pointerId);

        // prevent selection/scroll and avoid interference
        e.preventDefault();
        e.stopPropagation();
      });

      handleEl.addEventListener("pointermove", (e) => {
        if (!dragging) return;

        const dy = e.clientY - startY;
        const delta = direction === "bottom" ? dy : -dy;

        // ---- CHANGE: NO CLAMP during drag ----
        // allow free-drag, but keep a hard floor to avoid negative/zero values
        const newH = Math.max(20, Math.round(startH + delta));
        host.style.height = `${newH}px`;

        e.preventDefault();
        e.stopPropagation();
      });

      handleEl.addEventListener("pointerup", (e) => {
        if (!dragging) return;
        dragging = false;

        // ---- CHANGE: CLAMP on release ----
        const rawH = Math.round(host.getBoundingClientRect().height);
        const finalH = Math.max(minH, Math.min(maxH, rawH));
        host.style.height = `${finalH}px`;

        const st = loadState();
        st[key] = finalH;
        saveState(st);

        // unlock clicks *after* we clamp
        RESIZE_ACTIVE = false;

        e.preventDefault();
        e.stopPropagation();
      });

      handleEl.addEventListener("pointercancel", () => {
        dragging = false;
        // clamp on cancel as well
        const rawH = Math.round(host.getBoundingClientRect().height);
        const finalH = Math.max(minH, Math.min(maxH, rawH));
        host.style.height = `${finalH}px`;

        const st = loadState();
        st[key] = finalH;
        saveState(st);

        RESIZE_ACTIVE = false;
      });
    }

    // bind once (avoid stacking listeners)
    if (!topH.getAttribute("data-bound")) {
      attachDrag(topH, "top");
      topH.setAttribute("data-bound", "1");
    }
    if (!botH.getAttribute("data-bound")) {
      attachDrag(botH, "bottom");
      botH.setAttribute("data-bound", "1");
    }
  }

  function boot() {
    for (const t of TARGETS) {
      const host = document.querySelector(t.hostSelector);
      if (!host) continue;
      ensureHandles(host, t.key);
    }

    const mo = new MutationObserver(() => {
      for (const t of TARGETS) {
        const host = document.querySelector(t.hostSelector);
        if (!host) continue;
        ensureHandles(host, t.key);
      }
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }

  window.addEventListener("load", boot);
})();