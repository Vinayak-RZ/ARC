"""HTTP routes for Control Studio sessions."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse

from electrical_engineer.control_studio import analyze as analyze_mod
from electrical_engineer.control_studio import session as session_mod
from electrical_engineer.control_studio import simulate as simulate_mod
from electrical_engineer.control_studio.library import PALETTE, PALETTE_GROUPS
from electrical_engineer.control_studio.schema import StudioError
from electrical_engineer.control_studio.validate import validate
from electrical_engineer.ui_server.studio_events import sse_stream


def register_studio_routes(app: FastAPI, *, root: Path) -> None:
    @app.get("/api/control-studio/palette")
    def studio_palette() -> dict:
        return {"palette": PALETTE, "groups": PALETTE_GROUPS}

    @app.get("/api/control-studio/sessions")
    def studio_list() -> dict:
        return {"sessions": session_mod.list_sessions(root)}

    @app.post("/api/control-studio/sessions")
    async def studio_create(request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        golden = body.get("golden")
        title = str(body.get("title") or "Control Studio")
        seed = str(golden) if golden else ("pid_dc_motor" if body.get("seed_golden") else None)
        payload = session_mod.create_session(title, root, golden=seed)
        return payload

    @app.get("/api/control-studio/sessions/{session_id}")
    def studio_get(session_id: str) -> dict:
        try:
            return session_mod.load_session(session_id, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.put("/api/control-studio/sessions/{session_id}/diagram")
    async def studio_put_diagram(session_id: str, request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        author = str(body.get("author") or "human")
        op = str(body.get("op") or "edit")
        target = body.get("target")
        detail = body.get("detail") if isinstance(body.get("detail"), dict) else None
        try:
            return session_mod.apply_diagram(
                session_id,
                body.get("diagram") or body,
                author=author,
                op=op,
                target=str(target) if target is not None else None,
                detail=detail,
                root=root,
            )
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/undo")
    async def studio_undo(session_id: str, request: Request) -> dict:
        body = await request.json()
        author = "human"
        if isinstance(body, dict):
            author = str(body.get("author") or "human")
        try:
            return session_mod.undo(session_id, author=author, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/redo")
    async def studio_redo(session_id: str, request: Request) -> dict:
        try:
            return session_mod.redo(session_id, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/validate")
    def studio_validate(session_id: str) -> dict:
        try:
            payload = session_mod.load_session(session_id, root)
            return validate(payload["diagram"])
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    def _write_studio_run_summary(run_dir: Path, diagram: dict, updated_at_ms: int | None) -> None:
        import json
        import time

        title = str(diagram.get("title") or "Control Studio").strip()
        run_dir.mkdir(parents=True, exist_ok=True)
        run_dir.joinpath("summary.json").write_text(
            json.dumps(
                {
                    "title": title,
                    "recipe_id": "control-studio",
                    "unchecked": False,
                    "updated_at_ms": updated_at_ms or int(time.time() * 1000),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    @app.post("/api/control-studio/sessions/{session_id}/simulate")
    async def studio_sim(session_id: str, request: Request) -> dict:
        try:
            body = {}
            try:
                body = await request.json()
            except Exception:  # noqa: BLE001
                body = {}
            if not isinstance(body, dict):
                body = {}
            payload = session_mod.load_session(session_id, root)
            run_dir = root / "runs" / session_id
            _write_studio_run_summary(run_dir, payload.get("diagram") or {}, payload.get("updated_at_ms"))
            t_final = body.get("t_final", "auto")
            an_pre = analyze_mod.analyze(payload["diagram"], run_dir=run_dir) if t_final == "auto" else {}
            sim = simulate_mod.simulate(
                payload["diagram"],
                run_dir=run_dir,
                t_final=t_final,
                margins=an_pre if an_pre.get("ok") else None,
            )
            if not sim.get("ok"):
                return sim
            an = analyze_mod.analyze(payload["diagram"], run_dir=run_dir)
            out = {**sim, "analyze": an}
            if an.get("ok"):
                for key in (
                    "gain_margin_db",
                    "phase_margin_deg",
                    "phase_crossover_rad_s",
                    "gain_crossover_rad_s",
                    "display",
                ):
                    if key in an:
                        out[key] = an[key]
            return out
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.post("/api/control-studio/sessions/{session_id}/analyze")
    def studio_analyze(session_id: str) -> dict:
        try:
            payload = session_mod.load_session(session_id, root)
            run_dir = root / "runs" / session_id
            return analyze_mod.analyze(payload["diagram"], run_dir=run_dir)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.get("/api/control-studio/sessions/{session_id}/events")
    async def studio_events(session_id: str) -> StreamingResponse:
        return StreamingResponse(
            sse_stream(session_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache, no-transform",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    @app.post("/api/control-studio/sessions/{session_id}/notes")
    async def studio_note(session_id: str, request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        try:
            return session_mod.add_note(
                session_id,
                str(body.get("block_id") or ""),
                str(body.get("text") or ""),
                author=str(body.get("author") or "human"),
                root=root,
            )
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.get("/api/control-studio/sessions/{session_id}/plot/{name}")
    def studio_plot(session_id: str, name: str, theme: str = "light") -> Response:
        safe = Path(name).name
        suffix = "_dark" if (theme or "light").strip().lower() == "dark" else ""
        path = root / "runs" / session_id / f"studio_{safe}{suffix}.png"
        if not path.is_file() and suffix:
            path = root / "runs" / session_id / f"studio_{safe}.png"
        if not path.is_file():
            return JSONResponse({"error": "missing"}, status_code=404)
        return FileResponse(
            path,
            media_type="image/png",
            headers={"Cache-Control": "no-store"},
        )

    def _graph_series_rlc(graph: dict) -> dict | None:
        by_type: dict[str, list] = {}
        for node in graph.get("nodes") or []:
            t = str(node.get("type") or "")
            by_type.setdefault(t, []).append(node)
        need = {"source_v", "resistor", "inductor", "capacitor"}
        if not need <= set(by_type):
            return None
        try:
            return {
                "kind": "series_rlc",
                "v_step": float(by_type["source_v"][0].get("value") or 10),
                "r_ohm": float(by_type["resistor"][0].get("value") or 10),
                "l_h": float(by_type["inductor"][0].get("value") or 0.01),
                "c_f": float(by_type["capacitor"][0].get("value") or 1e-6),
            }
        except (TypeError, ValueError):
            return None

    @app.post("/api/circuit-sandbox/simulate")
    async def circuit_sandbox_simulate(request: Request) -> dict:
        import tempfile

        from electrical_engineer.circuit.graph import (
            GraphError,
            format_series_rlc_param_strip,
            graph_port_errors,
            parse_graph,
            probe_for_capacitor,
        )
        from electrical_engineer.circuit.simulate_graph import simulate_graph
        from electrical_engineer.engines.rlc_transient import solve_from_problem

        body = await request.json()
        graph = body.get("graph") if isinstance(body, dict) else {}
        if not graph:
            return JSONResponse({"ok": False, "error": "Missing circuit graph"}, status_code=400)
        try:
            parsed = parse_graph(graph if isinstance(graph, dict) else {})
        except GraphError as exc:
            return JSONResponse({"ok": False, "error": str(exc)}, status_code=400)
        port_errs = graph_port_errors(parsed)
        if port_errs:
            return JSONResponse({"ok": False, "error": "; ".join(port_errs[:3])}, status_code=400)
        problem = _graph_series_rlc(parsed)
        if problem is None:
            return JSONResponse(
                {"ok": False, "error": "Sandbox simulate needs a series R–L–C graph (V, R, L, C, GND)."},
                status_code=400,
            )
        problem |= {
            "analysis": "tran",
            "t_s": body.get("t_s") if isinstance(body, dict) else None,
            "derive_metric": "Vc_peak",
            "probe": probe_for_capacitor(parsed) or "v(3)",
            "tol": 0.02,
        }
        if not problem.get("t_s"):
            try:
                meta = solve_from_problem({**problem, "v_step": problem["v_step"]})
                problem["t_s"] = float(meta.get("t_Vc_peak_s") or 0.003628)
            except (TypeError, ValueError):
                problem["t_s"] = 0.003628
        with tempfile.TemporaryDirectory() as tmp:
            sim = simulate_graph(parsed, problem, run_dir=Path(tmp))
        if not sim.get("ok") and sim.get("skipped"):
            return JSONResponse(
                {"ok": False, "error": sim.get("reason") or "ngspice not available", "skipped": True},
                status_code=503,
            )
        if not sim.get("ok"):
            return JSONResponse({"ok": False, "error": sim.get("error") or "simulate failed"}, status_code=400)
        try:
            trace = solve_from_problem({**problem, "v_step": problem["v_step"]})
        except ValueError:
            trace = {"Vc_peak_V": sim.get("simulated"), "t_Vc_peak_s": problem.get("t_s")}
        peak = float(sim.get("simulated") if sim.get("simulated") is not None else trace.get("Vc_peak_V"))
        trace = {**trace, "Vc_peak_V": peak}
        backend = (sim.get("simulator") or {}).get("backend") or sim.get("engine") or "ngspice"
        param_strip = format_series_rlc_param_strip(parsed)
        final_v = float(
            sim.get("simulated")
            if sim.get("simulated") is not None
            else (trace.get("Vc_peak_V") or peak)
        )
        trace = {**trace, "Vc_peak_V": final_v}
        overshoot_pct = float(trace.get("overshoot_pct") or 0.0)
        headline = None
        if overshoot_pct < 0.5:
            t_set_ms = float(trace.get("settling_2pct_entry_s") or trace.get("settling_time_2pct_s") or 0) * 1000
            headline = f"No overshoot · Final value {final_v:.2f} V · Settling (2%) {t_set_ms:.2f} ms"
        else:
            t_pk_ms = float(trace.get("t_Vc_peak_s") or 0) * 1000
            headline = f"Vc,peak = {final_v:.3f} V at {t_pk_ms:.2f} ms"
        return {
            "ok": True,
            "engine": backend,
            "problem": problem,
            "result": {**trace, "Vc_peak_V": final_v, "simulated_Vc_peak_V": final_v},
            "sim": sim,
            "param_strip": param_strip,
            "headline": headline,
        }
