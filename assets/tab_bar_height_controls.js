(() => {
  /*
    Hover popover with + / - height controls for bar containers.

    Requirements:
    - Show after 0.5s hovering over bar container area
    - Hide after 0.5s, BUT only if mouse moved >= 50px away from container
      (hysteresis so it doesn't close when you move slightly to click +/-)
    - Clamp to [baseline, 2*baseline]
    - Persist to SAME storage key as vertical resize (v3)
  */

  const STORAGE_KEY = "cablegnosis_bar_heights_v3"; // keep consistent with your vertical resize
  const SHOW_DELAY_MS = 500;
  const HIDE_DELAY_MS = 500;
  const HYSTERESIS_PX = 50;
  const STEP_PX = 14; // change if you want (+/- step)

  const TARGETS = [
    { hostSelector: "#wp-bar-container", key: "wp", label: "Height" },
    { hostSelector: "#tool-bar-container", key: "tool", label: "Height" },
  ];

  let lastMouse = { x: 0, y: 0 };
  window.addEventListener("mousemove", (e) => {
    lastMouse = { x: e.clientX, y: e.clientY };
  }, { passive: true });

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function getBaseline(host) {
    // Reuse baseline stored by your vertical resize script if present
    const existing = host.getAttribute("data-baseline-height");
    if (existing) return parseInt(existing, 10);

    const h = Math.round(host.getBoundingClientRect().height || host.offsetHeight || 0);
    if (h > 0) host.setAttribute("data-baseline-height", String(h));
    return h;
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function rectInflated(rect, px) {
    return {
      left: rect.left - px,
      right: rect.right + px,
      top: rect.top - px,
      bottom: rect.bottom + px
    };
  }

  function pointInRect(p, r) {
    return p.x >= r.left && p.x <= r.right && p.y >= r.top && p.y <= r.bottom;
  }

  function ensurePopover(host, cfg) {
    let pop = host.querySelector(".tabbar-size-popover");
    if (!pop) {
      pop = document.createElement("div");
      pop.className = "tabbar-size-popover";
      pop.innerHTML = `
        <span class="lbl">${cfg.label}</span>
        <button class="minus" type="button" aria-label="Decrease height">−</button>
        <button class="plus" type="button" aria-label="Increase height">+</button>
      `;
      host.appendChild(pop);
    }
    return pop;
  }

  function updateButtonStates(host, pop, minH, maxH) {
    const h = Math.round(host.getBoundingClientRect().height);
    const minus = pop.querySelector("button.minus");
    const plus = pop.querySelector("button.plus");
    minus.classList.toggle("disabled", h <= minH + 1);
    plus.classList.toggle("disabled", h >= maxH - 1);
  }

  function applyHeight(host, key, newH, minH, maxH) {
    const finalH = clamp(Math.round(newH), minH, maxH);
    host.style.height = `${finalH}px`;

    const st = loadState();
    st[key] = finalH;
    saveState(st);
    return finalH;
  }

  function attach(cfg) {
    const host = document.querySelector(cfg.hostSelector);
    if (!host) return;

    const pop = ensurePopover(host, cfg);

    // Establish baseline & bounds
    const baseline = getBaseline(host);
    if (!baseline) return;

    const minH = baseline;
    const maxH = Math.round(baseline * 3);

    // Wire +/- buttons
    const minus = pop.querySelector("button.minus");
    const plus = pop.querySelector("button.plus");

    minus.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const h = Math.round(host.getBoundingClientRect().height);
      applyHeight(host, cfg.key, h - STEP_PX, minH, maxH);
      updateButtonStates(host, pop, minH, maxH);
    };

    plus.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const h = Math.round(host.getBoundingClientRect().height);
      applyHeight(host, cfg.key, h + STEP_PX, minH, maxH);
      updateButtonStates(host, pop, minH, maxH);
    };

    // Show/Hide timers
    let showT = null;
    let hideT = null;

    function showLater() {
      clearTimeout(hideT);
      clearTimeout(showT);
      showT = setTimeout(() => {
        pop.classList.add("visible");
        updateButtonStates(host, pop, minH, maxH);
      }, SHOW_DELAY_MS);
    }

    function hideLaterWithHysteresis() {
      clearTimeout(showT);
      clearTimeout(hideT);

      hideT = setTimeout(() => {
        // Only hide if mouse is far enough (outside inflated rect)
        const r = host.getBoundingClientRect();
        const inflated = rectInflated(r, HYSTERESIS_PX);
        if (!pointInRect(lastMouse, inflated)) {
          pop.classList.remove("visible");
        }
      }, HIDE_DELAY_MS);
    }

    // Enter/leave rules:
    // - hovering the host shows after delay
    // - leaving host tries to hide after delay+distance
    host.addEventListener("mouseenter", showLater);
    host.addEventListener("mouseleave", hideLaterWithHysteresis);

    // If user moves into popover, keep it open
    pop.addEventListener("mouseenter", () => {
      clearTimeout(hideT);
      clearTimeout(showT);
      pop.classList.add("visible");
      updateButtonStates(host, pop, minH, maxH);
    });

    // Leaving popover triggers hide logic too
    pop.addEventListener("mouseleave", hideLaterWithHysteresis);

    // Also update enabled/disabled state while scrolling/resizing
    // (lightweight)
    host.addEventListener("pointerup", () => {
      if (pop.classList.contains("visible")) {
        updateButtonStates(host, pop, minH, maxH);
      }
    }, { passive: true });
  }

  function boot() {
    // initial attach
    TARGETS.forEach(attach);

    // Dash DOM changes -> reattach if containers replaced
    const mo = new MutationObserver(() => {
      TARGETS.forEach(attach);
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }

  window.addEventListener("load", boot);
})();