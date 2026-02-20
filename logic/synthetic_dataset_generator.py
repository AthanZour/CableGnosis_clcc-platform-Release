from __future__ import annotations

import json
from datetime import datetime, timedelta
from math import pi
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from utils.paths import SYNTHETIC_DIR

__all__ = ["generate_synthetic_dataset"]


def generate_synthetic_dataset(
    *,
    # ------------------------------------------------------------------
    # Γενικός έλεγχος
    # ------------------------------------------------------------------
    mode: str = "random",  # "random" | "manual"
    # Επιλέγουμε **ένα** από τα δύο παρακάτω
    num_points: Optional[int] = None,  # π.χ. 8760   (αν None => derives)
    frequency_per_day: int = 24,
    duration_days: int = 365,
    # ------------------------------------------------------------------
    # Παράμετροι ημιτόνων
    # ------------------------------------------------------------------
    num_sinusoids: int = 10,
    max_amplitude: float = 60.0,
    max_dc_offset: float = 20.0,
    # Manual mode arrays (length == num_sinusoids)
    manual_amplitudes: Optional[List[float]] = None,
    manual_phases: Optional[List[float]] = None,
    manual_offsets: Optional[List[float]] = None,
    # ------------------------------------------------------------------
    # Συστατικό υψηλής συχνότητας (τυχαίος θόρυβος)
    # ------------------------------------------------------------------
    noise_min: float = -5.0,
    noise_max: float = 40.0,
    # ------------------------------------------------------------------
    # Clipping & έξοδος
    # ------------------------------------------------------------------
    clip_min: float = -120.0,
    clip_max: float = 200.0,
    save_path: Optional[Path] = SYNTHETIC_DIR,
    default_filename: str = "cablegnosis_synthetic_dataset.json",
) -> pd.DataFrame:
    """Generate & save a synthetic multisinusoidal dataset.

    Επιστρέφει ως `pandas.DataFrame` και ταυτόχρονα το αποθηκεύει σε JSON.
    Όλα τα ορίσματα έχουν ίδια default με τον αρχικό script.
    """

    # ------------------------------------------------------------------
    # 1. Ρύθμιση διαδρομής εξόδου
    # ------------------------------------------------------------------
    if save_path is None:
        save_path = Path.cwd() / default_filename
    else:
        save_path = Path(save_path)
    
        # ✅ If user passed a directory (e.g. SYNTHETIC_DIR), append filename
        if save_path.exists() and save_path.is_dir():
            save_path = save_path / default_filename
    
        # ✅ Also handle the case where path doesn't exist yet but looks like a dir
        # (common when you pass SYNTHETIC_DIR and it will be created)
        if save_path.suffix == "":
            save_path = save_path / default_filename
    
    # make sure parent dir exists
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 2. Εσωτερικές βοηθητικές συναρτήσεις (ίδια λογική με το παλιό)
    # ------------------------------------------------------------------
    def build_time_index() -> List[datetime]:
        if num_points is not None:
            dt_seconds = (duration_days * 24 * 3600) / num_points
            total_points = num_points
        else:
            total_points = frequency_per_day * duration_days
            dt_seconds = (24 * 3600) / frequency_per_day
        start_time = datetime(2025, 1, 1)
        return [start_time + timedelta(seconds=i * dt_seconds) for i in range(total_points)]

    def generate_components(num_pts: int, omega_base: float) -> np.ndarray:
        if mode == "random":
            amps = np.random.uniform(0, max_amplitude, num_sinusoids)
            phases = np.random.uniform(0, 2 * pi, num_sinusoids)
            dc_offs = np.random.uniform(-max_dc_offset, max_dc_offset, num_sinusoids)
        else:
            # Χρησιμοποίησε ό,τι πέρασε ο χρήστης – αλλιώς default arrays
            default_amps = [50, 40, 30, 25, 20, 15, 10, 8, 5, 3]
            default_phs = [0, pi / 6, pi / 4, pi / 3, pi / 2, pi, 3 * pi / 2, pi / 8, pi / 5, pi / 7]
            default_offs = [0] * num_sinusoids
            amps = np.array((manual_amplitudes or default_amps)[:num_sinusoids])
            phases = np.array((manual_phases or default_phs)[:num_sinusoids])
            dc_offs = np.array((manual_offsets or default_offs)[:num_sinusoids])

        sin_matrix = np.zeros((num_sinusoids, num_pts))
        for k in range(num_sinusoids):
            omega_k = omega_base * (k + 1)  # 1 year, 1/2 year …
            sin_matrix[k] = amps[k] * np.sin(omega_k * np.arange(num_pts) + phases[k]) + dc_offs[k]
        return sin_matrix

    # ------------------------------------------------------------------
    # 3. Παραγωγή dataset (ίδια βήματα με πριν)
    # ------------------------------------------------------------------
    timestamps = build_time_index()
    num_pts = len(timestamps)
    omega_base = 2 * pi / num_pts

    sin_components = generate_components(num_pts, omega_base)
    signal_sum = sin_components.sum(axis=0)

    high_freq = np.random.uniform(noise_min, noise_max, num_pts)
    final_signal = np.clip(signal_sum + high_freq, clip_min, clip_max)

    df = pd.DataFrame({"timestamp": timestamps, "value": final_signal})
    df.to_json(save_path, orient="records", date_format="iso")

    #print(f"✅ Dataset saved to {save_path.resolve()} (points: {num_pts})")
    return df


# ----------------------------------------------------------------------
# Stand‑alone εκτέλεση (ίδια συμπεριφορά με το αρχικό script)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    generate_synthetic_dataset()