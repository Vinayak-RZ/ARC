"""CLI command surface. Later nodes fill mcp/eval/ui/rag/memory bodies."""

from __future__ import annotations

import argparse
import sys

from electrical_engineer import __version__

COMMANDS = (
    "run",
    "workflows",
    "mcp",
    "eval",
    "ui",
    "rag",
    "memory",
    "hosts",
    "control-studio",
    "lab",
    "reference",
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="electrical-engineer")
    p.add_argument("--version", action="version", version=f"electrical-engineer {__version__}")
    sub = p.add_subparsers(dest="cmd")
    run = sub.add_parser("run")
    run.add_argument("workflow_id", nargs="?")
    run.add_argument("--allow-all", action="store_true")
    sub.add_parser("workflows")
    sub.add_parser("mcp")
    ev = sub.add_parser("eval")
    ev.add_argument("--pack")
    ui = sub.add_parser("ui")
    ui.add_argument("--run")
    rag = sub.add_parser("rag")
    rag.add_argument("action", nargs="?", default="list")
    rag.add_argument("path", nargs="?")
    rag.add_argument("--book-id")
    rag.add_argument("--chapter-id")
    rag.add_argument("--folder-tag")
    rag.add_argument("--domain-tag")
    rag.add_argument("--licence-tag")
    rag.add_argument("--query", default="")
    rag.add_argument("--hops", type=int, default=1)
    mem = sub.add_parser("memory")
    mem.add_argument("action", nargs="?", default="list")
    ref = sub.add_parser("reference")
    ref_sub = ref.add_subparsers(dest="reference_cmd")
    ref_search = ref_sub.add_parser("search")
    ref_search.add_argument("query")
    ref_get = ref_sub.add_parser("get")
    ref_get.add_argument("record_id")
    ref_eng = ref_sub.add_parser("engine")
    ref_eng.add_argument("engine_name")
    ref_eng.add_argument("json_payload", nargs="?", default="{}")
    prov = sub.add_parser("provenance", help="Audit answer/notes files for false web-verified labels")
    prov_sub = prov.add_subparsers(dest="provenance_cmd")
    prov_audit = prov_sub.add_parser("audit")
    prov_audit.add_argument("path")
    prov_audit.add_argument("--run-dir")
    hosts = sub.add_parser("hosts")
    hsub = hosts.add_subparsers(dest="hosts_cmd")
    inst = hsub.add_parser("install")
    inst.add_argument("--into", required=True)
    inst.add_argument(
        "--host",
        default="all",
        choices=("all", "cursor", "codex", "claude"),
    )
    hsub.add_parser("uninstall", help="Remove vertical pack files listed in install state").add_argument(
        "--into", required=True
    )
    hsub.add_parser("doctor", help="Report engines and optional backends")
    smoke = hsub.add_parser("smoke", help="Install smoke + contract JSON for CI")
    smoke.add_argument("--into", default=None, help="Temp homework dir (default: .vertical-pack-smoke)")
    cs = sub.add_parser("control-studio", help="Control Studio CLI (same model as UI/MCP)")
    cs.add_argument("action", nargs="?", default="create", choices=("create", "validate", "simulate", "analyze", "export"))
    cs.add_argument("--session", dest="session_id")
    cs.add_argument("--title", default="Control Studio")
    cs.add_argument("--out")
    lab = sub.add_parser("lab", help="Shared lab artifacts on runs (circuit)")
    lab.add_argument(
        "action",
        nargs="?",
        default="get",
        choices=("get", "finish", "simulate", "open"),
    )
    lab.add_argument("--run", dest="run_id", required=False)
    lab.add_argument("--problem", default=None, help="JSON problem payload for finish")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        return 0
    if args.cmd == "run":
        import json
        from pathlib import Path

        from electrical_engineer.runner.execute import execute

        if not args.workflow_id:
            from electrical_engineer.router.classify import scores_from_text
            from electrical_engineer.router.hybrid import route

            problem = None
            problem_path = Path("problem.json")
            if problem_path.is_file():
                problem = json.loads(problem_path.read_text())
            text = ""
            if isinstance(problem, dict):
                text = str(
                    problem.get("task")
                    or problem.get("query")
                    or problem.get("kind")
                    or ""
                )
            decided = route(None, scores_from_text(text))
            if decided.kind == "ask":
                print("ask: ambiguous workflow; pass an explicit id", file=sys.stderr)
                return 2
            args.workflow_id = decided.recipe_id
        problem = None
        problem_path = Path("problem.json")
        if problem_path.is_file():
            problem = json.loads(problem_path.read_text())
        out = execute(args.workflow_id, allow_all=args.allow_all, problem=problem)
        print(out["run_id"])
        print(json.dumps(out["summary"], indent=2))
        return 0
    if args.cmd == "mcp":
        from electrical_engineer.mcp.server import serve

        serve()
        return 0
    if args.cmd == "workflows":
        from electrical_engineer.catalog import list_workflow_ids

        print("\n".join(list_workflow_ids()) or "(none)")
        return 0
    if args.cmd == "memory":
        from electrical_engineer.memory.store import list_files, project_memory
        from electrical_engineer.runner.runs import project_root

        for p in list_files(project_memory(project_root())):
            print(p)
        return 0
    if args.cmd == "ui":
        import webbrowser

        import uvicorn

        from electrical_engineer.ui_server.app import (
            BIND_HOST,
            BIND_PORT,
            create_app,
            should_open_browser,
            ui_page_url,
        )

        if should_open_browser():
            webbrowser.open(ui_page_url(args.run))
        uvicorn.run(create_app(), host=BIND_HOST, port=BIND_PORT)
        return 0
    if args.cmd == "eval":
        from electrical_engineer.eval_runner.score import run_pack

        return run_pack(args.pack)
    if args.cmd == "rag":
        import json

        from electrical_engineer.rag.inventory import add_doc, listed_inventory, tag_doc
        from electrical_engineer.rag.retrieve import retrieve

        tags = {
            "book_id": getattr(args, "book_id", None),
            "chapter_id": getattr(args, "chapter_id", None),
            "folder_tag": getattr(args, "folder_tag", None),
            "domain_tag": getattr(args, "domain_tag", None),
            "licence_tag": getattr(args, "licence_tag", None),
        }
        if args.action == "list":
            print(json.dumps(listed_inventory(), indent=2))
            return 0
        if args.action == "add":
            if not args.path:
                print("rag add <path>", file=sys.stderr)
                return 2
            add_doc(args.path, tags=tags)
            print(args.path)
            return 0
        if args.action == "tag":
            if not args.path:
                print("rag tag <path>", file=sys.stderr)
                return 2
            tag_doc(args.path, tags)
            return 0
        if args.action == "query":
            filters = {k: v for k, v in tags.items() if v}
            q = args.query or args.path or ""
            out = retrieve(filters, query=q, hops=args.hops)
            print(json.dumps(out, indent=2))
            return 0 if not out.get("empty") else 1
        print(args.action)
        return 0
    if args.cmd == "control-studio":
        import json
        from pathlib import Path

        from electrical_engineer.control_studio import analyze as cs_analyze
        from electrical_engineer.control_studio import session as cs_session
        from electrical_engineer.control_studio import simulate as cs_simulate
        from electrical_engineer.control_studio.validate import validate
        from electrical_engineer.runner.runs import project_root

        root = project_root()
        sid = args.session_id
        if args.action == "create":
            payload = cs_session.create_session(args.title, root)
            print(payload["session_id"])
            print(json.dumps(payload["diagram"], indent=2))
            return 0
        if not sid:
            print("--session required", file=sys.stderr)
            return 2
        payload = cs_session.load_session(sid, root)
        diagram = payload["diagram"]
        if args.action == "validate":
            print(json.dumps(validate(diagram), indent=2))
            return 0
        run_dir = root / "runs" / sid
        if args.action == "simulate":
            print(json.dumps(cs_simulate.simulate(diagram, run_dir=run_dir), indent=2))
            return 0
        if args.action == "analyze":
            print(json.dumps(cs_analyze.analyze(diagram, run_dir=run_dir), indent=2))
            return 0
        if args.action == "export":
            dest = Path(args.out) if args.out else Path(f"{sid}.diagram.json")
            dest.write_text(json.dumps(diagram, indent=2), encoding="utf-8")
            print(dest)
            return 0
        return 2
    if args.cmd == "lab":
        import json
        from pathlib import Path

        from electrical_engineer.circuit import mcp_lab
        from electrical_engineer.collab.workflow import finish_circuit_lab
        from electrical_engineer.runner.runs import create_run_dir, new_run_id, project_root

        root = project_root()
        rid = args.run_id or new_run_id()
        run_dir = root / "runs" / rid
        if not run_dir.is_dir():
            create_run_dir(root, rid)
        if args.action == "get":
            out = mcp_lab.handle_tool("arc_circuit_lab_get", {"run_id": rid})
            print(json.dumps(out, indent=2))
            return 0 if "error" not in out else 1
        if args.action == "finish":
            prob = json.loads(args.problem) if args.problem else {}
            if not prob and (run_dir / "problem.json").is_file():
                prob = json.loads((run_dir / "problem.json").read_text(encoding="utf-8"))
            if not prob:
                print("lab finish needs --problem or runs/<id>/problem.json", file=sys.stderr)
                return 2
            verify = finish_circuit_lab(run_dir, prob)
            print(json.dumps({"run_id": rid, "verify": verify}, indent=2))
            return 0 if verify.get("ok") else 1
        if args.action == "simulate":
            prob = json.loads(args.problem) if args.problem else {}
            out = mcp_lab.handle_tool("arc_circuit_lab_simulate", {"run_id": rid, "problem": prob})
            print(json.dumps(out, indent=2))
            return 0 if out.get("ok") else 1
        if args.action == "open":
            from electrical_engineer.collab.lab_meta import load_lab_meta, ui_lab_url

            meta = load_lab_meta(run_dir)
            if not meta:
                meta = {"kind": "circuit"}
            print(ui_lab_url(rid, meta))
            return 0
        return 2
    if args.cmd == "provenance":
        import json
        from pathlib import Path

        from electrical_engineer.web_verify.validate import audit_markdown_provenance

        if args.provenance_cmd == "audit":
            run_dir = Path(args.run_dir) if args.run_dir else None
            text = Path(args.path).read_text(encoding="utf-8")
            try:
                audit_markdown_provenance(text, run_dir=run_dir)
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                return 2
            print(json.dumps({"ok": True, "path": args.path}, indent=2))
            return 0
        print("provenance audit <file>", file=sys.stderr)
        return 2
    if args.cmd == "reference":
        import json

        from electrical_engineer.reference.cli_handlers import cmd_engine, cmd_get, cmd_search

        if args.reference_cmd == "search":
            return cmd_search(args.query)
        if args.reference_cmd == "get":
            return cmd_get(args.record_id)
        if args.reference_cmd == "engine":
            payload = json.loads(args.json_payload or "{}")
            return cmd_engine(args.engine_name, payload)
        print("reference search|get|engine", file=sys.stderr)
        return 2
    if args.cmd == "hosts":
        import json
        from pathlib import Path as _Path

        from electrical_engineer import vertical_pack

        if args.hosts_cmd == "install":
            for path in vertical_pack.install_pack(_Path(args.into), host=args.host):
                print(path)
            return 0
        if args.hosts_cmd == "uninstall":
            for path in vertical_pack.uninstall_pack(_Path(args.into)):
                print(path)
            return 0
        if args.hosts_cmd == "doctor":
            print(json.dumps(vertical_pack.doctor(), indent=2))
            return 0
        if args.hosts_cmd == "smoke":
            into = _Path(args.into) if args.into else None
            print(json.dumps(vertical_pack.smoke_contract(into), indent=2))
            return 0
        print("electrical-engineer hosts install|uninstall|doctor|smoke", file=sys.stderr)
        return 2
    print(args.cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
