import json
import subprocess
import sys


def test_reference_cli_search_get() -> None:
    search = subprocess.run(
        [sys.executable, "-m", "electrical_engineer", "reference", "search", "standard inverse"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert search.returncode == 0
    body = json.loads(search.stdout)
    assert any(r["id"] == "IEC_SI" for r in body["results"])
    get = subprocess.run(
        [sys.executable, "-m", "electrical_engineer", "reference", "get", "IEC_SI"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert get.returncode == 0
    rec = json.loads(get.stdout)
    assert rec["values"]["k"] == 0.14
