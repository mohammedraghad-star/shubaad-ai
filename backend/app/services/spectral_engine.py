import io
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, savgol_filter

def detect_columns(df: pd.DataFrame):
    lower_cols = [c.lower().strip() for c in df.columns]
    w_col = None
    a_col = None

    for original, lower in zip(df.columns, lower_cols):
        if lower in ["wavenumber", "wave_number", "cm-1", "cm^-1", "wn"]:
            w_col = original
        if lower in ["absorbance", "abs", "intensity", "transmittance"]:
            a_col = original

    if w_col is None:
        w_col = df.columns[0]

    if a_col is None:
        if len(df.columns) < 2:
            raise ValueError("CSV must contain two columns.")
        a_col = df.columns[1]

    return w_col, a_col

def baseline_correction(y: np.ndarray):
    x = np.arange(len(y))
    coeff = np.polyfit(x, y, deg=2)
    baseline = np.polyval(coeff, x)
    return y - baseline

def zone_mean(w, y, high, low):
    region = (w <= high) & (w >= low)
    if np.sum(region) == 0:
        return None
    return float(np.mean(y[region]))

def analyze_ftir_csv(content: bytes):
    df = pd.read_csv(io.BytesIO(content))

    if df.shape[1] < 2:
        raise ValueError("CSV must have at least two columns: wavenumber and absorbance.")

    w_col, a_col = detect_columns(df)
    wavenumber = pd.to_numeric(df[w_col], errors="coerce").to_numpy()
    absorbance = pd.to_numeric(df[a_col], errors="coerce").to_numpy()

    mask = ~np.isnan(wavenumber) & ~np.isnan(absorbance)
    wavenumber = wavenumber[mask]
    absorbance = absorbance[mask]

    if len(wavenumber) < 20:
        raise ValueError("Spectrum is too short for reliable FTIR analysis.")

    window = 11 if len(absorbance) >= 11 else 5
    if window % 2 == 0:
        window += 1

    smoothed = savgol_filter(absorbance, window_length=window, polyorder=2)
    corrected = baseline_correction(smoothed)

    max_abs = np.max(np.abs(corrected))
    normalized = corrected / max_abs if max_abs != 0 else corrected

    peaks_idx, _ = find_peaks(normalized, prominence=0.03)

    peaks = [
        {
            "wavenumber_cm1": float(wavenumber[idx]),
            "relative_intensity": float(normalized[idx])
        }
        for idx in peaks_idx[:50]
    ]

    zones = {
        "OH_NH_3600_3200": zone_mean(wavenumber, normalized, 3600, 3200),
        "Aliphatic_CH_3000_2800": zone_mean(wavenumber, normalized, 3000, 2800),
        "Carbonyl_1760_1620": zone_mean(wavenumber, normalized, 1760, 1620),
        "Amide_II_1580_1510": zone_mean(wavenumber, normalized, 1580, 1510),
        "Polysaccharide_SiO_PO4_1120_990": zone_mean(wavenumber, normalized, 1120, 990)
    }

    return {
        "status": "success",
        "points": int(len(wavenumber)),
        "preprocessing": [
            "Savitzky-Golay smoothing",
            "second-order polynomial baseline correction",
            "maximum absolute normalization"
        ],
        "detected_peaks": peaks,
        "spectral_zone_means": zones,
        "scientific_note": "This v1 engine is for screening. Publication-grade analysis still requires replication, validation, calibration, and uncertainty reporting."
    }
