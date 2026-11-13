"""Studio block widths in Python layout must match studio.css."""

from __future__ import annotations

import re
from pathlib import Path

from electrical_engineer.control_studio.layout import BLOCK_W, GAP, PID_W, SUM_W

ROOT = Path(__file__).resolve().parents[2]
CSS = (ROOT / "ui" / "src" / "control-studio" / "studio.css").read_text(encoding="utf-8")


def _width(selector: str) -> int:
    m = re.search(rf"{re.escape(selector)}\s*\{{(.*?)}}", CSS, re.DOTALL)
    assert m, f"missing rule for {selector}"
    wm = re.search(r"^\s*width:\s*(\d+)px", m.group(1), re.MULTILINE)
    assert wm, f"missing width for {selector}"
    return int(wm.group(1))


def test_python_layout_matches_css() -> None:
    assert _width(".studio-pid.studio-block") == PID_W
    assert _width(".studio-sum.studio-block") == SUM_W
    m = re.search(r"\.studio-block\s*\{[^}]*width:\s*(\d+)px", CSS)
    assert m and int(m.group(1)) == BLOCK_W
    assert GAP >= 48
