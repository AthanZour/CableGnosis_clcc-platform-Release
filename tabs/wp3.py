# tabs/wp3.py
from dash import html

TAB_META = {
    "id": "wp3",
    "label": "WP3 – Requirements engineering and validation planning",
    "type": "workpackage",
    "order": 14,
    "wp": "WP3",
    "role": "Superconducting cable assessment and design",
    "scope": "Design, aging studies, and feasibility assessment of superconducting HVDC cables",
    "status": "active",
    "version": "Proposal baseline"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Work Package 3 – Superconducting Cable Design & Feasibility"),

            html.P(
                "This Work Package addresses the design, ageing assessment, "
                "and feasibility analysis of superconducting HVDC cable systems "
                "for long-distance and submarine power transmission."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/hvdc_cable.jpg",
                        style={"width": "60%", "margin": "20px auto", "display": "block"}
                    ),
                    html.P(
                        "WP3 evaluates superconducting cable technologies and "
                        "their applicability within the CABLEGNOSIS framework.",
                        style={"textAlign": "center", "fontStyle": "italic"}
                    ),
                    html.P(
                        "Current status: design studies and feasibility assessment.",
                        style={"textAlign": "center", "color": "#777"}
                    )
                ]
            )
        ]
    )