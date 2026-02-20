// overview.js

// ===================== CONFIG =====================
// Change slide every X seconds (set 0 to disable auto-rotate)
const HERO_ROTATE_SECONDS = 3;
// ==================================================

window.dash_clientside = Object.assign(
  {},
  window.dash_clientside,
  {
    overview: {
      init: function () {
        console.log("[WP OVERVIEW] init called");

        const boxes = document.querySelectorAll("[id$='-hero-image_wp_over']");
        console.log("[WP OVERVIEW] boxes found:", boxes.length);

        const intervalMs = Math.max(0, Number(HERO_ROTATE_SECONDS) || 0) * 1000;

        boxes.forEach((box) => {
          if (box.dataset.bound === "true") return;
          box.dataset.bound = "true";

          const serviceId = box.id.replace("-box", "");
          const cursorOut = document.getElementById(`${serviceId}-cursor`);

          const imagesAttr = box.getAttribute("data-images");
          if (!imagesAttr) {
            console.warn("[WP OVERVIEW] no data-images for", box.id);
            return;
          }

          const images = imagesAttr
            .split("|")
            .map((s) => s.trim())
            .filter(Boolean);

          if (images.length < 2) return;

          let currentImage = 0;

          // ensure initial image
          box.style.backgroundImage = `url("${images[0]}")`;

          // OPTIONAL: stop existing timer if any (defensive)
          if (box.dataset.timerId) {
            try {
              clearInterval(Number(box.dataset.timerId));
            } catch (e) {}
            delete box.dataset.timerId;
          }

          // AUTO-ROTATE
          if (intervalMs > 0) {
            const timerId = setInterval(() => {
              currentImage = (currentImage + 1) % images.length;
              box.style.backgroundImage = `url("${images[currentImage]}")`;
            }, intervalMs);

            // store timer id so we don't create duplicates
            box.dataset.timerId = String(timerId);
          }

          // keep your existing handlers
          box.addEventListener("mousemove", (e) => {
            if (!cursorOut) return;
            // intentionally disabled
          });

          box.addEventListener("mousedown", (e) => {
            if (e.button !== 0) return;
            currentImage = (currentImage + 1) % images.length;
            box.style.backgroundImage = `url("${images[currentImage]}")`;
          });

          box.addEventListener("contextmenu", (e) => e.preventDefault());
        });

        return "";
      },
    },
  }
);