# Orchestrator Search UI – Root Cause & Fix (Dash 3.4 → 4.x)

## Σκοπός

Το παρόν έγγραφο περιγράφει:
- το **πρόβλημα** που εμφανίστηκε στο custom orchestrator search UI
- την **αιτία** του προβλήματος μετά από upgrade της Dash
- τις **αλλαγές** που εφαρμόστηκαν
- και τη **συμβατότητα** της λύσης με Dash 3.4 και Dash 4.x

Το αρχείο λειτουργεί ως **technical record / post‑mortem**, ώστε να μην χρειαστεί επανα‑debugging στο μέλλον.

---

## Περιγραφή προβλήματος

Μετά την αναβάθμιση της Dash από **3.4 → 4.0**, το orchestrator search εμφάνισε:

- διπλό ή λάθος position του search icon
- λάθος stacking μεταξύ:
  - input (search area)
  - label ("Orchestrator | Per Work Package")
- ανεξήγητο κενό (padding / spacing) αριστερά του search
- focus outline / active border που δεν υπήρχε πριν
- label που **δεν κρυβόταν σωστά** στο focus / typing

Οπτικά, το search έμοιαζε «σπασμένο», παρότι η HTML δομή δεν είχε αλλάξει.

---

## Root Cause (Αιτία)

Η αιτία **ΔΕΝ** ήταν bug στον custom κώδικα.

Ήταν συνδυασμός των εξής:

### 1. Αλλαγή default rendering behavior στη Dash 4.x

- Το `dcc.Input` στη Dash 4.x ακολουθεί πιο αυστηρά HTML5 / browser defaults
- Εμφανίζονται:
  - focus outlines
  - διαφορετικό box‑model
  - διαφορετικό stacking behavior

Στη Dash 3.4 αυτά **υπήρχαν σιωπηρά**, αλλά δεν γίνονταν ορατά.

---

### 2. Λανθασμένο mental model στο layout

Το αρχικό UI βασιζόταν σε implicit assumptions:

- ότι το input μπορεί να λειτουργεί ως background
- ότι label / icon μπορούν να είναι siblings χωρίς σαφές stacking
- ότι fixed‑width parents δεν θα επηρεάζουν το τελικό alignment

Με τη Dash 4.x αυτά τα assumptions έσπασαν.

---

### 3. CSS selector που δεν έπιανε

Το label δεν κρυβόταν επειδή:

- το `label` **δεν ήταν sibling μετά το input**
- άρα selectors τύπου:

```css
input:focus ~ label
```

δεν ενεργοποιούνταν ποτέ.

---

## Τελικό Μοντέλο (Correct Architecture)

Το UI επανασχεδιάστηκε με **ρητό και ανθεκτικό μοντέλο**:

```
[ orchestrator-input-wrapper ]   (position: relative)
    ├── dcc.Input               (full-size search area)
    ├── icon                    (absolute, inside input)
    └── label                   (absolute, inside input)
```

Βασικές αρχές:

- το **input είναι το μοναδικό interactive layer**
- label και icon είναι **overlay elements εντός του input**
- το wrapper **hugάρει** το input (`width: fit-content`)
- όλα τα browser / Dash defaults γίνονται explicit reset

---

## Τι Αλλάχθηκε (Summary)

### Layout
- αφαιρέθηκαν fixed widths από parents
- το search container shrink‑wraps το input
- εξαφανίστηκαν ανεξήγητα κενά (left spacing)

### Input
- ρητό height / width
- ουδέτερο γκρι border
- explicit `outline: none`
- reset όλων των browser injected UI

### Label
- positioned **inside** the search area
- κρύβεται με `:focus-within` (όχι fragile sibling selectors)
- γίνεται `opacity: 0` (όχι display:none → no layout jump)

### Icon
- single source of truth
- positioned absolute μέσα στο input
- όχι background του input

---

## Συμβατότητα με Dash

### Dash 3.4

✅ Πλήρως συμβατό
- οι CSS κανόνες είναι standard
- `:focus-within` υποστηρίζεται
- δεν εξαρτάται από Dash internals

### Dash 4.x

✅ Πλήρως συμβατό
- neutralizes τα νέα defaults
- δεν σπάει σε future minor releases

### Μελλοντικά upgrades

Το UI:
- δεν βασίζεται σε undocumented behavior
- δεν χρησιμοποιεί Dash‑specific hacks
- δεν εξαρτάται από internal DOM structure

➡️ **θεωρείται safe για future Dash versions**.

---

## Γιατί αυτή η λύση είναι "σωστή"

- είναι deterministic
- είναι CSS‑only
- είναι ανεξάρτητη από Dash version
- λειτουργεί όπως mature UI frameworks (Slack, VS Code, SCADA HMIs)

Δεν είναι workaround.
Είναι **διόρθωση αρχιτεκτονικής υπόθεσης**.

---

## Προτεινόμενο όνομα αρχείου

**`orchestrator_search_fix.md`**  ✅

Εναλλακτικά:
- `dash4_orchestrator_search_postmortem.md`
- `orchestrator_search_layout_contract.md`

---

## Σημείωση για το μέλλον

Αν ξαναπειραχτεί το UI:

- ΜΗΝ μετακινηθεί το label έξω από το input
- ΜΗΝ επανέλθουν background‑icons στο input
- ΜΗΝ μπει fixed width σε parent container

Το παρόν αρχείο είναι το **source of truth** για αυτό το component.

