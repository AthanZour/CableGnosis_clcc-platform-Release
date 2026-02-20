css\_integration\_notes:

&nbsp; context:

&nbsp;   description: >

&nbsp;     The tab menu CSS involves advanced sticky positioning,

&nbsp;     nested containers, and multiple layout contexts (Dash tabs,

&nbsp;     scrollable panels, monitoring dashboards).

&nbsp;     Some behaviors were non-intuitive and could not be fully

&nbsp;     reasoned about during initial implementation.



&nbsp; known\_working\_state:

&nbsp;   status: stable

&nbsp;   notes:

&nbsp;     - Menu renders correctly across lifecycle, timeline, and monitoring tabs

&nbsp;     - Sticky behavior works in all tested tabs

&nbsp;     - Hide / show logic functions as expected

&nbsp;     - CSS changes applied at template level propagate correctly



&nbsp; open\_css\_questions:

&nbsp;   - id: sticky\_pre\_activation\_offset

&nbsp;     description: >

&nbsp;       There is a visible vertical gap before the menu becomes sticky.

&nbsp;       The exact contributing CSS properties were not fully isolated.

&nbsp;     suspected\_causes:

&nbsp;       - parent container padding or margin

&nbsp;       - scroll container boundary

&nbsp;       - Dash tab wrapper styles

&nbsp;       - implicit containing block created by position/overflow



&nbsp;   - id: inconsistent\_rule\_application

&nbsp;     description: >

&nbsp;       Some CSS rules apply in certain tabs but not in others,

&nbsp;       even when DOM structure and menu meta are identical.

&nbsp;     suspected\_causes:

&nbsp;       - CSS specificity conflicts

&nbsp;       - rule ordering in compiled assets

&nbsp;       - hidden overflow on ancestor containers

&nbsp;       - interaction with Dash-generated wrappers



&nbsp;   - id: show\_button\_position\_constraints

&nbsp;     description: >

&nbsp;       The show menu button sometimes cannot be moved further up

&nbsp;       despite changes to top / transform / margin.

&nbsp;     suspected\_causes:

&nbsp;       - ancestor overflow clipping

&nbsp;       - positioning context created by parent elements

&nbsp;       - scroll container limitations



&nbsp; important\_css\_rules\_to\_review:

&nbsp;   positioning:

&nbsp;     - position: sticky

&nbsp;     - top

&nbsp;     - margin-top (pre-sticky positioning)

&nbsp;     - transform: translateY (visual only)

&nbsp;   container\_constraints:

&nbsp;     - overflow: hidden | auto | scroll

&nbsp;     - position: relative on ancestors

&nbsp;     - height / min-height on tab wrappers

&nbsp;   specificity:

&nbsp;     - id-based selectors (\[id$="-root"])

&nbsp;     - class-based selectors (.tab-tool-menu, .tab-tool-menu-item)

&nbsp;     - duplicate selectors with conflicting declarations

&nbsp;   z\_index:

&nbsp;     - ensure consistent layering between menu and show button

&nbsp;     - avoid relying on implicit stacking contexts



&nbsp; future\_debugging\_strategy:

&nbsp;   - Start from a minimal reproduction (single tab, no monitoring UI)

&nbsp;   - Incrementally reintroduce wrappers and containers

&nbsp;   - Inspect computed styles and containing blocks in DevTools

&nbsp;   - Temporarily remove overflow constraints on ancestors

&nbsp;   - Avoid visual-only fixes (transform) until layout flow is understood



&nbsp; architectural\_notes:

&nbsp;   - The current template architecture is correct

&nbsp;   - CSS issues are orthogonal to the Python integration

&nbsp;   - No architectural rollback is recommended due to CSS complexity

&nbsp;   - Future CSS refactors should be done at template level only



&nbsp; decision\_log:

&nbsp;   - decision: proceed\_with\_template

&nbsp;     reason: >

&nbsp;       Centralized template integration provides long-term stability

&nbsp;       and isolates CSS complexity to a single layer.

&nbsp;     status: locked

