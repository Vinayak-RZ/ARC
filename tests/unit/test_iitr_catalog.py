from pathlib import Path

CATALOG = Path("research/notes/iitr-ee-book-catalog.md")


def test_every_core_heading_has_licence_tag() -> None:
    text = CATALOG.read_text(encoding="utf-8")
    heads = []
    current = None
    tags: dict[str, bool] = {}
    for line in text.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            heads.append(current)
            tags[current] = False
        elif current and "licence_tag:" in line:
            tags[current] = True
    assert heads, "catalog has no ### course headings"
    missing = [h for h, ok in tags.items() if not ok]
    assert not missing, f"missing licence_tag: {missing}"


def test_catalog_forbids_pirate_and_git_binaries() -> None:
    text = CATALOG.read_text(encoding="utf-8")
    assert "Pirate hosts are not sources" in text
    assert "no commercial book bytes in git" in text
    assert "byo_status: needed" in text
