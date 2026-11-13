const MAC =
  typeof navigator !== "undefined" && /Mac|iPhone|iPad|iPod/i.test(navigator.platform);

function formatToken(token) {
  const t = token.trim();
  if (!t) return "";
  const lower = t.toLowerCase();
  if (lower === "ctrl" || lower === "control" || t === "⌃") return MAC ? "⌘" : "Ctrl";
  if (lower === "cmd" || lower === "meta" || lower === "command") return "⌘";
  return t;
}

/** Renders a keyboard hint; Ctrl maps to ⌘ on macOS via navigator.platform. */
export function Shortcut({ keys }) {
  const parts = String(keys || "")
    .split(/\s+/)
    .filter(Boolean)
    .map(formatToken);
  return (
    <kbd className="shortcut-kbd">
      {parts.map((part, i) => (
        <span key={`${part}-${i}`}>
          {i > 0 ? " " : null}
          {part}
        </span>
      ))}
    </kbd>
  );
}
