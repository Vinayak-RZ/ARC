"""CLI wrapper for agent UI diagram artifact checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.ui_diagrams.check import (
    DiagramCheckError,
    check_artifact_file,
    check_control_diagram,
    check_rlc_graph,
    check_run_dir,
)


def _check_examples_dir(ex_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(ex_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if path.name.endswith("_graph.json") or path.name == "rlc_graph.json":
            errors.extend(check_rlc_graph(data, path=path.name))
        elif path.name.endswith("_control_diagram.json"):
            errors.extend(check_control_diagram(data, path=path.name))
        else:
            errors.append(f"{path.name}: unknown example naming")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check graph.json / control_diagram.json for IITR UI law")
    parser.add_argument("--path", type=Path, help="Single artifact file (graph.json or control_diagram.json)")
    parser.add_argument("--run-dir", type=Path, help="Run directory under runs/")
    parser.add_argument("--examples", action="store_true", help="Check skills/ui-diagrams/examples/*.json")
    args = parser.parse_args()
    errors: list[str] = []
    try:
        if args.examples:
            errors.extend(_check_examples_dir(ROOT / "skills" / "ui-diagrams" / "examples"))
            errors.extend(_check_examples_dir(ROOT / "eval" / "gold" / "ui-diagrams"))
        elif args.path:
            errors.extend(check_artifact_file(args.path))
        elif args.run_dir:
            errors.extend(check_run_dir(args.run_dir))
        else:
            parser.error("one of --path, --run-dir, or --examples required")
    except DiagramCheckError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
