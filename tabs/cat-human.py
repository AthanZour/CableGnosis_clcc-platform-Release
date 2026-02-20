from dash import html

TAB_META = {
    "id": "cat-human",
    "label": "Human Engagement",
    "type": "category",
    "order": 103,
    "category": "Human Engagement",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Human Engagement"),

            html.P(
                "This category focuses on human-in-the-loop interaction, "
                "including predictive maintenance support, fault location accuracy, "
                "repair activities, and cable ageing assessment."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/human_engagement.jpeg",
                        style={
                            "width": "60%",
                            "margin": "20px auto",
                            "display": "block"
                        }
                    ),

                    html.P(
                        "Alerts, notifications, and decision-support information "
                        "will be presented to operators through human-centric "
                        "interfaces.",
                        style={
                            "textAlign": "center",
                            "fontStyle": "italic"
                        }
                    ),

                    html.P(
                        "Status: conceptual – human engagement workflows to be finalized.",
                        style={
                            "textAlign": "center",
                            "color": "#777"
                        }
                    )
                ]
            )
        ]
    )