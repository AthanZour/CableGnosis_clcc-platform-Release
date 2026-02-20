from flask import Blueprint, jsonify
import pandas as pd
from utils.paths import MONITORING_DIR  # <-- αυτό πρέπει να δείχνει στο data/generated/monitoring

monitoring_api = Blueprint(
    "monitoring_api",
    __name__,
    url_prefix="/api/services/monitoring"
)

WINDOW_SIZE = 30

@monitoring_api.route("/ping", methods=["GET"])
def ping():
    print("PING HIT")
    return jsonify({"ok": True})

def _read_metric_csv(metric: str):
    path = MONITORING_DIR / f"ucy_{metric}.csv"
    #print("Reading:", path, "exists:", path.exists())

    if not path.exists():
        return [], []

    df = pd.read_csv(path)
    if df.empty or "timestamp" not in df.columns or "value" not in df.columns:
        return [], []

    df = df.tail(WINDOW_SIZE)

    t = df["timestamp"].astype(str).tolist()
    v = df["value"].astype(float).tolist()
    return t, v

@monitoring_api.route("/<metric>", methods=["GET"])
def get_metric(metric):
    #print("\n--- MONITORING API HIT ---")
    #print("metric:", metric)
    #print("MONITORING_DIR:", MONITORING_DIR)

    # κρατάμε allowed metrics για να μην γεμίζει σκουπίδια
    if metric not in ("load", "temp"):
        return jsonify({"error": "Unknown metric"}), 404

    t, v = _read_metric_csv(metric)
    return jsonify({"t": t, "v": v})

def register_monitoring_services(app):
    app.register_blueprint(monitoring_api)