(function () {
  const STORAGE_KEY = "cablegnosis_tab_widths_v2";

  // ---- CHANGE: global click blocker while resizing tab widths ----
  let RESIZE_ACTIVE = false;

  function clickBlocker(e) {
    if (!RESIZE_ACTIVE) return;
    e.preventDefault();
    e.stopPropagation();
    if (typeof e.stopImmediatePropagation === "function") {
      e.stopImmediatePropagation();
    }
  }

  // Capture-phase: blocks clicks even if underlying elements listen
  document.addEventListener("click", clickBlocker, true);
  document.addEventListener("mousedown", clickBlocker, true);

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

      // knobs (min/max) – clamp happens on release now
      const MIN_W = 120;
      const MAX_W = 520;

      h.addEventListener("pointerdown", (e) => {
        dragging = true;
        RESIZE_ACTIVE = true; // ---- CHANGE: start blocking clicks ----

        startX = e.clientX;
        startW = btn.getBoundingClientRect().width;

        h.setPointerCapture(e.pointerId);
        e.preventDefault();
        e.stopPropagation();
      });

      h.addEventListener("pointermove", (e) => {
        if (!dragging) return;

        const dx = e.clientX - startX;

        // ---- CHANGE: free-drag (no clamp during move) ----
        // Keep a hard floor only so it doesn't go negative/0.
        const newW = Math.max(20, Math.round(startW + dx));
        btn.style.width = `${newW}px`;

        e.preventDefault();
        e.stopPropagation();
      });

      h.addEventListener("pointerup", (e) => {
        if (!dragging) return;
        dragging = false;

        // ---- CHANGE: clamp on release ----
        const rawW = Math.round(btn.getBoundingClientRect().width);
        const finalW = Math.max(MIN_W, Math.min(MAX_W, rawW));
        btn.style.width = `${finalW}px`;

        const key2 = getBtnKey(btn, barType);
        const st = loadState();
        st[key2] = finalW;
        saveState(st);

        RESIZE_ACTIVE = false; // ---- CHANGE: stop blocking clicks ----

        e.preventDefault();
        e.stopPropagation();
      });

      h.addEventListener("pointercancel", () => {
        dragging = false;

        // clamp on cancel too
        const rawW = Math.round(btn.getBoundingClientRect().width);
        const finalW = Math.max(MIN_W, Math.min(MAX_W, rawW));
        btn.style.width = `${finalW}px`;

        const key2 = getBtnKey(btn, barType);
        const st = loadState();
        st[key2] = finalW;
        saveState(st);

        RESIZE_ACTIVE = false;
      });
    });
  }

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