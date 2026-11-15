"""Signals SolverSpec table."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy import signal

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_PI = math.pi
_TWO_PI = 2.0 * _PI


def _harmonic_cn(an: float, bn: float) -> float:
    return math.hypot(an, bn)


def fourier_series_std(
    waveform: str,
    amplitude: float,
    f0_hz: float,
    n_harmonics: float = 9,
) -> dict:
    n_max = int(n_harmonics)
    harmonics: list[dict[str, float]] = []
    for n in range(1, n_max + 1):
        an, bn = 0.0, 0.0
        if waveform == "square":
            if n % 2 == 1:
                bn = 4.0 * amplitude / (n * _PI)
        elif waveform == "triangle":
            if n % 2 == 1:
                bn = (8.0 * amplitude / (n * n * _PI * _PI)) * ((-1) ** ((n - 1) // 2))
        elif waveform == "sawtooth":
            bn = -2.0 * amplitude / (n * _PI) * (-1) ** n
        elif waveform == "half_rect_sine":
            if n == 1:
                an = amplitude / 2.0
            elif n % 2 == 0:
                an = 0.0
            else:
                an = -2.0 * amplitude / (_PI * (n * n - 1))
            bn = 0.0
        elif waveform == "full_rect_sine":
            if n == 1:
                an = 2.0 * amplitude / _PI
            elif n % 2 == 1:
                an = 0.0
            else:
                an = -4.0 * amplitude / (_PI * (n * n - 1))
            bn = 0.0
        else:
            raise ValueError(
                f"waveform must be square, triangle, sawtooth, half_rect_sine, or full_rect_sine, got {waveform!r}"
            )
        harmonics.append({"n": float(n), "an": an, "bn": bn, "cn": _harmonic_cn(an, bn)})
    c1 = harmonics[0]["cn"]
    fund = harmonics[0]["cn"]
    if fund > 0:
        thd_pct = 100.0 * math.sqrt(sum(h["cn"] ** 2 for h in harmonics[1:])) / fund
    else:
        thd_pct = 0.0
    return {
        "c1": c1,
        "harmonics": harmonics,
        "thd_pct": thd_pct,
        "f0_hz": f0_hz,
        "waveform": waveform,
    }


def dt_convolution(
    x: list,
    h: list,
    x_start: float = 0.0,
    h_start: float = 0.0,
) -> dict:
    xv = np.asarray(x, dtype=float)
    hv = np.asarray(h, dtype=float)
    y = np.convolve(xv, hv)
    y_sum = float(np.sum(y))
    y_start = x_start + h_start
    return {
        "y_sum": y_sum,
        "y": [float(v) for v in y],
        "y_start": y_start,
        "x_sum": float(np.sum(xv)),
        "h_sum": float(np.sum(hv)),
    }


def dft_spectrum(samples: list, fs_hz: float) -> dict:
    if len(samples) > 4096:
        raise ValueError("samples length must be at most 4096")
    if len(samples) < 2:
        raise ValueError("need at least 2 samples")
    x = np.asarray(samples, dtype=float)
    mag = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs_hz)
    if len(mag) > 1:
        idx = int(np.argmax(mag[1:]) + 1)
    else:
        idx = 0
    dominant_hz = float(freqs[idx])
    return {
        "dominant_hz": dominant_hz,
        "magnitude": [float(v) for v in mag],
        "freqs_hz": [float(v) for v in freqs],
        "dominant_index": idx,
    }


def sampling_alias(f_signal_hz: float, fs_hz: float) -> dict:
    alias_hz = abs(f_signal_hz - fs_hz * round(f_signal_hz / fs_hz))
    nyquist_ok = fs_hz >= 2.0 * abs(f_signal_hz)
    return {
        "alias_hz": alias_hz,
        "nyquist_ok": nyquist_ok,
        "f_signal_hz": f_signal_hz,
        "fs_hz": fs_hz,
    }


def _inverse_laplace_at_t(num: list[float], den: list[float], t_eval: float) -> float:
    r, p, k = signal.residue(num, den)
    f_t = 0.0
    if k is not None and len(k):
        for ki in np.atleast_1d(k):
            f_t += float(ki)
    for ri, pi in zip(r, p):
        f_t += float(np.real(ri * np.exp(pi * t_eval)))
    return f_t


def laplace_inverse_pf(num: list, den: list, t_eval: float = 1.0) -> dict:
    num_f = [float(x) for x in num]
    den_f = [float(x) for x in den]
    r, p, k = signal.residue(num_f, den_f)
    f_t = _inverse_laplace_at_t(num_f, den_f, t_eval)
    return {
        "f_t": f_t,
        "residues": [complex(x) for x in r],
        "poles": [complex(x) for x in p],
        "direct_terms": [] if k is None else list(np.atleast_1d(k)),
        "t_eval_s": t_eval,
    }


SPECS: dict[str, SolverSpec] = {
    "fourier_series_std": SolverSpec(
        fn=fourier_series_std,
        params=(
            Param(
                "waveform",
                kind="str",
                choices=("square", "triangle", "sawtooth", "half_rect_sine", "full_rect_sine"),
            ),
            Param("amplitude"),
            Param("f0_hz"),
            Param("n_harmonics", default=9.0),
        ),
        value_key="c1",
        unit="1",
    ),
    "dt_convolution": SolverSpec(
        fn=dt_convolution,
        params=(
            Param("x", kind="list"),
            Param("h", kind="list"),
            Param("x_start", default=0.0),
            Param("h_start", default=0.0),
        ),
        value_key="y_sum",
        unit="1",
    ),
    "dft_spectrum": SolverSpec(
        fn=dft_spectrum,
        params=(
            Param("samples", kind="list"),
            Param("fs_hz"),
        ),
        value_key="dominant_hz",
        unit="Hz",
    ),
    "sampling_alias": SolverSpec(
        fn=sampling_alias,
        params=(
            Param("f_signal_hz"),
            Param("fs_hz"),
        ),
        value_key="alias_hz",
        unit="Hz",
    ),
    "laplace_inverse_pf": SolverSpec(
        fn=laplace_inverse_pf,
        params=(
            Param("num", kind="list"),
            Param("den", kind="list"),
            Param("t_eval", default=1.0),
        ),
        value_key="f_t",
        unit="1",
    ),
}