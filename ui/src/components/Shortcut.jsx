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
    <span className="shortcut-kbd-row">
      {parts.map((part, i) => (
        <kbd key={`${part}-${i}`} className="shortcut-kbd">
          {part}
        </kbd>
      ))}
    </span>
  );
}
