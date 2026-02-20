\# Dash Bug Postmortem  

\## Pattern-Matching Callbacks \& Ghost State Reset



\### Context

In a Dash application, a hidden orchestrator control manages the UI mode

(e.g. `per\_wp`, `per\_category`) using a SCADA-style panel.



The visible UI renders orchestration options dynamically based on search input.

Each option is a dynamically created `html.Div` with a pattern-matching `id`.



The orchestration mode is stored in a `dcc.Store` (`tab-view-mode-store`)

and mirrored to a hidden dropdown for backward compatibility.



---



\## Symptom



After selecting \*\*Per Category\*\*, the application \*randomly reverted\*

back to \*\*Per Work Package\*\*:



\- No user click on the option

\- No callback explicitly setting `per\_wp`

\- No page reload

\- No dropdown default value



Logs showed sequences like:



soo

\[None, None, None, None]



uos

per\_wp





Meaning:

\- The selection callback fired

\- No option had been clicked

\- Yet the mode reset to the first option (`per\_wp`)



---



\## Root Cause



The orchestrator options were rendered dynamically:



```python

html.Div(

&nbsp;   label,

&nbsp;   id={"type": "orch-option", "value": value, "scope": "..."},

)

The selection callback used:



Input({"type": "orch-option", "value": ALL, "scope": ALL}, "n\_clicks")

What actually happened

Every re-render of the options panel (search change, panel open/close)

recreated the option components



Newly created components reset n\_clicks → None



Dash treated this as an Input change



The callback fired without a real click



ctx.triggered\_id resolved to the first option



The store was overwritten with per\_wp



This is a known Dash pitfall:

n\_clicks is NOT safe for dynamic pattern-matching components.



The Fix

1\. Use n\_clicks\_timestamp instead of n\_clicks

Input(

&nbsp;   {"type": "orch-option", "value": ALL, "scope": ALL},

&nbsp;   "n\_clicks\_timestamp"

)

2\. Ignore re-renders (all timestamps are None)

if not timestamps or all(t is None for t in timestamps):

&nbsp;   raise dash.exceptions.PreventUpdate

3\. Select only the most recent actual click

idx = max(

&nbsp;   range(len(timestamps)),

&nbsp;   key=lambda i: timestamps\[i] or -1

)



trigger = ctx.inputs\_list\[0]\[idx]\["id"]

value = trigger\["value"]

4\. Optional guard (no-op if same value)

if value == current\_mode:

&nbsp;   raise dash.exceptions.PreventUpdate

Final Callback (Canonical)

@app.callback(

&nbsp;   Output("tab-view-mode-store", "data"),

&nbsp;   Input({"type": "orch-option", "value": ALL, "scope": ALL}, "n\_clicks\_timestamp"),

&nbsp;   State("tab-view-mode-store", "data"),

&nbsp;   prevent\_initial\_call=True,

)

def select\_orchestrator\_option(timestamps, current\_mode):



&nbsp;   if not timestamps or all(t is None for t in timestamps):

&nbsp;       raise dash.exceptions.PreventUpdate



&nbsp;   idx = max(

&nbsp;       range(len(timestamps)),

&nbsp;       key=lambda i: timestamps\[i] or -1

&nbsp;   )



&nbsp;   ctx = dash.callback\_context

&nbsp;   trigger = ctx.inputs\_list\[0]\[idx]\["id"]

&nbsp;   value = trigger.get("value")



&nbsp;   if value == current\_mode:

&nbsp;       raise dash.exceptions.PreventUpdate



&nbsp;   return value

Result

Mode changes occur only on explicit user clicks



Panel open/close and search updates do not affect state



No more silent resets to per\_wp



Deterministic, SCADA-safe behavior



Takeaway

Never use n\_clicks on dynamically created pattern-matching components.

Always use n\_clicks\_timestamp with guards.



This bug is subtle, silent, and extremely easy to misdiagnose.





---



Αν θες, μπορώ:

\- να σου το δώσω και σε \*\*PDF-ready Markdown\*\* (με frontmatter)

\- ή να προσθέσω \*\*diagram section\*\* (event → render → trigger)

\- ή να το κάνουμε \*\*generic Dash best-practice note\*\* (χωρίς το project context)



Αλλά αυτό το `.md` είναι \*\*ακριβώς αυτό που έζησες\*\*.

