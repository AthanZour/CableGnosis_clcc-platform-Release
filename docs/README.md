# System Documentation

This directory represents the **single semantic source of truth**
for the system.

The documentation is organized by **conceptual relevance** rather than
code structure, while still describing the **current implementation**
where it is part of stable system behavior.

There is intentionally **no separation** between "conceptual" and
"developer" documentation.  
All content here contributes to a unified understanding of:
- what the system is
- how it operates today
- how it evolves over time

---

## Directory Overview

### `overview/`
High-level understanding of the system.

Contains:
- purpose and scope
- mental model
- system-wide context

No implementation details.

---

### `meta/`
Canonical definitions and invariants.

Contains:
- terminology
- naming conventions
- stable concepts that define the system language

Changes here affect the entire system.

---

### `system/`
Documentation of the **current operating system**.

Describes how the system is structured and behaves today, including:
- layout organization
- callback responsibilities
- provided services
- shared utilities

This section reflects the active implementation from a semantic perspective,
not as a code reference.

---

### `roadmap/`
Intent and planned evolution.

Contains:
- future directions
- planned extensions
- architectural intentions

Does not describe current behavior.

---

### `deprecated/`
Historical record of removed or retired elements.

Contains:
- what was removed
- why it was removed
- what should not be reintroduced

This section exists to preserve system memory and prevent regression.

---

## Guiding Principle

> If something is hard to locate in this documentation,
> the system itself is not yet clearly defined.


## Conventions


The `conventions/` directory contains **binding rules and development conventions**
that define how code is written, structured, and evolved within this project.


These conventions act as **engineering contracts** and are designed to ensure:


- predictable UI behavior
- prevention of CSS / DOM collisions
- safe reuse of UI templates
- long-term maintainability
- clear boundaries between generic and specific implementations


### What this includes


The `conventions/` directory documents rules such as:


- DOM & CSS contracts (e.g. versioned templates)
- naming conventions (ids, prefixes, suffixes)
- UI pattern versioning rules
- architectural agreements that **must not be broken silently**


### Important
- Files under `conventions/` are **not general guidelines**
- They represent **agreed development contracts**
- Breaking a convention requires a conscious decision and an explicit refactor


For details, see `docs/conventions/README.md`.
(Optional, but strong) Line for conventions/README.md

If you want to reinforce the intent, you can add this at the top of
docs/conventions/README.md:

# Conventions & Engineering Contracts


This directory defines binding development conventions.
Breaking them without an explicit refactor is considered a bug.