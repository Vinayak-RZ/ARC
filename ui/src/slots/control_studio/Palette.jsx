export function StudioPalette({ groups, onDragStart }) {
  return (
    <aside className="studio-palette" aria-label="Block palette">
      {(groups || []).map((g) => (
        <section key={g.id} className="studio-palette-group">
          <h3 className="studio-palette-heading">{g.label}</h3>
          <ul className="studio-palette-list">
            {(g.items || []).map((item) => (
              <li key={item.type}>
                <button
                  type="button"
                  className="studio-palette-chip"
                  draggable
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
              </li>
            ))}
          </ul>
        </section>
      ))}
    </aside>
  );
}
