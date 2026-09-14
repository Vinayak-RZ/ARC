#!/usr/bin/env python3
"""D0 stop: COVERAGE.yaml unit-count floors."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_knowledge_tree import main

if __name__ == "__main__":
    raise SystemExit(main(["--floors-only"]))
