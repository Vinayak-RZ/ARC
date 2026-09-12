#!/usr/bin/env bash
# Research artifact validator for Electrical-Engineer research phase.
# Exit 0 = PASS, non-zero = FAIL.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FULL=0
if [[ "${1:-}" == "--full" ]]; then
  FULL=1
fi

FAIL=0
fail() { echo "FAIL: $*"; FAIL=1; }
ok() { echo "OK: $*"; }

PLACEHOLDER_RE='TODO|TBD|FIXME|\[Note title\]|\[brackets\]'
PRD_RE='^#+ .*[Rr]equirement|^#+ .*[Ss]hall |^#+ .*[Mm]ust ship'

echo "=== research validate (full=$FULL) ==="

# 1. Shape checks on research markdown
shopt -s nullglob
NOTES=(research/**/*.md research/*.md)
if [[ ${#NOTES[@]} -eq 0 ]]; then
  fail "no research markdown files found"
fi

for f in research/*.md research/notes/*.md research/synthesis/*.md; do
  [[ -f "$f" ]] || continue
  # Map / template / registers are not research notes — skip note-shape rules
  case "$f" in
    research/README.md|research/NOTE.template.md|research/question-bank.md|research/DECISION_REGISTER.md|research/source-ledger.md)
      continue
      ;;
  esac
  for heading in "## Sources" "## Confidence"; do
    if ! grep -qF "$heading" "$f"; then
      fail "$f missing $heading"
    fi
  done
  if grep -nE "$PLACEHOLDER_RE" "$f" >/dev/null 2>&1; then
    fail "$f contains placeholder/TODO tokens: $(grep -nE "$PLACEHOLDER_RE" "$f" | head -3 | tr '\n' ' ')"
  fi
done
# Template must still declare the required headings so authors copy them
if [[ -f research/NOTE.template.md ]]; then
  for heading in "## Sources" "## Confidence"; do
    if ! grep -qF "$heading" research/NOTE.template.md; then
      fail "research/NOTE.template.md missing $heading"
    fi
  done
fi
ok "shape checks"

# 2. Placeholder scan on non-template research files
ok "placeholder scan (merged into shape)"

# 3–4. Source ledger and internal links (full mode)
if [[ "$FULL" -eq 1 ]]; then
  if [[ ! -f research/source-ledger.md ]]; then
    fail "missing research/source-ledger.md"
  else
    ok "source-ledger present"
  fi
  if [[ ! -f research/question-bank.md ]]; then
    fail "missing research/question-bank.md"
  else
    # Every Q-ID line like | Q1 | should have owner+status columns non-empty — light check
    if ! grep -qE '^\| Q[0-9]+ ' research/question-bank.md; then
      fail "question-bank.md has no Q-ID rows"
    else
      ok "question-bank has Q-IDs"
    fi
  fi
  if [[ ! -f research/DECISION_REGISTER.md ]]; then
    fail "missing research/DECISION_REGISTER.md"
  else
    if ! grep -qE '^\| D[0-9]+ ' research/DECISION_REGISTER.md; then
      fail "DECISION_REGISTER.md has no D-ID rows"
    else
      ok "decision register has D-IDs"
    fi
  fi

  # Internal relative links that look like markdown links to repo paths
  while IFS= read -r link; do
    # strip leading ./
    target="${link#./}"
    # ignore absolute http(s) and anchors-only
    if [[ "$target" == http* ]] || [[ "$target" == \#* ]] || [[ -z "$target" ]]; then
      continue
    fi
    # strip anchor
    target="${target%%#*}"
    if [[ -n "$target" && ! -e "$target" ]]; then
      # also try relative to file's dir — skip complex cases; flag only root-relative
      if [[ "$link" == /* ]] || [[ "$link" == research/* ]] || [[ "$link" == docs/* ]] || [[ "$link" == scripts/* ]]; then
        fail "broken link target: $link"
      fi
    fi
  done < <(grep -hoR '\[[^]]*\](\([^)]*\))' research docs/EXTENSIVE.md README.md 2>/dev/null | sed -n 's/.*](\([^)]*\)).*/\1/p' || true)
  ok "internal link scan (best-effort)"
fi

# 5–6. Copyright guard: fail on long attributed book quotes (heuristic)
# Look for "Book:" attributions followed by long quoted blocks — simple heuristic: lines with >25 words in quotes attributed to a textbook
for f in research/notes/*.md research/synthesis/*.md; do
  [[ -f "$f" ]] || continue
  # Heuristic: "verbatim from" or "quoted from" plus a long quote
  if grep -qiE 'verbatim from (the )?(book|textbook)|quoted from .*chapter' "$f"; then
    fail "$f may contain verbatim book text (matched attribution phrase)"
  fi
done
ok "copyright guard (heuristic)"

# 7. Anti-PRD guard on all synthesis memos
shopt -s nullglob
SYNTH=(research/synthesis/*.md)
if [[ ${#SYNTH[@]} -eq 0 ]]; then
  ok "anti-PRD guard (no synthesis memos)"
else
  for f in "${SYNTH[@]}"; do
    if grep -nE "$PRD_RE" "$f" >/dev/null 2>&1; then
      fail "$f looks like PRD language: $(grep -nE "$PRD_RE" "$f" | head -3 | tr '\n' ' ')"
    fi
    if grep -qiE '^#+ (functional )?requirements|^#+ must ship|^#+ non-functional' "$f"; then
      fail "$f contains requirements-style headings"
    fi
  done
  ok "anti-PRD guard"
fi

# 8. README guard (when both exist)
if [[ -f README.md && -f docs/EXTENSIVE.md ]]; then
  if ! grep -q 'docs/EXTENSIVE.md' README.md; then
    fail "README.md missing extensive banner link to docs/EXTENSIVE.md"
  fi
  if ! grep -qiE 'Future advancements|## Future' README.md; then
    fail "README.md missing Future advancements section"
  fi
  # path existence for research/ links in EXTENSIVE
  while IFS= read -r p; do
    p="${p#\`}"
    p="${p%\`}"
    if [[ "$p" == research/* ]] && [[ ! -e "$p" ]]; then
      fail "docs/EXTENSIVE.md references missing path: $p"
    fi
  done < <(grep -oE '`research/[^`]+`' docs/EXTENSIVE.md || true)
  # product-landing language
  if grep -qiE 'install now|get started in 30 seconds|⭐|badges? first' README.md; then
    fail "README.md has product-landing language"
  fi
  ok "README guard"
elif [[ -f README.md ]]; then
  # After Phase F both should exist; before that, soft skip
  ok "README guard (extensive not yet present — skipped)"
else
  ok "README guard (not yet present)"
fi

# 9. Summary
if [[ "$FAIL" -ne 0 ]]; then
  echo "=== RESULT: FAIL ==="
  exit 1
fi
echo "=== RESULT: PASS ==="
exit 0
