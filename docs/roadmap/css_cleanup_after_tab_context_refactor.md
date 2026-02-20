\# CSS Cleanup Notes – Post Tab Context Refactor



This document records CSS elements that became \*\*deprecated or redundant\*\*

after the migration of contextual information from the \*\*UI Orchestrator\*\*

to \*\*per-tab contextual headers\*\*.



The goal is to allow \*\*safe, incremental CSS cleanup\*\* without breaking

backward compatibility.



---



\## 1. Deprecated: Orchestrator-Level Context Styling



The following CSS selectors were originally used to style the

\*\*global orchestrator summary\*\* (`Mode / Selected`) that appeared

centered in the header.



That UI element is no longer rendered (callback returns `None`),

and context is now handled per-tab.



\### Deprecated selectors (safe to remove later)



```css

.contextual-info {

&nbsp;   flex: 1;

&nbsp;   text-align: center;

&nbsp;   font-size: 14px;

&nbsp;   color: #5a5a5a;

}



.contextual-info {

&nbsp;   color: rgba(255, 255, 255, 0.9);

}



.contextual-info .context-strong {

&nbsp;   font-weight: 600;

&nbsp;   color: #ffffff;

}



.contextual-info {

&nbsp;   color: #0b1f3b;

&nbsp;   font-weight: 600;

}



.contextual-info {

&nbsp;   color: #3f5f82;

&nbsp;   font-size: 14px;

}



.contextual-info .context-strong {

&nbsp;   color: #6b7280;

&nbsp;   font-weight: 600;

}

