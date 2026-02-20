"""Utility functions for synthetic data generation and visualization."""
import plotly.graph_objects as go
from pathlib import Path
from logic.synthetic_dataset_generator import generate_synthetic_dataset
from utils.paths import UPTIME_DIR

def _synth_series(metric="Uptime", days=30, freq_per_day=24):
    """Generate a synthetic uptime time series."""
    df = generate_synthetic_dataset(
        mode="random",
        frequency_per_day=freq_per_day,
        duration_days=days,
        num_sinusoids=6,
        max_amplitude=40,
        max_dc_offset=10,
        noise_min=-5,
        noise_max=20,
        clip_min=-50,
        clip_max=150,
        save_path=UPTIME_DIR / "uptime_generated_dataset.json",
    )

    # Post-processing ONLY
    df["value"] = df["value"] - df["value"].min()
    df["value"] = 99 - (df["value"] / (df["value"].max() + 1e-9)) * 2.5

    return df[["timestamp", "value"]]


def _indicator(
    value,
    title="Platform Uptime",
    subtitle=None,
    suffix=" %"
):
    """Create a KPI indicator figure (generic, semantic-aware)."""

    title_text = (
        f"{title}<br>"
        f"<span style='font-size:12px;color:#666'>{subtitle}</span>"
        if subtitle else title
    )

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            number={"suffix": suffix},
            title={"text": title_text},
        )
    )

    fig.update_layout(margin=dict(l=6, r=6, t=30, b=6))
    return fig


def _chart(df):
    """Create a line chart for uptime values."""
    fig = go.Figure(go.Scatter(x=df["timestamp"], y=df["value"], mode="lines", name="Uptime (%)"))
    fig.update_layout(title="Uptime History", xaxis_title="Time", yaxis_title="Uptime (%)")
    return fig
