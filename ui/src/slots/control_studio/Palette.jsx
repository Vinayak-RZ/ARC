import { useMemo, useState } from "react";
import {
  Activity,
  FunctionSquare,
  PlusCircle,
  Sigma,
  SlidersHorizontal,
  Triangle,
} from "lucide-react";

const ICONS = {
  gain: Triangle,
  sum: PlusCircle,
  transfer: FunctionSquare,
  pid: SlidersHorizontal,
  integrator: Sigma,
  derivative: Activity,
};

export function StudioPalette({ groups, onDragStart }) {
  const [q, setQ] = useState("");
  const items = useMemo(
    () => (groups || []).flatMap((g) => (g.items || []).map((item) => ({ ...item, group: g.label }))),
    [groups],
  );
  const filtered = useMemo(() => {
    const t = q.trim().toLowerCase();
    if (!t) return items;
    return items.filter((i) => i.label.toLowerCase().includes(t) || i.type.toLowerCase().includes(t));
  }, [items, q]);
  return (
    <aside className="studio-palette studio-palette-pane" aria-label="Block palette">
      <input
        className="studio-palette-search"
        type="search"
        placeholder="Search blocks"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />
      <ul className="studio-palette-rows">
        {filtered.map((item) => {
          const Icon = ICONS[item.type] || FunctionSquare;
          return (
            <li key={item.type}>
              <button
                type="button"
                className="studio-palette-row"
                draggable
                aria-label={item.label}
                onDragStart={(e) => {
                  e.dataTransfer.setData("application/control-studio-block", JSON.stringify(item));
                  e.dataTransfer.effectAllowed = "copy";
                  onDragStart?.(item);
                }}
              >
                <Icon size={18} strokeWidth={1.5} />
                <span>{item.label}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
