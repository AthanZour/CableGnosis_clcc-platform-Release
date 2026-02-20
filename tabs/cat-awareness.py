from dash import html

TAB_META = {
    "id": "cat-awareness",
    "label": "Cable System Awareness",
    "type": "category",
    "order": 102,
    "category": "Cable System Awareness",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Cable System Awareness"),

            html.P(
                "This category addresses cable system awareness, including "
                "pre-fault detection, alarming functionalities, and "
                "operational preparedness of HVDC cable assets."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/awerness.jpg",
                        style={
                            "width": "70%",
                            "margin": "20px auto",
                            "display": "block"
                        }
                    ),

                    html.P(
                        "Pre-fault detection mechanisms, alarm generation, "
                        "and system awareness tools will be accessible "
                        "through this section.",
                        style={
                            "textAlign": "center",
                            "fontStyle": "italic"
                        }
                    ),

                    html.P(
                        "Status: research-oriented modules planned.",
                        style={
                            "textAlign": "center",
                            "color": "#777"
                        }
                    )
                ]
            )
        ]
    )