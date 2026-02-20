from flask import render_template_string
import plotly.graph_objs as go
import random

def register_partner_routes(server):

    # ---------------- New Device Onboarding ---------------- #
    @server.route("/onboard")
    def onboard_popup():
        return render_template_string("""
        <html>
        <head>
            <title>Onboard New Device</title>
            <style>
                body { font-family: Arial; background: #f9f9f9; padding: 20px; }
                input, select { width: 100%; padding: 6px; margin: 6px 0; }
                button { background: #007bff; color: white; border: none; padding: 8px 14px; cursor: pointer; }
                button:hover { background: #0056b3; }
                h2 { color: #222; }
            </style>
        </head>
        <body>
            <h2>🔌 Device Onboarding</h2>
            <form>
                <label>Device Name:</label>
                <input type='text' placeholder='e.g. UCY Thermal Node'>

                <label>Device Type:</label>
                <select>
                    <option>PMU Sensor</option>
                    <option>Thermal Probe</option>
                    <option>Magnetic Node</option>
                    <option>Environmental Unit</option>
                </select>

                <label>Protocol:</label>
                <select>
                    <option>MQTT</option>
                    <option>REST API</option>
                    <option>OPC UA</option>
                </select>

                <label>Measurement Units:</label>
                <input type='text' placeholder='e.g. °C, kV, μm/m'>

                <br><br>
                <button type='submit'>Add Device</button>
            </form>
            <p style='margin-top:20px;color:#555'><i>This popup simulates the device onboarding process.</i></p>
        </body>
        </html>
        """)

    # ---------------- Plot Data Popup ---------------- #
    @server.route("/plotdata/<device_id>")
    def plotdata_popup(device_id):
        data = [random.uniform(0, 100) for _ in range(20)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data, mode="lines+markers", line=dict(color="#007bff")))
        fig.update_layout(title=f"Simulated Data for {device_id}", height=400, margin=dict(l=30, r=30, t=40, b=30))
        graph_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

        return render_template_string(f"""
        <html>
        <head><title>Plot Data – {device_id}</title></head>
        <body style="font-family:Arial; background:#f9f9f9; padding:20px;">
            <h3>📈 Plot for {device_id}</h3>
            {graph_html}
            <p style='margin-top:20px;color:#666'><i>Simulated random dataset (demo purpose only)</i></p>
        </body>
        </html>
        """)
