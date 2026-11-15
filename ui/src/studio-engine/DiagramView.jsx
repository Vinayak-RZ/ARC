import { validateDiagram } from "./spec.js";
import { Schematic } from "./renderers/Schematic.jsx";
import { BlockDiagram } from "./renderers/BlockDiagram.jsx";
import { OneLine } from "./renderers/OneLine.jsx";
import { Waveform } from "./renderers/Waveform.jsx";

export function DiagramView({ diagram }) {
  const errors = validateDiagram(diagram || {});
  if (errors.length) {
    return (
      <div className="se-error" role="alert">
        <p>Invalid diagram</p>
        <ul>
          {errors.map((e) => (
            <li key={e}>{e}</li>
          ))}
        </ul>
      </div>
    );
  }
  return (
    <div className="se-diagram-view">
      {diagram.title ? <h3 className="se-diagram-title">{diagram.title}</h3> : null}
      {(diagram.panels || []).map((panel, i) => (
        <section key={i} className="se-panel">
          {panel.title ? <h4>{panel.title}</h4> : null}
          {panel.kind === "schematic" ? <Schematic panel={panel} /> : null}
          {panel.kind === "block" ? <BlockDiagram panel={panel} /> : null}
          {panel.kind === "oneline" ? <OneLine panel={panel} /> : null}
          {panel.kind === "waveform" ? <Waveform panel={panel} /> : null}
        </section>
      ))}
    </div>
  );
}
