"""Hatch hook: ensure ui/dist exists so editable installs succeed without a prebuilt UI."""

from __future__ import annotations

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class UiDistHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:
        ui_dist = Path(self.root) / "ui" / "dist"
        ui_dist.mkdir(parents=True, exist_ok=True)
        index = ui_dist / "index.html"
        if not index.is_file():
            index.write_text(
                "<!DOCTYPE html><html><head><title>Arc</title></head>"
                "<body><p>UI not built. Run <code>npm run build</code> in ui/.</p></body></html>",
                encoding="utf-8",
            )