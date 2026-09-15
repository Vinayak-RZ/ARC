"""Parse providers: text/markdown, PDF text, optional OCR, multimodal adapter stub."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FigureBlock:
    path: str
    caption: str = ""
    page: int | None = None
    ocr_text: str = ""
    low_confidence: bool = False


@dataclass
class ParseResult:
    text: str
    pages: list[str] = field(default_factory=list)
    figures: list[FigureBlock] = field(default_factory=list)
    low_confidence: bool = False
    provider: str = "text"


_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def parse_document(path: Path) -> ParseResult:
    """Dispatch by suffix. OCR/multimodal are optional extras."""
    if not path.is_file():
        return ParseResult(text="", provider="missing")
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(path)
    return _parse_text(path)


def _parse_text(path: Path) -> ParseResult:
    text = path.read_text(errors="replace")
    figures: list[FigureBlock] = []
    for cap, rel in _MD_IMAGE.findall(text):
        fig_path = (path.parent / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
        figures.append(
            FigureBlock(
                path=str(fig_path) if fig_path.is_file() else rel,
                caption=cap.strip(),
            )
        )
    return ParseResult(text=text, pages=[text], figures=figures, provider="text")


def _parse_pdf(path: Path) -> ParseResult:
    try:
        from pypdf import PdfReader
    except ImportError:
        # ponytail: soft-dep; fall back to raw bytes decode
        raw = path.read_text(errors="replace")
        return ParseResult(text=raw, pages=[raw], provider="pdf-fallback", low_confidence=True)

    reader = PdfReader(str(path))
    pages: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        pages.append(f"[page {i}]\n{page.extract_text() or ''}")
    text = "\n".join(pages)
    low = len(text.strip()) < 40
    if low:
        ocr = _try_ocr(path)
        if ocr is not None:
            return ocr
    return ParseResult(text=text, pages=pages, provider="pypdf", low_confidence=low)


def _try_ocr(path: Path) -> ParseResult | None:
    """Optional ocrmypdf → sidecar text. Skip if tooling absent."""
    try:
        import shutil
        import subprocess
        import tempfile
    except ImportError:
        return None
    if shutil.which("ocrmypdf") is None:
        return None
    with tempfile.TemporaryDirectory() as td:
        out_pdf = Path(td) / "ocr.pdf"
        try:
            subprocess.run(
                ["ocrmypdf", "--force-ocr", "--quiet", str(path), str(out_pdf)],
                check=True,
                capture_output=True,
                timeout=120,
            )
        except (subprocess.SubprocessError, OSError):
            return None
        try:
            from pypdf import PdfReader
        except ImportError:
            return None
        pages = []
        for i, page in enumerate(PdfReader(str(out_pdf)).pages, start=1):
            pages.append(f"[page {i}]\n{page.extract_text() or ''}")
        text = "\n".join(pages)
        return ParseResult(text=text, pages=pages, provider="ocrmypdf", low_confidence=False)


def multimodal_adapter_available() -> bool:
    """RAG-Anything / MinerU optional. Never required in CI."""
    try:
        import importlib.util

        return importlib.util.find_spec("raganything") is not None
    except (ImportError, ValueError):
        return False


def parse_multimodal(path: Path) -> ParseResult | None:
    """Map a multimodal provider into ParseResult when installed; else None."""
    if not multimodal_adapter_available():
        return None
    # ponytail: provider ships its own API; we only declare the hook until installed
    return None
