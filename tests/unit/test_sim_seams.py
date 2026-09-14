from electrical_engineer.nodes import sim as _sim  # noqa: F401
from electrical_engineer.nodes.registry import get


def test_missing_spice_is_clear() -> None:
    out = get("run-spice")({"id": "sp"}, {})
    assert out["ok"] is False
    assert "ngspice" in out["error"]
    assert out["unchecked"] is True


def test_matlab_missing_clear() -> None:
    out = get("run-matlab-if-present")({"id": "m"}, {})
    assert "matlab" in out["error"].lower()


def test_simulink_missing_clear() -> None:
    out = get("run-simulink-if-present")({"id": "s"}, {})
    assert out["ok"] is False
    assert out["cannot_do"] == "CD-SIMULINK-PLANT"
    assert "simulink" in out["error"].lower()
