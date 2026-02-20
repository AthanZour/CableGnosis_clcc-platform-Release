\# UI / UX Orchestrator – Design Rationale \& Evolution Roadmap



\## 1. Scope \& Intent



The current UI/UX design of the C-LCC platform is \*\*intentionally transitional\*\*.

The choices made at this stage aim to support user understanding of the platform’s

conceptual structure and to create a \*\*semantic bridge\*\* between:



\- project-centric organization (Work Packages)

\- function-centric organization (categories / tools)



Rather than being final design decisions, the current layout acts as an

\*\*interpretability layer\*\* that prepares users for the platform’s future evolution.



---



\## 2. Current Design Rationale (Phase 1)



\### 2.1 Per Work Package View



The “Per Work Package” orchestration mode is a \*\*deliberate choice\*\* at this stage.

It allows users to:



\- understand how tools relate to research Work Packages

\- perceive functional overlaps across WPs

\- gradually shift mental models from project structure to functional capability



This approach enables a \*\*smooth conceptual transition\*\* toward category-based

and function-based navigation.



---



\## 3. Planned UI Structural Evolution (Phase 2+)



\### 3.1 Header Simplification



The top header will be simplified to include:



\- platform logo

\- a thin horizontal strip

\- essential user action icons (login, profile, navigation)



All secondary navigation elements will be removed from the header area.



---



\### 3.2 Orchestrator as Primary Navigation Layer



The current primary bar will be removed as a standalone UI layer.



Instead, the \*\*Tab Orchestrator\*\* will become the single, central navigation mechanism

responsible for:



\- Work Package selection

\- Category-based browsing

\- Tool discovery



Typography and spacing will be slightly compacted to maintain visual clarity.



---



\## 4. Search-Driven Orchestration



\### 4.1 Free-Text Search



The static “Tab Orchestrator” label will be replaced by a search input field:



\- magnifying glass icon to indicate search

\- free-text input (no predefined syntax)

\- dynamic matching against:

&nbsp; - tool names

&nbsp; - categories

&nbsp; - functional keywords



Search results will surface:

\- the relevant tool

\- its associated category

\- all valid navigation paths to reach it



---



\### 4.2 Navigation Modes



Users will be able to explicitly select navigation context:



\- \*\*By Category\*\*

\- \*\*By Work Package\*\*



Additional advanced options may appear contextually and will not be enabled by default.



---



\## 5. Scroll-Aware Navigation Assistance



When users navigate inside large tools with extensive vertical content:



\- a client-side listener will detect deep scroll positions

\- a minimal sub-menu or action button (e.g. “Return to Home”) will appear

\- selecting it will scroll the user back to the orchestration layer



This improves usability without introducing intrusive UI elements.



---



\## 6. Technical Continuity



All existing interaction logic remains valid:



\- GS / JavaScript listeners are preserved

\- preloaded tab architecture is unchanged

\- state management remains backend-mediated



The evolution focuses on \*\*re-orchestration\*\*, not reimplementation.



---



\## 7. Summary



The current UI/UX is a \*\*didactic and transitional layer\*\*.

The planned evolution refines navigation, reduces visual complexity,

and shifts the platform toward a \*\*function-first, search-driven experience\*\*

while preserving architectural stability.

