// Close version popover on ESC (close-only, SCADA-safe)
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" || e.key === "Esc") {
    const backdrop = document.getElementById("app-header-version-backdrop");
    // Backdrop is only visible when popover is open
    if (backdrop && backdrop.style.display !== "none") {
      backdrop.click(); // closes via your Dash callback
    }
  }
});