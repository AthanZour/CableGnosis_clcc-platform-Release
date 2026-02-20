# User Feedback Form Integration -- Platform Module

## Overview

This document describes the integration of a structured user feedback
form within the CABLEGNOSIS platform.\
The goal of this module is to collect qualitative and quantitative
feedback from platform users (e.g., researchers, operators, engineers)
in order to support iterative platform improvement and usability
refinement.

The feedback mechanism is lightweight, extensible, and compatible with
the existing modular architecture of the platform.

------------------------------------------------------------------------

## Objectives

-   Enable users to submit structured feedback directly from the
    platform UI.
-   Support usability assessment during pilot demonstrations and
    reviews.
-   Collect improvement suggestions for tools, workflows, and
    visualization components.
-   Maintain traceability between feedback entries and platform
    versions.

------------------------------------------------------------------------

## Functional Scope

The feedback form supports:

-   User role selection (e.g., Operator, Researcher, Engineer)
-   Tool or tab selection (e.g., Monitoring, Diagnostics, Lifecycle)
-   Rating (e.g., 1--5 scale for usability and clarity)
-   Open-text comments
-   Optional improvement suggestions
-   Optional issue reporting

------------------------------------------------------------------------

## Non-Functional Considerations

-   Lightweight integration within Dash-based UI.
-   No impact on core tool performance.
-   GDPR-compliant handling (no personal data required unless explicitly
    enabled).
-   Backend-agnostic storage (file-based, database, or API endpoint).
-   Extensible structure for future survey expansions.

------------------------------------------------------------------------

## Architecture Positioning

The feedback form is positioned as a platform-level component, not tied
to a single service tab.\
It may be:

-   Embedded within each tool tab
-   Accessed via a global platform menu
-   Triggered after specific user interactions (e.g., tool execution)

The module is designed to remain independent from analytical logic and
tool computation layers.

------------------------------------------------------------------------

## Data Handling Options

The feedback entries can be stored using one of the following
approaches:

1.  Local JSON storage (for demo/testing environments)
2.  Database persistence (PostgreSQL / SQLite)
3.  External API endpoint
4.  Integration with project SharePoint or reporting repository

The storage mechanism can be configured without modifying the frontend
structure.

------------------------------------------------------------------------

## Suggested Data Schema

``` json
{
  "timestamp": "ISO8601",
  "platform_version": "vX.X",
  "tool": "tool-id",
  "user_role": "operator/researcher/etc",
  "usability_rating": 1-5,
  "comments": "text",
  "improvement_suggestions": "text"
}
```

------------------------------------------------------------------------

## Future Extensions

-   Export of aggregated feedback reports (CSV / PDF)
-   Dashboard for feedback analytics
-   Automated clustering of suggestions using NLP
-   Version-based feedback comparison
-   Integration with project review documentation

------------------------------------------------------------------------

## Conclusion

The feedback form module enhances the platform's maturity and supports
iterative refinement during the project lifecycle.\
It provides a structured mechanism to capture user insights without
altering the analytical integrity of the core services.
