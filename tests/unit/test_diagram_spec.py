from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.visual_kit.diagram_spec import diagram_for_run, voltage_divider
from electrical_engineer.visual_kit.diagram_study import STUDY_BUILDERS
from electrical_engineer.visual_kit.diagram_validate import validate_diagram

_NONE_RECIPES = frozenset(
    {
        "routh-hurwitz-study",
        "kmap-minimization-study",
        "line-parameters-study",
        "capacitance-geometry-study",
    }
)


def test_builders_validate() -> None:
    d = voltage_divider({"vin": 10, "r1": 1000, "r2": 1000})
    assert validate_diagram(d) == []
    out = diagram_for_run(None, "solve-circuit-problem", {"kind": "voltage_divider", "vin": 10, "r1": 1, "r2": 1})  # type: ignore[arg-type]
    assert out and validate_diagram(out) == []
    swing = diagram_for_run(None, "smib-swing-study", {})  # type: ignore[arg-type]
    assert swing and validate_diagram(swing) == []


def test_study_recipe_dispatch_coverage() -> None:
    assert len(STUDY_BUILDERS) == 38


def test_new_study_diagrams_validate_or_none() -> None:
    sample_ids = [
        "rectifier-1ph-study",
        "boost-converter-study",
        "idmt-relay-study",
        "fourier-series-study",
        "resonance-study",
        "routh-hurwitz-study",
        "line-parameters-study",
    ]
    for rid in sample_ids:
        meta = load_recipe_meta(rid)
        problem = dict(meta.get("sample_problem") or {})
        problem.pop("expected", None)
        problem.pop("tol", None)
        diagram = diagram_for_run(None, rid, problem)  # type: ignore[arg-type]
        if rid in _NONE_RECIPES:
            assert diagram is None
        else:
            assert diagram is not None
            assert validate_diagram(diagram) == []


def test_all_study_builders_under_point_cap() -> None:
    for rid, builder in STUDY_BUILDERS.items():
        if rid in _NONE_RECIPES:
            assert builder({}) is None
            continue
        meta = load_recipe_meta(rid)
        problem = {k: v for k, v in (meta.get("sample_problem") or {}).items() if k not in ("expected", "tol")}
        diagram = builder(problem)
        assert diagram is not None
        for panel in diagram.get("panels") or []:
            if panel.get("kind") != "waveform":
                continue
            for series in panel.get("series") or []:
                assert len(series.get("points") or []) <= 4000