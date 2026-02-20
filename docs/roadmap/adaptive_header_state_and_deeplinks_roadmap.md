# Roadmap note — Adaptive Header, State Persistence, and (Optional) Deep Links

This note captures UI/UX improvements inspired by a “persistent header that switches context” pattern (e.g., MIT Sloan),
adapted to a SCADA-style Dash application where the **orchestrator** (app.py) controls navigation/state while each tab
owns its own content.

## Context

- `app.py` acts as an **orchestrator**:
  - routes user navigation across Work Packages / views,
  - maintains global context (e.g., selected WP, selected tab, selected asset/PMU),
  - **does not** need to know the internal layout of each tab.

- Each tab/page module exposes **metadata** (e.g., `tab_meta`) describing:
  - how the tab should appear in navigation,
  - what header “mode” it belongs to,
  - what contextual controls are relevant for this view.

This keeps the orchestrator lightweight, reduces coupling, and supports incremental onboarding of new tabs/tools.

---

## A. Adaptive Persistent Header (SCADA-friendly)

### Goal
A **persistent header** that remains visible across the app, but **switches** its title/badges/actions depending on:
- selected Work Package (WP),
- active tab/view,
- global mode (e.g., Per WP vs Per Tool),
- selected context (asset/PMU).

### Design principles
- **Single runtime** (no full-page reloads).
- Header is driven by **metadata** and **global state**, not by tab internals.
- Header always exposes:
  - global navigation anchor(s) (Home/Menu),
  - status/“mode” badge,
  - optional context selectors (asset/PMU) when relevant,
  - optional “utility” actions (Help, Copy link, Reset view).

### Proposed metadata contract
Each tab exposes a `tab_meta` entry (or equivalent) with at least:

```yaml
id: "wp5_demo_overview"
label: "WP5 Demonstration Overview"
group: "WP5"
header:
  title: "WP5 Demonstration & Replicability Overview"
  subtitle: "M18: demonstration framing (indicative)"
  badges:
    - key: "mode"
      value: "Per Work Package"
    - key: "wp"
      value: "WP5"
  actions:
    - id: "reset_view"
      label: "Reset"
      kind: "secondary"
    - id: "open_help"
      label: "Help"
      kind: "secondary"
  context:
    show_asset_selector: true
    show_pmu_selector: true
```

**Notes**
- The orchestrator reads `tab_meta` for the currently active tab and renders header accordingly.
- A separate mapping file may define defaults per WP (e.g., colors/icons/badges), so tabs only override when needed.

### Acceptance criteria (MVP)
- Switching tabs changes:
  - header title/subtitle,
  - mode/WP badge,
  - visibility of context selectors.
- No tab-specific code is required in the orchestrator beyond reading metadata keys.

---

## B. “Resume last state” (SCADA behavior)

### Goal
When a user returns to the platform, they continue from the **last selected WP/tab/context**.

### Recommended approach (Dash)
- Store state in browser storage using `dcc.Store(storage_type="local")`.
- Persist:
  - active WP,
  - active tab id,
  - selected asset/PMU,
  - optional view parameters (time window, filters).

### Critical safeguards
- Provide a visible **Home / Reset** entry point to avoid “stuck in last view”.
- Use **versioned storage keys** to avoid breakage when the app changes.

Example:
- storage key prefix: `c_lcc_state_v0_4`
- on app version bump, migrate or reset gracefully.

### Acceptance criteria (MVP)
- Refresh preserves current view and context.
- New session loads last-used view.
- “Reset view” returns to safe default (WP overview).

---

## C. Deep links (optional; post-demo)

You may choose to avoid deep links in M18. When/if enabled later, keep the single runtime, but add **shareable state**.

### Options
1. **Query parameters** (simple, Dash-friendly):
   - `/?wp=wp5&tab=hvdc_kpis&pmu=1`
2. **Hash routing** (SPA feel without server routing):
   - `/#/wp5/hvdc_kpis?pmu=1`
3. **Path routing** (clean URLs; requires careful Dash setup):
   - `/wp5/hvdc_kpis` (still SPA-like if handled by Dash callbacks)

### Minimal “share link” feature
- Add a header action: **Copy link to this view**.
- Implement as: current base URL + serialized state.

### Acceptance criteria (MVP)
- Opening a link restores the view (WP/tab/context) without errors.
- If a tab is missing/renamed, fallback to WP overview and show a small notice.

---

## D. Recommended Markdown docs to add to the repo

To keep this work structured and easy to track, add the following docs:

1) `adaptive_persistent_header.md`
- Problem statement (context in SCADA-like UI)
- Metadata contract (`tab_meta.header`)
- Header layout components (title/subtitle/badges/actions/context selectors)
- Orchestrator responsibilities
- Acceptance criteria & screenshots checklist

2) `state_persistence_resume_last_view.md`
- What is persisted
- Storage strategy (`dcc.Store(local)`)
- Versioning/migration strategy
- Reset/Home behavior
- Edge cases (schema changes, missing tabs)

3) `deep_links_strategy.md`
- Deep link options (query/hash/path)
- Canonical state model
- Copy-link feature
- Fallback rules
- Security notes (do not encode secrets)

4) `navigation_and_back_forward_behavior.md`
- Desired behavior of browser back/forward
- How Dash callback state maps to navigation events
- Testing checklist

5) `header_modes_and_wp_branding.md`
- Mapping WP -> header accents (icon/color/badge text)
- How to keep branding consistent while remaining neutral/industrial

---

## Suggested placement in roadmap

**M18 → M19**
- Adaptive header MVP (metadata-driven)
- Reset/Home improvements
- State persistence (resume last view), versioned key

**M19 → M30**
- Copy-link action (query-based deep link)
- Back/forward navigation alignment
- Hardening (migration/fallback)

**M30 → M36**
- Optional path-style deep links (if needed)
- Per-user saved “workspaces” (multiple saved states)
- Audit-friendly “view state export” (json dump of current view/context)

---

## Implementation notes (non-binding)

- Keep orchestrator logic generic:
  - `active_tab_id` -> read `tab_meta[active_tab_id]`
  - `tab_meta.header` drives header rendering
- Tabs own their content; orchestrator owns:
  - navigation, global state, header, persistence.
- Avoid coupling: tabs should not call orchestrator functions directly; use events/ids.
