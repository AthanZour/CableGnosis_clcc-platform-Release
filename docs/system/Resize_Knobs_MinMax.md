# UI Resize Knobs (Min/Max Heights & Widths)

This note documents **where** and **how** to change the limits for:

- **Container (bar) height**: `#wp-bar-container`, `#tool-bar-container`
- **Tab button width**: `.wp-tab-bar .tab-btn`, `.tool-tab-bar .tab-btn`

All limits are currently controlled in **JavaScript**, with optional CSS hard-guards.

---

## 1) Container (Bar) Height Limits (Min/Max)

### Files involved
- `assets/tab_bar_vertical_resize.js`  *(drag up/down on the bar handles)*
- `assets/tab_bar_height_controls.js`  *(+ / − popover on the bar)*

### How min/max is computed (current behavior)
Both scripts use the same rule:

- **min height** = the bar's **baseline** height (captured once on first render)
- **max height** = **2 × baseline**

Baseline is stored on the container element as:
- `data-baseline-height="<px>"`

So the allowed range is:

```
minH = baseline
maxH = baseline * 2
```

### Option A (recommended): Change the multiplier (max height)
In **both** JS files, find the line (or equivalent):

```js
const maxH = Math.round(baseline * 2);
```

Change `2` to whatever you want (e.g. 2.5):

```js
const maxH = Math.round(baseline * 2.5);
```

### Option B: Use explicit min/max pixels (override baseline logic)
If you prefer fixed values, replace the range calculation in **both** files with explicit numbers, e.g.:

```js
const minH = 56;   // px
const maxH = 160;  // px
```

> Keep this consistent in both:
> - `tab_bar_vertical_resize.js`
> - `tab_bar_height_controls.js`

### Optional: change the +/- step size
In `assets/tab_bar_height_controls.js`:

```js
const STEP_PX = 14;
```

Increase or decrease to control how much each click changes height.

---

## 2) Tab Button Width Limits (Min/Max)

### Files involved
- `assets/tab_resize.js`  *(drag on the resize-handle at the right edge)*
- `assets/tab_width_controls.js` *(vertical + / − popover at cursor, shown ONLY on `.resize-handle` hover)*

### Where to change min/max width
In **both** files, change these constants:

```js
const MIN_W = 120;
const MAX_W = 520;
```

### Optional: change the +/- step size
In `assets/tab_width_controls.js`:

```js
const STEP_PX = 16;
```

---

## 3) Optional CSS hard-guards (extra safety)

JS is the “source of truth” right now.  
If you want a CSS safety net (so tabs cannot exceed bounds even if JS changes), add to `core_patches.css`:

```css
.wp-tab-bar .tab-btn,
.tool-tab-bar .tab-btn {
  min-width: 120px;
  max-width: 520px;
}
```

If you use CSS guards, make sure they match the JS values to avoid confusing behavior.

---

## 4) Persistence Notes (localStorage)

Widths/heights persist via `localStorage`:

- Tab widths: `cablegnosis_tab_widths_v2`
- Bar heights: `cablegnosis_bar_heights_v3`

If you change min/max limits and want users to “reset” old saved sizes, clear those keys in the browser storage.

---

## Quick Checklist

- Bar max height multiplier: change `baseline * 2` in **both** height JS files
- Bar +/- step: change `STEP_PX` in `tab_bar_height_controls.js`
- Tab min/max width: change `MIN_W / MAX_W` in **both** tab width JS files
- Tab +/- step: change `STEP_PX` in `tab_width_controls.js`
- (Optional) CSS min/max: add `min-width/max-width` rules
