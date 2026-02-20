from flask import Flask

def create_backend_app():
    app = Flask(__name__)

    try:
        from backend.api.services.monitoring.routes import monitoring_api
        app.register_blueprint(monitoring_api)
        print("✓ Monitoring API registered")
    except Exception as e:
        print("⚠ Monitoring API not loaded:", e)

    return app