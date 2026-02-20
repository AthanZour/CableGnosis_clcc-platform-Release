# tabs/category_monitoring.py
from dash import html

TAB_META = {
    "id": "cat-monitoring",
    "label": "Monitoring & Analytics",
    "type": "category",
    "order": 100,
    "category": "Monitoring & Analytics",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Monitoring & Analytics"),

            html.P(
                "This category covers real-time monitoring, data acquisition, "
                "data analysis, and data visualization services based on "
                "laboratory measurements, sensors, and PMUs across the platform."
            ),

            html.Hr(),

            html.Img(
                src="/assets/hvdc_power_line.jpg",
                style={"width": "70%", "margin": "20px auto", "display": "block"}
            ),

            html.P(
                "Monitoring data, analytics results, and measured quantities "
                "will be visualized and analyzed here to support diagnostic "
                "and assessment functions.",
                style={"textAlign": "center", "fontStyle": "italic"}
            )
        ]
    )