(() => {
  const SELECTOR = ".wp-tab-bar, .tool-tab-bar";
  const DRAG_THRESHOLD_PX = 6;

  let activeContainer = null;
  let startX = 0;
  let startScrollLeft = 0;
  let dragged = false;

  function getContainer(target) {
    return target?.closest ? target.closest(SELECTOR) : null;
  }

  document.addEventListener("pointerdown", (e) => {
    if (e.pointerType === "mouse" && e.button !== 0) return;

    const container = getContainer(e.target);
    if (!container) return;

    activeContainer = container;
    dragged = false;
    startX = e.clientX;
    startScrollLeft = container.scrollLeft;

    // ❗ ΔΕΝ κάνουμε preventDefault εδώ
  });

  document.addEventListener("pointermove", (e) => {
    if (!activeContainer) return;

    const dx = e.clientX - startX;

    if (!dragged && Math.abs(dx) > DRAG_THRESHOLD_PX) {
      dragged = true;
      activeContainer.classList.add("dragging");
    }

    if (dragged) {
      activeContainer.scrollLeft = startScrollLeft - dx;
      e.preventDefault(); // κόβει text selection
    }
  }, { passive: false });

  document.addEventListener("pointerup", () => {
    if (activeContainer) {
      activeContainer.classList.remove("dragging");
    }
    activeContainer = null;
  });

  // 🔑 Ακυρώνουμε click ΜΟΝΟ αν έγινε drag
  document.addEventListener("click", (e) => {
    if (!dragged) return;

    const container = getContainer(e.target);
    if (!container) return;

    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    dragged = false;
  }, true);
})();