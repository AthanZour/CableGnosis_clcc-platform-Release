(() => {
  // Bars you want to enhance
  const TARGETS = [
    {
      hostSelector: "#wp-bar-container",
      barSelector: ".wp-tab-bar",
      leftIcon: "/assets/arrow_blue_left.png",   // βάλε ό,τι svg θες
      rightIcon: "/assets/arrow_blue_right.png",
      stepRatio: 0.75, // scroll by 75% of visible width
    },
    {
      hostSelector: "#tool-bar-container",
      barSelector: ".tool-tab-bar",
      leftIcon: "/assets/arrow_blue_left.png",
      rightIcon: "/assets/arrow_blue_right.png",
      stepRatio: 0.75,
    },
  ];

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

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
    // Create arrows only once per host
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

    // Set icons (as background images)
    leftBtn.querySelector(".icon").style.backgroundImage = `url("${cfg.leftIcon}")`;
    rightBtn.querySelector(".icon").style.backgroundImage = `url("${cfg.rightIcon}")`;

    // Click handlers (won't interfere with scada_pan.js because buttons are OUTSIDE bar)
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

      // Disabled states at edges
      leftBtn.classList.toggle("disabled", atLeft(bar));
      rightBtn.classList.toggle("disabled", atRight(bar));
    }

    // Refresh on scroll + resize + layout changes
    bar.addEventListener("scroll", refresh, { passive: true });

    const ro = new ResizeObserver(refresh);
    ro.observe(bar);

    // Also refresh now
    refresh();

    return refresh;
  }

  function boot() {
    const refreshers = [];

    for (const cfg of TARGETS) {
      const host = document.querySelector(cfg.hostSelector);
      if (!host) continue;

      const bar = host.querySelector(cfg.barSelector);
      if (!bar) continue;

      refreshers.push(ensureArrows(host, bar, cfg));
    }

    // Dash re-renders DOM: keep it stable via MutationObserver
    const mo = new MutationObserver(() => {
      // Re-init if bars were replaced
      for (const cfg of TARGETS) {
        const host = document.querySelector(cfg.hostSelector);
        if (!host) continue;
        const bar = host.querySelector(cfg.barSelector);
        if (!bar) continue;

        // If arrows exist but bar replaced, ensure listeners exist
        ensureArrows(host, bar, cfg);
      }
    });

    mo.observe(document.body, { childList: true, subtree: true });
  }

  window.addEventListener("load", boot);
})();