import { useState } from "react";

export function StudioPalette({ groups, onDragStart }) {
  const [open, setOpen] = useState(() => new Set(["linear"]));
  function toggle(id) {
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }
  return (
    <aside className="studio-palette" aria-label="Block palette">
      {(groups || []).map((g) => (
        <details key={g.id} className="studio-palette-details" open={open.has(g.id)}>
          <summary
            onClick={(e) => {
              e.preventDefault();
              toggle(g.id);
            }}
          >
            {g.label}
          </summary>
          <div className="studio-palette-grid">
            {(g.items || []).map((item) => (
              <button
                key={item.type}
                type="button"
                className="studio-palette-chip-compact"
                draggable
                title={item.label}
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
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </details>
      ))}
    </aside>
  );
}
