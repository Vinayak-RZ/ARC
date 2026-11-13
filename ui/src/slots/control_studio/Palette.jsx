export function StudioPalette({ groups, onDragStart }) {
  const items = (groups || []).flatMap((g) => (g.items || []).map((item) => ({ ...item, group: g.label })));
  return (
    <aside className="studio-palette studio-palette-icons" aria-label="Block palette">
      <ul className="studio-palette-icons-list">
        {items.map((item) => (
          <li key={item.type}>
            <button
              type="button"
              className="studio-palette-icon-btn"
              draggable
              title={`${item.label}${item.group ? ` (${item.group})` : ""}`}
              aria-label={item.label}
              onDragStart={(e) => {
                e.dataTransfer.setData("application/control-studio-block", JSON.stringify(item));
                e.dataTransfer.effectAllowed = "copy";
                onDragStart?.(item);
              }}
              onClick={() => onDragStart?.(item, { placeCenter: true })}
            >
              <span className="chip-icon" aria-hidden="true">
                {item.icon || "▣"}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
