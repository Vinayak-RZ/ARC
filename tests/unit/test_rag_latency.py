import json
import time

from electrical_engineer.rag.retrieve import retrieve


def test_retrieve_latency_under_budget() -> None:
    t0 = time.perf_counter()
    out = retrieve({"book_id": "kuphaldt-dc"}, query="Ohm's law voltage current resistance")
    elapsed = time.perf_counter() - t0
    assert out["empty"] is False
    assert elapsed < 7.0
    assert out["elapsed_ms"] < 7000
    assert out["engine"] == "hybrid-graph"
    payload = {"elapsed_s": elapsed, "engine": out["engine"], "n": len(out["passages"])}
    Path = __import__("pathlib").Path
    art = Path("/tmp/rag-latency.json")
    art.write_text(json.dumps(payload, indent=2))
