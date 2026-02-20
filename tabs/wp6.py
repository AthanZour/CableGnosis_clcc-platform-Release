# tabs/wp6.py
from dash import html

TAB_META = {
    "id": "wp6",
    "label": "WP6 – Validation, testing and evaluation of results",
    "type": "workpackage",
    "order": 13,
    "wp": "WP6",
    "role": "Demonstration in real use cases",
    "scope": "Demonstration and replication of CABLEGNOSIS solutions in European pilots",
    "status": "active",
    "version": "Proposal baseline"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Work Package 6 – Demonstration & Replicability"),

            html.P(
                "This Work Package addresses the large-scale demonstration "
                "and replication of the CABLEGNOSIS solutions across multiple "
                "European use cases and pilot deployments."
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
                        "WP6 demonstrates the applicability and scalability of "
                        "CABLEGNOSIS technologies in real operational environments.",
                        style={"textAlign": "center", "fontStyle": "italic"}
                    ),
                    html.P(
                        "Current status: demonstration planning and pilot preparation.",
                        style={"textAlign": "center", "color": "#777"}
                    )
                ]
            )
        ]
    )