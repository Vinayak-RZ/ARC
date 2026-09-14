import { PARTS } from "./graph.js";

export function Palette({ onAdd, disabled }) {
  return (
    <div className="palette" role="group" aria-label="Palette">
      {PARTS.map((part) => (
        <button
          key={part.type}
          type="button"
          className="palette-btn"
          disabled={disabled}
          onClick={() => onAdd(part.type)}
        >
          {part.label}
        </button>
      ))}
    </div>
  );
}
