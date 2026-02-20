# Fix: Dash `DuplicateIdError` από `tool-link` hyperlinks σε πολλά overview tabs

## Συμπτώματα
Εμφανίζεται error τύπου:

- `dash.exceptions.DuplicateIdError: Duplicate component id found in the initial layout: {"target":"...","type":"tool-link"}`

Αυτό συμβαίνει όταν **διαφορετικά overview tabs** δημιουργούν links με **ακριβώς το ίδιο dict-id** (π.χ. `{"type":"tool-link","target":"svc-hvdc-data-timeline"}`) και το `app.py` φορτώνει/κρατάει πολλά tabs στο αρχικό layout.

---

## Root cause
Τα hyperlinks προς εργαλεία/ tabs ορίζονται με dict ids:

```python
id={"type": "tool-link", "target": "<tool-id>"}
```

Αν **2+ components** στο αρχικό layout έχουν ίδιο dict id, το Dash το θεωρεί duplicate και “σκάει”.

---

## Λύση: κάνε τα `tool-link` ids μοναδικά με `src` + `uid`

### 1) Αλλαγή στα overview modules
Σε **κάθε** `html.A(...)` (ή άλλο clickable component) που είναι tool-link, άλλαξε από:

```python
id={"type": "tool-link", "target": target_xyz}
```

σε:

```python
id={"type": "tool-link", "target": target_xyz, "src": SERVICE_ID, "uid": sid("link-<something>")}
```

- `src`: το service/page που το δημιούργησε (π.χ. `SERVICE_ID`)
- `uid`: μοναδικό per-link (χρησιμοποίησε `sid(...)` για να είναι unique/consistent)

**Παράδειγμα**
```python
html.A(
    "Open tool →",
    href="#",
    id={"type": "tool-link", "target": target_wp4_dt, "src": SERVICE_ID, "uid": sid("link-wp4-dt")},
)
```

> Tip: Αν έχεις μόνο 1 link ανά target ανά σελίδα, αρκεί και `uid` σαν απλό string.
> Αν όμως υπάρχει πιθανότητα να βάλεις 2 links προς το ίδιο target στο ίδιο tab, κράτα `sid(...)`.

---

### 2) Αλλαγή στο `app.py` (pattern matching)
Αφού πλέον τα ids έχουν **επιπλέον keys**, τα callbacks πρέπει να “ταιριάζουν” το ίδιο σχήμα.

Αν πριν είχες:

```python
Input({"type": "tool-link", "target": ALL}, "n_clicks")
Input({"type": "tool-link", "target": ALL}, "n_clicks_timestamp")
```

κάνε τα:

```python
Input({"type": "tool-link", "target": ALL, "src": ALL, "uid": ALL}, "n_clicks")
Input({"type": "tool-link", "target": ALL, "src": ALL, "uid": ALL}, "n_clicks_timestamp")
```

Η λογική μέσα στο callback **δεν χρειάζεται αλλαγή**, αρκεί να συνεχίζει να διαβάζει:

```python
target = tid.get("target")
```

---

### 3) Προσοχή: tool-links που δημιουργούνται δυναμικά (π.χ. orchestrator / search results)
Όπου αλλού δημιουργείς `tool-link` ids (π.χ. “tool hits” από search), πρέπει επίσης να έχουν `src/uid`.

Από:
```python
id={"type": "tool-link", "target": hit["tool_id"]}
```

Σε:
```python
id={"type": "tool-link", "target": hit["tool_id"], "src": "orchestrator", "uid": f"orch-{hit['tool_id']}"}
```

---

## Checklist
- [ ] Όλα τα overview/category overview modules: **όλα** τα `tool-link` ids έχουν `src` + `uid`
- [ ] `app.py` callbacks: pattern ids περιλαμβάνουν `src: ALL` και `uid: ALL`
- [ ] Dynamically-generated tool-links (orchestrator/search): έχουν επίσης `src` + `uid`
- [ ] Τρέχει χωρίς `DuplicateIdError`

---

## Γρήγορο smoke test
1. Άνοιξε το app (initial load).
2. Πλοηγήσου σε 2+ overview tabs που δείχνουν στο ίδιο tool.
3. Κάνε click στα “Open tool →” links.
4. Επιβεβαίωσε ότι:
   - δεν υπάρχει `DuplicateIdError`
   - γίνεται σωστό tab/tool navigation
