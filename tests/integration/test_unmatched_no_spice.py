from pathlib import Path

from electrical_engineer.runner.execute import execute


def test_unmatched_run_has_no_spice(tmp_path) -> None:
    out = execute("unmatched-cosolver", run_root=tmp_path)
    blob = "\n".join(p.read_text(encoding="utf-8") for p in Path(out["run_dir"]).rglob("*.json"))
    assert "run-spice" not in blob
    assert out["summary"]["token"] == "unchecked"
