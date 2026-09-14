#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parent / "scenarios"
files = list(root.rglob("*.json"))
print(f"total: {len(files)}")
