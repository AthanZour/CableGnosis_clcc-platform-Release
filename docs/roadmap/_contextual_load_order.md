# Contextual Load Order – Planned Implementation

## Overview

The C- LCC platform currently relies on a **single, global load order**
defined via `TAB_META["order"]` to determine the visual ordering of tabs
and services.

This mechanism is sufficient for:

- initial platform bootstrapping
- static primary navigation elements (Work Packages, Categories)
- early- stage platform demonstrations

However, as the platform evolves toward **context- aware and function- first
navigation**, a single global order is no longer sufficient to express
advanced orchestration requirements.

--- 

## Design Intent

The goal of this planned enhancement is to introduce a **flexible,
extensible, and backward- compatible load order mechanism** that:

- supports multiple navigation contexts
- enables future user- driven customization
- preserves the stability of existing tabs and services
- avoids coupling UI behavior with tab implementation logic

The solution focuses on **re- orchestration**, not reimplementation.

--- 

## Current Load Order Policy (Phase 1)

## #Reserved Order Ranges

- **Order 1–30**  
  Reserved for **primary bar elements**, including:
  - Work Package tabs
  - Category tabs
  - future primary- level navigation items

- **Order >30**  
  Reserved for **service and tool tabs**

This separation ensures that:

- primary navigation remains stable and predictable
- services can evolve independently
- visual hierarchy is preserved across UI states

--- 

## Identified Limitations

A single global order cannot adequately represent scenarios such as:

- a service belonging to multiple Work Packages (e.g. WP4 and WP5),
  but requiring:
  - early positioning in WP4
  - later positioning in WP5

- the same tool requiring different positions when viewed:
  - per Work Package
  - per Category
  - per Function (future default)

These limitations motivate the introduction of **context- aware ordering**.

--- 

## Planned Solution: Layered Contextual Load Order

The planned solution introduces **multiple metadata layers** that are
resolved at runtime by the Tab Orchestrator.

## Core Principle

**Tab modules define defaults.  
The orchestrator composes the effective load order.**

Tab implementations remain unaware of user preferences or contextual
resolution logic.

--- 

## Layer 1: Default Tab Metadata (Canonical Definition)

Each tab defines its default load order inside `TAB_META`.

This layer represents the **canonical, shipped definition** of a tab and
acts as the fallback mechanism when no contextual or user- level overrides
are applied.

## Supported (Current and Backward- Compatible)

TAB_META = {
    "id": "svc- example",
    "order": 225
}

This definition remains valid and sufficient for all existing deployments,
ensuring full backward compatibility.

## Layer 2: Context- Aware Order (System- Level Metadata)

To support contextual navigation scenarios, the order field can be
extended to express context- dependent positioning, while preserving
the original behavior.

Context- aware ordering is optional and only applied when the relevant
context is active.

## Extended Order Definition (Backward- Compatible)

TAB_META = {
    "id": "svc- example",
    "order": {
        "global": 225,
        "per_wp": {
            "WP4": 10,
            "WP5": 30
        },
        "per_category": {
            "Monitoring & Analytics": 5,
            "Cable System Awareness": 20
        }
    }
}

## Context Resolution Rules

- global acts as a universal fallback

- context- specific keys are evaluated only when the corresponding context is active

- tabs without contextual definitions behave exactly as in Phase 1

Layer 3: User- Level Load Order Overrides (Planned)

## A third metadata layer is introduced to support user- driven customization
and future UI- based reordering capabilities.

User- level load order metadata:

- is external to tab modules

- is stored as data files

- does not modify or overwrite source code

- is optional and safely ignorable

Example: User Load Order Override File
{
  "per_wp": {
    "WP4": {
      "svc- example": 3,
      "svc- secondary": 8
    }
  }
}

This layer enables:

- per- user or per- profile ordering

- experimentation without code changes

- future integration with Tab Orchestrator controls


## Load Order Resolution Priority

The effective load order is resolved deterministically by the Tab
Orchestrator according to the following priority chain:

- User- level metadata overrides

- System- level contextual order

- Default TAB_META order

- Stable fallback order (registration or alphabetical)

This guarantees:

- predictable behavior

- reproducibility across sessions

- zero regression for existing deployments

Architectural Guarantees

The proposed load order mechanism ensures that:

- tab implementation code remains unchanged

- no metadata is written back to tab modules

- user preferences never pollute canonical definitions

- the Tab Orchestrator remains the single orchestration authority

All existing interaction logic and preloaded tab architecture remain
intact.

## Planned Status

- Status: Planned / Design- approved

- Implementation: Not active

- Scope: Orchestration layer only

- Dependencies: Metadata resolution logic, Tab Orchestrator

The feature will be introduced incrementally and may initially be
validated on a limited subset of services.

## Summary

The contextual load order mechanism introduces a layered and future- proof
orchestration model that supports multiple navigation contexts and user
customization while maintaining architectural stability.

By clearly separating default definitions, contextual behavior, and
user preferences, the platform achieves flexibility, backward
compatibility, and long- term scalability.