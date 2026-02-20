(() => {
  const AUTO_HIDE_MS = 2200;

  if (document.querySelector(".return-to-menu-box")) return;

  let state = "HIDDEN";
  let lastScrollY = window.scrollY;
  let timer = null;

  const box = document.createElement("div");
  box.className = "return-to-menu-box";
  box.innerHTML = `<span class="label">MENU</span>
    <img class="return-icon" src="/assets/return_to_menu_help.png" alt="" />`;
  document.body.appendChild(box);

  function show() {
    if (state !== "HIDDEN") return;
    state = "VISIBLE";
    box.classList.add("visible");
    clearTimeout(timer);
    timer = setTimeout(hide, AUTO_HIDE_MS);
  }

  function hide() {
    if (state !== "VISIBLE") return;
    state = "HIDDEN";
    box.classList.remove("visible");
    clearTimeout(timer);
  }

  window.addEventListener(
    "scroll",
    () => {
      const y = window.scrollY;
      if (y < lastScrollY && state === "HIDDEN") show();
      if (y > lastScrollY && state === "VISIBLE") hide();
      lastScrollY = y;
    },
    { passive: true }
  );

  document.addEventListener("click", (e) => {
    if (state === "VISIBLE" && !box.contains(e.target)) hide();
  });

  box.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    window.scrollTo({ top: 0, behavior: "smooth" });
    hide();
  });
})();