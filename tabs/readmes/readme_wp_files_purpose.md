# Purpose and Role of Work Package (WP) Files

## Context: CABLEGNOSIS Life Cycle Center Platform

The **CABLEGNOSIS Life Cycle Center** is designed as an integrated digital platform that hosts services, tools, and analytics supporting the full life cycle of HVDC cable systems.

Within this platform, **Work Package (WP) files (e.g. `wp1.py`, `wp4.py`) do not represent functional application modules**. Instead, they serve a specific and deliberate architectural and semantic role.

---

## What Lives Where in the Platform

### Functional Layer (Operational)
The **actual operational functionality** of the platform lives in:

- **Services** (e.g. monitoring, diagnostics, lifecycle assessment)
- **Tools** (algorithms, analytics components, dashboards)
- **Analytics & visualizations**

These elements:
- perform computations
- expose user-facing functionality
- evolve independently of project structure

---

### Work Packages (Contextual / Structural Layer)

Work Packages:

- ❌ **are not entry points** for users
- ❌ **are not user workflows**
- ❌ **do not host tools or analytics**

Instead, WP files act as:

> **Documentation and traceability anchors**

They provide **context**, not execution.

---

## Purpose of WP Files (`wp<number>.py`)

Each WP file exists to:

1. **Describe the scope and objectives** of the Work Package as defined in the Grant Agreement and Proposal
2. **Explain the role of the WP** within the overall cable system life cycle
3. **Link platform capabilities to project structure**, answering:
   - *Why does this functionality exist?*
   - *In which WP was it developed or validated?*
4. **Provide traceability** between:
   - project deliverables
   - developed services/tools
   - maturity snapshots (e.g. M18, M30)

WP files therefore act as a **semantic bridge** between:

- the **EU project structure** (WPs, tasks, deliverables)
- and the **platform architecture** (services, tools, analytics)

---

## Relationship Between Work Packages and Tools

The relationship is **many-to-many**, but asymmetric:

- A **tool or service**:
  - belongs functionally to a *Category* or *Function*
  - but is **developed, integrated, or validated** within one or more WPs

- A **Work Package**:
  - does not control filtering or navigation
  - does not define user interaction flows
  - provides **rationale, scope, and maturity context** for the tools

In practical terms, a WP answers:

> "This capability exists because it was developed in the context of WPX, addressing objective Y of the proposal."

---

## What a WP File Should Contain

Each `wp<number>.py` file should focus on **descriptive content**, such as:

- A concise description of the WP objectives
- Its position in the cable system life cycle
- Its contribution to the CABLEGNOSIS platform
- The types of services/tools it enables (high-level, non-operational)
- The current maturity or snapshot status

It should **not** contain:

- business logic
- analytics code
- dashboards
- interactive controls

---

## Why This Design Matters

This separation ensures that:

- the platform remains **technology-driven**, not project-driven
- tools can evolve beyond the lifetime of the project
- project reporting, audits, and reviews can clearly trace outcomes back to WPs
- the UI remains clean, consistent, and scalable

---

## Summary

Work Package files are **structural and semantic elements**, not functional ones.

They exist to provide:

- context
- traceability
- alignment with the Grant Agreement

while all **real functionality lives elsewhere** in the platform.

This is an intentional and foundational architectural choice.