# tabs/wp5.py
from dash import html

TAB_META = {
    "id": "wp5",
    "label": "WP5 – Technologies for the operational life and reliability of cable systems",
    "type": "workpackage",
    "order": 11,
    "wp": "WP5",
    "role": "System validation and lifecycle evaluation",
    "scope": "Validation of CABLEGNOSIS technologies and lifecycle performance assessment",
    "status": "active",
    "version": "Proposal baseline"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Work Package 5 – Validation, Deployment & Lifecycle Assessment"),

            html.P(
                "This Work Package focuses on the validation, deployment, "
                "and lifecycle assessment of the CABLEGNOSIS technologies, "
                "ensuring their performance, reliability, and long-term impact."
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
                        "WP5 validates CABLEGNOSIS tools and services through "
                        "realistic use cases and lifecycle performance evaluation.",
                        style={"textAlign": "center", "fontStyle": "italic"}
                    ),
                    html.P(
                        "Current status: validation planning and lifecycle assessment framework.",
                        style={"textAlign": "center", "color": "#777"}
                    )
                ]
            )
        ]
    )