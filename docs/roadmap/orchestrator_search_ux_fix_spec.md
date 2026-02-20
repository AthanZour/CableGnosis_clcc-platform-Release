# Orchestrator Search UX Fix – Spec (Tools & Deep Links)

This document captures the **desired UX behavior** for the orchestrator search bar and dropdown, focusing on **Tools** and **Deep Links** results.

---

## Problem (current behavior)

When a user types a query (e.g., `hvdc`) and selects a Tool result:

1. Tool results appear correctly and navigation/selection happens.
2. Immediately after selection, the **search input is overwritten** (or visually replaced) by the orchestrator status text such as:
   - `Orchestrator | Per Workpackage`
   - `Orchestrator | Per Category`

This is confusing because the user is still in a “search session”.

---

## Target UX (expected behavior)

### Core rule: Search input stays a search input while search is open
While the search dropdown/panel is **open**, the input should behave like a search box:
- it should show the typed query (or be cleared if we choose that mode),
- it should **not** be overwritten by orchestrator “status” text.

### After selecting a Tool / Deep Link
After a user clicks a Tool or Deep Link:
- The selection/navigation happens as today.
- The **search session must not be visually interrupted** by the status text.
- Only when the user explicitly closes the search panel should the status text become visible again.

---

## State model

Introduce an explicit UI state:

- `search_open: bool`  
  True when the user has opened the dropdown/panel and is actively searching.

Optionally:
- `search_query: str` (already the input value)
- `search_mode: "closed" | "open"` (derived from `search_open`)

**Rule:**
- If `search_open == True` → the orchestrator input displays **search query** only.
- If `search_open == False` → the orchestrator input displays **orchestrator status** (e.g. `Orchestrator | Per Workpackage`).

---

## Open/close triggers

### Open
- Search panel opens **only** when clicking the **search icon** (not by clicking the box).
- Typing should keep the panel open and refresh results.

### Close
Search panel closes only when the user explicitly closes it, for example:
- clicking the “close/caret” control,
- pressing ESC (optional),
- clicking outside (optional depending on current UI patterns).

---

## Selection behavior options (choose 1)

### Option A – Clear on select (recommended)
When selecting a Tool/Deep Link while search is open:
- `search_query` is cleared: `""`
- search panel stays open **or** closes (choose one; recommended: stays open if user is in discovery mode, closes if navigation is “final”)

Regardless: **do not show status text until search is closed**.

Pros:
- Keeps input clean, avoids stale queries.
- Feels like “command palette” behavior.

### Option B – Keep query on select
When selecting a Tool/Deep Link:
- keep `search_query` as-is (e.g., `hvdc`)
- panel can remain open
- still **do not show status text** until user closes the panel

Pros:
- Lets user quickly click multiple related results.

---

## Rendering rules for results list

### When search is open and query is non-empty
Show:
- Tools (matching label and optional tags)
- Deep Links (matching label)

Do **not** show:
- the main orchestrator options list (Per Work Package / Per Category / Favorites, etc.)
  - (unless explicitly requested as a separate “Modes” section)

### When search is closed
Show:
- main orchestrator options list (existing behavior)

---

## Navigation / resolver note (future work, not implemented now)

Eventually, tool selection from search should resolve across contexts:
- If a tool is not available in the currently selected Work Package (e.g., WP3),
  search should fall back to other Work Packages / contexts and route to the first valid match.

This will require a generalized resolver that extends the current hyperlink logic.

**Not part of this fix** – included here for completeness.

---

## Implementation sketch (high level)

- Add a `dcc.Store(id="orch-search-state", data={"open": False})`
- Search icon click sets `open=True`
- Close control sets `open=False`
- Input value is used only for query when `open=True`
- A separate computed “status text” is shown only when `open=False`
  - (either as placeholder or as a separate label next to the input)

On Tool/Deep Link click:
- navigate as today
- apply Option A or B for query
- keep `open=True` (until user closes)

---

## Acceptance criteria

- Clicking inside the input box does not open the dropdown.
- Clicking the search icon opens the dropdown.
- While dropdown is open:
  - typing updates results and keeps dropdown open,
  - status text (`Orchestrator | ...`) never replaces the query.
- After selecting a Tool:
  - navigation/selection happens,
  - the query is either cleared (Option A) or preserved (Option B),
  - status text remains hidden until dropdown is explicitly closed by the user.
