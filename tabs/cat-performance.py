from dash import html

TAB_META = {
    "id": "cat-performance",
    "label": "Cable Performance & Optimization",
    "type": "category",
    "order": 101,
    "category": "Cable Performance & Optimization",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Cable Performance & Optimization"),

            html.P(
                "This category focuses on cable performance assessment, "
                "optimization techniques, and fault detection using "
                "machine learning and artificial intelligence algorithms "
                "supporting lifecycle optimization."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/fault_detection.jpeg",
                        style={
                            "width": "65%",
                            "margin": "20px auto",
                            "display": "block"
                        }
                    ),

                    html.P(
                        "AI-based analytics, optimization algorithms, "
                        "and fault detection services will be integrated here.",
                        style={
                            "textAlign": "center",
                            "fontStyle": "italic"
                        }
                    ),

                    html.P(
                        "Status: conceptual / under development.",
                        style={
                            "textAlign": "center",
                            "color": "#777"
                        }
                    )
                ]
            )
        ]
    )