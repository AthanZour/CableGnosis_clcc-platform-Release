# utils/paths.py
from pathlib import Path

# ---------------------------------------------------------------------
# Base directories
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
GENERATED_DIR = DATA_DIR / "generated"

# ---------------------------------------------------------------------
# Generated data subfolders (by producer / domain)
# ---------------------------------------------------------------------

SYNTHETIC_DIR = GENERATED_DIR / "synthetic"
UPTIME_DIR = GENERATED_DIR / "uptime"
METADATA_DIR = GENERATED_DIR / "metadata"
MONITORING_DIR = GENERATED_DIR / "monitoring"
TIMELINE_DIR = GENERATED_DIR / "timeline"
PARTNER_DATA_DIR = GENERATED_DIR / "partner"

# ---------------------------------------------------------------------
# Initialization helper
# ---------------------------------------------------------------------

def ensure_dirs() -> None:
    """
    Ensure that all required data directories exist.

    This should be called ONCE at application startup (app.py).
    """
    for p in [
        DATA_DIR,
        RAW_DIR,
        GENERATED_DIR,
        SYNTHETIC_DIR,
        UPTIME_DIR,
        METADATA_DIR,
        MONITORING_DIR,
        TIMELINE_DIR,
        PARTNER_DATA_DIR,
    ]:
        p.mkdir(parents=True, exist_ok=True)
