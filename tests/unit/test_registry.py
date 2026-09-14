from electrical_engineer.nodes import sim as _sim  # noqa: F401
from electrical_engineer.nodes.registry import get, names
from electrical_engineer.unchecked import UNCHECKED


def test_registry_has_label_and_summary() -> None:
    assert "label-unchecked" in names()
    assert "write-run-summary" in names()
    assert "run-simulink-if-present" in names()
    out = get("label-unchecked")({"id": "u"}, {})
    assert out["token"] == UNCHECKED
    assert out["unchecked"] is True
