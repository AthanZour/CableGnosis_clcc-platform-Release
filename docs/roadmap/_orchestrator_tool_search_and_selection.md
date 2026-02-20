# Roadmap — Orchestrator Tool Search (Cross-Mode) with Deterministic Placement

This roadmap item extends the **Orchestrator Search** so that an operator can type a tool name (later: keywords),
see matching tools, and **select** one to navigate to it.

The orchestrator remains a **generic shell** (does not know tab internals). It relies on tab metadata
(`TAB_META`) plus a lightweight index built at startup.

---

## Goal

When a user searches for a *specific tool* in the orchestrator:

1) The tool appears in search results and can be selected.
2) On selection, the orchestrator **navigates** to that tool and ensures it is **visible** in the UI:
   - Prefer to place it under the **first declared Work Package** (WP) or **first declared Category**
     (depending on available metadata / chosen policy).
   - If no WP/Category placement is possible, check **Favorites** and navigate there **if the user has favorited it**.
   - Otherwise, fall back to a safe default (no-op or show a small “tool not available in current demo scope” notice).

This keeps navigation deterministic and SCADA-friendly.

---

## Metadata requirements (per tool tab)

Each tool/service tab must expose `TAB_META` fields (safe defaults allowed):

- `id` *(string, required)*
- `label` *(string, required)*
- `workpackages` *(list[str], optional)* — e.g. `["WP4","WP5"]`
- `categories` *(list[str], optional)* — e.g. `["Monitoring & Analytics"]`
- `keywords` *(list[str], optional, future)* — synonyms, abbreviations, domain terms

**Placement policy input**
- If `workpackages` exists → candidate placement = first matching WP in UI
- Else if `categories` exists → candidate placement = first matching Category in UI
- Else → only Favorites can provide a stable navigation home

---

## Search policy

### Matching tiers (current → future)
**Tier 0 (now):**
- exact `id` match
- exact `label` match (case-insensitive)

**Tier 1 (next):**
- prefix/contains on label (case-insensitive)

**Tier 2 (future keywords):**
- match against `TAB_META.keywords` and/or a generated keyword index
- optional scoring (exact > prefix > contains)

### Output
Search returns a list of candidates with:
- tool id
- label
- preferred placement (first WP/Category if available)
- reason/score (optional debug)

---

## Navigation & placement algorithm (deterministic)

Given a selected `tool_id`:

1) **Resolve tool id**
   - `tool_id = resolve(input)` using (id → meta) and (label → id)

2) **Choose placement**
   - If tool has `workpackages`: pick the **first** WP that exists in the UI registry
   - Else if tool has `categories`: pick the **first** Category that exists in the UI registry
   - Else: placement = None

3) **Apply orchestrator transition**
   - If placement is a WP:
     - set `selected-wp-store = <wp_tab_id>`
     - set `selected-tool-store = tool_id`
   - Else if placement is a Category:
     - set `selected-category-store = <cat_tab_id>`
     - set `selected-tool-store = tool_id`
   - Else:
     - check favorites:
       - if `tool_id` is in user favorites → set mode to Favorites and select tool
       - else → no-op or show safe notice

4) **Do not remount tabs**
   - Keep preloaded tab layouts; only switch which is visible.

---

## Favorites (future, but required for fallback rule)

### Data model (per user)
Store a small list/set of tool ids:

- `favorites_store` in `dcc.Store(storage_type="local")` or backend user profile later.
- Version the key, e.g. `c_lcc_favorites_v0_4`.

### Fallback rule
If a tool has no WP/Category placement:
- If it exists in favorites → navigate to Favorites scope and select it.
- Else → show “Not available” message (do not jump unpredictably).

---

## UI behavior (SCADA semantics)

- Search is **assistive**, not destructive:
  - It should not permanently filter toolbars unless explicitly designed as a “filter mode”.
- Selection is explicit:
  - Only clicking a result navigates.
- Deterministic:
  - Same search input → same top result ordering.
- Safe:
  - If a tool cannot be resolved, do nothing.

---

## Acceptance criteria (MVP)

1) Typing in orchestrator search shows matching tools by label.
2) Clicking a result navigates to that tool and makes it visible:
   - under its first declared WP (preferred),
   - else under its first declared Category,
   - else under Favorites if favorited.
3) No crashes if metadata is missing; safe fallbacks apply.
4) Behavior remains stable across sessions.

---

## Stretch goals (post-M18)

- Keyword index + scoring
- “Copy link to tool” (deep link) as a header action (optional)
- User workspace: save/restore last state + favorites + pinned tools
- Operator audit trail: last N visited tools (local)

---

## Implementation notes (high level)

- Build a startup index:
  - `TOOL_ID_TO_META`
  - `TOOL_LABEL_TO_ID`
  - `WP_CODE_TO_WP_TAB_ID`
  - `CATEGORY_LABEL_TO_CAT_TAB_ID`
- Add a search result renderer in the orchestrator panel:
  - show top N tool matches
  - on click: emit `{"type":"tool-link","target": <tool_id>}` (or similar) to reuse existing nav path
- Add favorites store + minimal UI hooks (star/unstar later).

