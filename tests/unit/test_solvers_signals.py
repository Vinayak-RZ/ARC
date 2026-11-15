from __future__ import annotations

import math

import numpy as np
import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_fourier_square_c1() -> None:
    out = _solve("fourier_series_std", waveform="square", amplitude=1, f0_hz=50)
    assert out["value"] == pytest.approx(4.0 / math.pi, rel=1e-3)


def test_dt_convolution_sum() -> None:
    out = _solve("dt_convolution", x=[1, 2, 3], h=[1, 1])
    assert out["value"] == pytest.approx(12.0, rel=1e-9)
    assert out["result"]["y"] == pytest.approx([1, 3, 5, 3], rel=1e-9)


def test_dft_dominant_50hz() -> None:
    fs = 1000.0
    n = 1000
    t = np.arange(n) / fs
    samples = np.sin(2 * np.pi * 50 * t).tolist()
    out = _solve("dft_spectrum", samples=samples, fs_hz=fs)
    assert out["value"] == pytest.approx(50.0, abs=0.5)


def test_sampling_alias() -> None:
    out = _solve("sampling_alias", f_signal_hz=70, fs_hz=100)
    assert out["value"] == pytest.approx(30.0, rel=1e-9)
    assert out["result"]["nyquist_ok"] is False


def test_laplace_inverse_pf() -> None:
    out = _solve("laplace_inverse_pf", num=[1], den=[1, 3, 2], t_eval=1.0)
    expected = math.exp(-1) - math.exp(-2)
    assert out["value"] == pytest.approx(expected, rel=1e-4)