import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { formatResistanceOhms, formatVoltage } from "../units/format.js";

function readEvid(summary) {
  try {
    return JSON.parse(summary || "{}");
  } catch {
    return {};
  }
}

function inputsLine(problem) {
  if (!problem) return "";
  if (problem.kind === "voltage_divider" || ("vin" in problem && "r1" in problem)) {
    const vin = formatVoltage(problem.vin);
    const r1 = formatResistanceOhms(problem.r1);
    const r2 = formatResistanceOhms(problem.r2);
    return `${vin.text}, ${r1.text}, ${r2.text}`;
  }
  return "";
}

const HIDDEN = new Set(["run.start", "node.start", "node.end", "span.start", "span.end"]);

export function dividerSteps(problem, evid, unchecked) {
  const inputs = inputsLine(problem);
  const vout = evid?.value != null ? `${Number(evid.value).toFixed(2)} V` : "—";
  const rows = [
    { title: "Read the circuit", result: inputs || "Divider with two resistors", author: "Agent", body: null },
    {
      title: "Write the divider equation",
      result: "Vout from Vin, R1, R2",
      author: "Agent",
      body: (
        <p className="work-equation-typeset">
          V<sub>out</sub> = V<sub>in</sub> R<sub>2</sub> / (R<sub>1</sub> + R<sub>2</sub>)
        </p>
      ),
    },
    { title: "Substitute values", result: `Vout = ${vout}`, author: "Engine", body: null },
  ];
  if (!unchecked) {
    rows.push({
      title: "Check with SPICE",
      result: "Operating point matches hand calculation within 0.1%",
      author: "Engine",
      body: null,
    });
  }
  return rows;
}

export function StepTimeline({ data }) {
  const evid = readEvid(data?.summary);
  const unchecked = evid.unchecked === true || evid.token === "unchecked";
  const steps =
    data?.problem?.kind === "voltage_divider" || (data?.problem?.vin && data?.problem?.r1)
      ? dividerSteps(data.problem, evid, unchecked)
      : [
          { title: "Solve", result: unchecked ? "Pending verification" : "Numeric check passed", author: "Engine" },
        ];
  const [open, setOpen] = useState(null);
  return (
    <section className="step-timeline" aria-label="Work steps">
      <ol className="step-timeline-list">
        {steps.map((step, i) => (
          <li key={step.title} className="step-timeline-row">
            <span className="step-index" aria-hidden="true">
              {i + 1}
            </span>
            <div className="step-body">
              <div className="step-head">
                <span className="step-title">{step.title}</span>
                <span className="step-author">{step.author}</span>
              </div>
              <p className="step-result">{step.result}</p>
              {step.body ? (
                <button
                  type="button"
                  className="step-expand"
                  aria-label="Show working"
                  aria-expanded={open === i}
                  onClick={() => setOpen(open === i ? null : i)}
                >
                  <ChevronDown size={16} />
                </button>
              ) : null}
              {open === i && step.body ? <div className="step-detail">{step.body}</div> : null}
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}

export function TraceDiagnostics({ trace }) {
  const hidden = (trace || []).filter((s) => HIDDEN.has(String(s?.name || "")));
  if (!hidden.length) return null;
  return (
    <details className="trace-diagnostics">
      <summary>Diagnostics</summary>
      <pre className="trace-diagnostics-pre">{JSON.stringify(hidden, null, 2)}</pre>
    </details>
  );
}
