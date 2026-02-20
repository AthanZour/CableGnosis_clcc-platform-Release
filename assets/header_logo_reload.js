// ============================================================
// HEADER LOGO CLICK → FULL PAGE RELOAD
// ============================================================

// document.addEventListener("DOMContentLoaded", function () {
//   const logoBtn = document.getElementById("app-header-logo-btn");
//   if (logoBtn) {
//     logoBtn.addEventListener("click", function () {
//       window.location.reload();
//     });
//   }
// });

// ============================================================
// HEADER LOGO CLICK → FULL PAGE RELOAD
// ============================================================
// document.addEventListener("click", function (e) {
//     const btn = e.target.closest("#app-header-logo-btn");
//     if (btn) {
//         window.location.reload();
//     }
// });

document.addEventListener("click", function (e) {
    const btn = e.target.closest("#app-header-logo-btn");
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();
    window.location.reload();
});