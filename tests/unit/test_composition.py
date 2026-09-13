from electrical_engineer.compose.graph import ComposeError, compose


def test_over_cap_rejects() -> None:
    nodes = {f"n{i}": {"activity": "solve-explain"} for i in range(17)}
    try:
        compose({"nodes": nodes, "edges": []})
    except ComposeError as exc:
        assert "16" in str(exc)
    else:
        raise AssertionError("expected cap")


def test_capability_id_composes() -> None:
    out = compose(
        {
            "id": "hand",
            "nodes": {"n0": {"capability": "algebraic-check"}},
            "edges": [],
        }
    )
    assert out["ok"] is True


def test_unknown_capability_rejected() -> None:
    try:
        compose({"nodes": {"n0": {"activity": "lookup_vout_guess"}}, "edges": []})
    except ComposeError as exc:
        assert "unknown id" in str(exc)
    else:
        raise AssertionError("expected reject")
