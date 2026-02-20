(() => {
  /*
    Vertical + / - popover for TAB BUTTON WIDTH.
    CHANGE: show ONLY when hovering the actual resize handle (.resize-handle),
            not when hovering the whole tab button.

    - Appears at cursor after 0.5s hover on .resize-handle
    - Disappears after 0.5s on leave (NO hysteresis)
    - Vertical layout (+ above, - below)
    - Uses SAME storage key & keying logic as tab_resize.js
  */

  const STORAGE_KEY = "cablegnosis_tab_widths_v2";
  const SHOW_DELAY_MS = 500;
  const HIDE_DELAY_MS = 500;

  const MIN_W = 120;
  const MAX_W = 520;
  const STEP_PX = 16;

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }
  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  // Same keying logic as tab_resize.js
  function getBtnKey(btn, barType) {
    const id = btn.getAttribute("data-tab-id") || btn.id;
    if (id) return `${barType}:${id}`;
    const txt = (btn.textContent || "").trim().slice(0, 80);
    return `${barType}:text:${txt}`;
  }

  function getBarType(btn) {
    if (btn.closest(".wp-tab-bar")) return "wp";
    if (btn.closest(".tool-tab-bar")) return "tool";
    return "unknown";
  }

  // singleton popover
  let pop = null;
  let showT = null;
  let hideT = null;
  let currentBtn = null;
  let lastMouse = { x: 0, y: 0 };

  window.addEventListener("mousemove", (e) => {
    lastMouse = { x: e.clientX, y: e.clientY };
  }, { passive: true });

  function ensurePopover() {
    if (pop) return pop;

    pop = document.createElement("div");
    pop.className = "tabwidth-popover";
    pop.innerHTML = `
      <button class="plus"  type="button" aria-label="Increase width">+</button>
      <button class="minus" type="button" aria-label="Decrease width">−</button>
    `;
    document.body.appendChild(pop);

    // Keep open while hovering popover itself
    pop.addEventListener("mouseenter", () => {
      clearTimeout(hideT);
      clearTimeout(showT);
      pop.classList.add("visible");
    });

    pop.addEventListener("mouseleave", () => {
      scheduleHide();
    });

    pop.querySelector(".plus").onclick = (e) => {
      e.preventDefault(); e.stopPropagation();
      if (!currentBtn) return;
      adjustWidth(currentBtn, +STEP_PX);
    };

    pop.querySelector(".minus").onclick = (e) => {
      e.preventDefault(); e.stopPropagation();
      if (!currentBtn) return;
      adjustWidth(currentBtn, -STEP_PX);
    };

    return pop;
  }

  function positionPopoverAtCursor() {
    const p = ensurePopover();
    const offset = 10;
    p.style.left = `${lastMouse.x + offset}px`;
    p.style.top = `${lastMouse.y + offset}px`;
  }

  function updateDisabled(btn) {
    const p = ensurePopover();
    const w = Math.round(btn.getBoundingClientRect().width);
    p.querySelector(".minus").classList.toggle("disabled", w <= MIN_W + 1);
    p.querySelector(".plus").classList.toggle("disabled", w >= MAX_W - 1);
  }

  function adjustWidth(btn, delta) {
    const barType = getBarType(btn);
    const key = getBtnKey(btn, barType);

    const currentW = Math.round(btn.getBoundingClientRect().width);
    const nextW = clamp(currentW + delta, MIN_W, MAX_W);

    btn.style.width = `${nextW}px`;

    const st = loadState();
    st[key] = nextW;
    saveState(st);

    updateDisabled(btn);
  }

  function scheduleShow(btn) {
    clearTimeout(hideT);
    clearTimeout(showT);

    showT = setTimeout(() => {
      currentBtn = btn;
      positionPopoverAtCursor();
      ensurePopover().classList.add("visible");
      updateDisabled(btn);
    }, SHOW_DELAY_MS);
  }

  function scheduleHide() {
    clearTimeout(showT);
    clearTimeout(hideT);

    hideT = setTimeout(() => {
      if (!pop) return;
      pop.classList.remove("visible");
      currentBtn = null;
    }, HIDE_DELAY_MS);
  }

  function boot() {
    ensurePopover();

    // ------------------------------------------------------------
    // CHANGE: delegate ONLY from .resize-handle hover
    // ------------------------------------------------------------
    document.addEventListener("mouseover", (e) => {
      const handle = e.target.closest(".resize-handle");
      if (!handle) return;

      const btn = handle.closest(".wp-tab-bar .tab-btn, .tool-tab-bar .tab-btn");
      if (!btn) return;

      scheduleShow(btn);
    });

    document.addEventListener("mouseout", (e) => {
      const handle = e.target.closest(".resize-handle");
      if (!handle) return;

      // If moving into popover, keep open
      if (pop && pop.contains(e.relatedTarget)) return;

      scheduleHide();
    });
  }

  window.addEventListener("load", boot);
})();