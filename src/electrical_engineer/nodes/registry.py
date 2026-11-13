"""Registered EE activity nodes. Bodies fail closed except label/summary."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from electrical_engineer.unchecked import UNCHECKED

Activity = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]

REGISTRY: dict[str, Activity] = {}


def register(name: str) -> Callable[[Activity], Activity]:
    def wrap(fn: Activity) -> Activity:
        REGISTRY[name] = fn
        return fn

    return wrap


def _nested_payloads(node: dict[str, Any]) -> list[Any]:
    inner = node.get("inputs")
    if isinstance(inner, dict):
        return list(inner.values())
    return []


def _trap_blocks_checked(inputs: Mapping[str, Any]) -> bool:
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("tool") == "trap-verify" and (
            v.get("ok") is False or v.get("process_pass") is False
        ):
            return True
        frontier.extend(_nested_payloads(v))
    return False


def _web_blocks_checked(inputs: Mapping[str, Any]) -> bool:
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("tool") == "web-verify" or v.get("web_verify_status"):
            if v.get("needs_review"):
                return True
            st = str(v.get("web_verify_status") or "")
            if st in ("pending_host", "unsupported", "needs_review"):
                return True
            if v.get("ok") is False and not v.get("offline_unverified"):
                return True
        frontier.extend(_nested_payloads(v))
    return False


def _walk_checked(inputs: Mapping[str, Any]) -> bool:
    """True when an upstream verifier (including through explain nodes) produced a checked value."""
    if _trap_blocks_checked(inputs) or _web_blocks_checked(inputs):
        return False
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("ok") is True and (v.get("value") is not None or v.get("tool") == "web-verify"):
            if v.get("tool") == "web-verify":
                continue
            return True
        if v.get("unchecked") is False and v.get("value") is not None:
            return True
        frontier.extend(_nested_payloads(v))
    return False


def _first_checked_value(inputs: Mapping[str, Any]) -> Any:
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        if v.get("ok") is True and v.get("value") is not None:
            return v.get("value")
        if v.get("unchecked") is False and v.get("value") is not None:
            return v.get("value")
        frontier.extend(_nested_payloads(v))
    return None


@register("label-unchecked")
def label_unchecked(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    extra = {}
    if _spec.get("cannot_do"):
        extra["cannot_do"] = _spec["cannot_do"]
    if _spec.get("capability"):
        extra["capability"] = _spec["capability"]
    label_message = None
    for v in inputs.values():
        if isinstance(v, dict) and v.get("label_message"):
            label_message = v.get("label_message")
            break
    if label_message:
        extra["label_message"] = label_message
        extra["context_offline_unverified"] = True
    if _walk_checked(inputs):
        value = _first_checked_value(inputs)
        return {"unchecked": False, "token": None, "value": value, "inputs": inputs, **extra}
    return {"unchecked": True, "token": UNCHECKED, "inputs": inputs, **extra}


@register("write-run-summary")
def write_run_summary(_spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    checked = _walk_checked(inputs)
    value = _first_checked_value(inputs) if checked else None
    paths: list[str] = []
    citations: list[Any] = []
    frontier = list(inputs.values())
    steps = 0
    while frontier and steps < 64:
        steps += 1
        v = frontier.pop()
        if not isinstance(v, dict):
            continue
        paths.extend(v.get("paths") or [])
        citations.extend(v.get("citations") or [])
        frontier.extend(_nested_payloads(v))
    web_excerpt: dict[str, Any] = {}
    trap_excerpt: dict[str, Any] = {}
    answer_md = ""
    frontier2 = list(inputs.values())
    steps2 = 0
    while frontier2 and steps2 < 64:
        steps2 += 1
        v = frontier2.pop()
        if not isinstance(v, dict):
            continue
        if v.get("tool") == "trap-verify":
            trap_excerpt = {
                "outcome_pass": v.get("outcome_pass"),
                "process_pass": v.get("process_pass"),
                "outcome_score": v.get("outcome_score"),
                "process_score": v.get("process_score"),
                "checks": v.get("checks"),
            }
        if v.get("tool") == "web-verify":
            web_excerpt = {
                "status": v.get("web_verify_status"),
                "provider": v.get("provider"),
                "needs_review": v.get("needs_review"),
                "offline_unverified": v.get("offline_unverified"),
                "verified_values": v.get("verified_values"),
                "disagreement_banner": v.get("disagreement_banner"),
            }
            answer_md = str(v.get("answer_markdown") or "")
            citations = v.get("citations") or citations
        frontier2.extend(_nested_payloads(v))
    out = {
        "recipe_id": _spec.get("recipe_id", ""),
        "unchecked": not checked,
        "token": None if checked else UNCHECKED,
        "value": value,
        "paths": paths,
        "citations": citations,
        "web_verification": web_excerpt or None,
        "trap_verification": trap_excerpt or None,
        "answer_markdown": answer_md or None,
    }
    run_dir = _spec.get("run_dir")
    if run_dir:
        rd = Path(run_dir)
        cited = rd / "evidence" / "answer_cited.md"
        if cited.is_file() and not answer_md:
            answer_md = cited.read_text(encoding="utf-8")
            out["answer_markdown"] = answer_md
        Path(run_dir, "summary.json").write_text(json.dumps(out, indent=2))
        if answer_md:
            from electrical_engineer.web_verify.provenance import sanitize_verification_markers
            from electrical_engineer.web_verify.validate import audit_markdown_provenance

            try:
                audit_markdown_provenance(answer_md, run_dir=rd)
            except ValueError:
                answer_md, _ = sanitize_verification_markers(answer_md)
                out["answer_markdown"] = answer_md
            (rd / "argument.md").write_text(answer_md, encoding="utf-8")
        out["paths"] = [*paths, str(Path(run_dir) / "summary.json")]
    return out


def get(name: str) -> Activity:
    if name not in REGISTRY:
        raise KeyError(name)
    return REGISTRY[name]


def names() -> list[str]:
    return sorted(REGISTRY)
