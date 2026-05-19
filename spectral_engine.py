import io
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, savgol_filter

def _detect_columns(df: pd.DataFrame):
    cols = [c.lower().strip() for c in df.columns]
    wavenumber_candidates = ["wavenumber", "wave_number", "cm-1", "cm^-1", "wn"]
    absorbance_candidates = ["absorbance", "abs", "intensity", "transmittance"]

    w_col = None
    a_col = None

    for original, lower in zip(df.columns, cols):
        if lower in wavenumber_candidates:
            w_col = original
        if lower in absorbance_candidates:
            a_col = original

    if w_col is None:
        w_col = df.columns[0]
    if a_col is None:
        a_col = df.columns[1] if len(df.columns) > 1 else None

    if a_col is None:
        raise ValueError("CSV must contain wavenumber and absorbance columns.")

    return w_col, a_col

def baseline_correction(y: np.ndarray):
    x = np.arange(len(y))
    coeff = np.polyfit(x, y, deg=2)
    baseline = np.polyval(coeff, x)
    corrected = y - baseline
    return corrected

def _zone_mean(w, y, high, low):
    region = (w <= high) & (w >= low)
    if np.sum(region) == 0:
        return None
    return float(np.mean(y[region]))

def analyze_ftir_csv(content: bytes):
    df = pd.read_csv(io.BytesIO(content))
    if df.shape[1] < 2:
        raise ValueError("CSV must have at least two columns: wavenumber and absorbance.")

    w_col, a_col = _detect_columns(df)
    wavenumber = pd.to_numeric(df[w_col], errors="coerce").to_numpy()
    absorbance = pd.to_numeric(df[a_col], errors="coerce").to_numpy()

    mask = ~np.isnan(wavenumber) & ~np.isnan(absorbance)
    wavenumber = wavenumber[mask]
    absorbance = absorbance[mask]

    if len(wavenumber) < 20:
        raise ValueError("Spectrum is too short for reliable analysis.")

    window = 11 if len(absorbance) >= 11 else 5
    if window % 2 == 0:
        window += 1

    smoothed = savgol_filter(absorbance, window_length=window, polyorder=2)
    corrected = baseline_correction(smoothed)
    max_abs = np.max(np.abs(corrected))
    normalized = corrected / max_abs if max_abs != 0 else corrected

    peaks_idx, _ = find_peaks(normalized, prominence=0.03)
    peaks = []
    for idx in peaks_idx[:50]:
        peaks.append({
            "wavenumber_cm1": float(wavenumber[idx]),
            "relative_intensity": float(normalized[idx])
        })

    zones = {
        "OH_NH_3400": _zone_mean(wavenumber, normalized, 3600, 3200),
        "Aliphatic_CH_2920_2850": _zone_mean(wavenumber, normalized, 3000, 2800),
        "Carbonyl_1740_1630": _zone_mean(wavenumber, normalized, 1760, 1620),
        "Amide_II_1550": _zone_mean(wavenumber, normalized, 1580, 1510),
        "Polysaccharide_SiO_PO4_1100_1000": _zone_mean(wavenumber, normalized, 1120, 990)
    }

    return {
        "status": "success",
        "points": int(len(wavenumber)),
        "preprocessing": ["Savitzky-Golay smoothing", "polynomial baseline correction", "max normalization"],
        "detected_peaks": peaks,
        "spectral_zone_means": zones,
        "scientific_note": "This is a v1 screening engine. For publication-grade outputs, validate preprocessing, calibration, replication, and model performance."
    }
