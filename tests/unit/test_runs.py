from datetime import UTC, datetime
from pathlib import Path

from electrical_engineer.runner.runs import ALPHABET, create_run_dir, new_run_id, node_dir


def test_run_id_shape() -> None:
    rid = new_run_id(now=datetime(2026, 9, 10, 16, 21, 48, tzinfo=UTC))
    suffix, ts = rid.split("-", 1)
    assert len(suffix) == 4
    # ALPHABET includes digits; str.islower() is false for digit-only suffixes
    assert all(c in ALPHABET for c in suffix)
    assert ts == "20260910T162148Z"


def test_run_dirs_isolated(tmp_path: Path) -> None:
    a = create_run_dir(tmp_path, "aaaa-20260910T000000Z")
    b = create_run_dir(tmp_path, "bbbb-20260910T000000Z")
    node_dir(a, "spice").joinpath("out.json").write_text("{}")
    assert not (b / "nodes" / "spice" / "out.json").exists()
    assert a.resolve() != b.resolve()
