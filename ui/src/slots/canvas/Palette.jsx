import { PARTS } from "./graph.js";

const GROUPS = [
  { name: "Passives", types: ["resistor", "capacitor", "inductor"] },
  { name: "Sources", types: ["source_v", "source_i"] },
  { name: "Reference", types: ["ground"] },
];

export function Palette({ onAdd, disabled }) {
  return (
    <div className="palette" role="group" aria-label="Palette">
      {GROUPS.map((group) => (
        <div key={group.name} className="palette-group">
          <p className="palette-label">{group.name}</p>
          {group.types.map((type) => {
            const part = PARTS.find((p) => p.type === type);
            if (!part) return null;
            return (
              <button
                key={part.type}
                type="button"
                className="palette-btn"
                disabled={disabled}
                onClick={() => onAdd(part.type)}
              >
                {part.label}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}
