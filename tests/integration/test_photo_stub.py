from pathlib import Path

from electrical_engineer.runner.execute import execute


def test_confirm_does_not_spice(tmp_path) -> None:
    out = execute("photo-to-netlist", run_root=tmp_path)
    run = Path(out["run_dir"])
    texts = [p.read_text(encoding="utf-8") for p in run.rglob("*.json")]
    blob = "\n".join(texts)
    assert "run-spice" not in blob
    confirm = (run / "nodes" / "confirm" / "out.json").read_text(encoding="utf-8")
    assert '"simulate": false' in confirm
    assert '"spice"' not in confirm or '"spice": false' in confirm
