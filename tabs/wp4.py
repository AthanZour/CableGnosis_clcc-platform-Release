# tabs/wp4.py
from dash import html

TAB_META = {
    "id": "wp4",
    "label": "WP4 –  Technologies for the development of innovative cable systems",
    "type": "workpackage",
    "order": 12,
    "wp": "WP4",
    "role": "Condition monitoring and diagnostics",
    "scope": "Monitoring, diagnostics, analytics and AI-based tools for cable systems",
    "status": "active",
    "version": "M18 snapshot"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Work Package 4 – Monitoring & Diagnostics"),

            html.P(
                "This Work Package focuses on monitoring, diagnostics, "
                "and analytics for HVDC cable systems."
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
                        "WP4-related tools and services will be integrated here.",
                        style={"textAlign": "center", "fontStyle": "italic"}
                    ),
                    html.P(
                        "Current status: tools under development / integration.",
                        style={"textAlign": "center", "color": "#777"}
                    )
                ]
            )
        ]
    )