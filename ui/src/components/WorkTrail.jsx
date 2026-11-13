function readEvid(summary) {
  try {
    return JSON.parse(summary || "{}");
  } catch {
    return {};
  }
}

function formatProblemInputs(problem) {
  if (!problem || typeof problem !== "object") return [];
  const kind = problem.kind || "";
  if (kind === "voltage_divider" || ("vin" in problem && "r1" in problem && "r2" in problem)) {
    return [
      { label: "Vin", value: problem.vin, unit: "V" },
      { label: "R1", value: problem.r1, unit: "Ω" },
      { label: "R2", value: problem.r2, unit: "Ω" },
    ];
  }
  if (kind === "ohms_law" || ("v" in problem && "r" in problem)) {
    return [
      { label: "V", value: problem.v, unit: "V" },
      { label: "R", value: problem.r, unit: "Ω" },
    ];
  }
  if (problem.prompt) {
    return [{ label: "Prompt", value: String(problem.prompt).slice(0, 120), unit: "" }];
  }
  return Object.entries(problem)
    .filter(([k]) => !["kind", "recipe_id"].includes(k))
    .slice(0, 6)
    .map(([k, v]) => ({ label: k, value: v, unit: "" }));
}

function traceSteps(trace, evid) {
  const steps = [];
  for (const span of trace || []) {
    const name = String(span?.name || "step");
    if (!name || name === "root") continue;
    const label = name.replace(/-/g, " ");
    let detail = "";
    if (span.node_id) detail = span.node_id;
    if (span.unchecked) detail = (detail ? `${detail} · ` : "") + "unchecked";
    else if (span.ok === true) detail = (detail ? `${detail} · ` : "") + "ok";
    steps.push({ title: label, detail });
  }
  if (steps.length === 0) {
    steps.push({
      title: "Algebraic check",
      detail: evid.recipe_id ? `Recipe ${evid.recipe_id}` : "Numeric kernel",
    });
    if (evid.verifier) steps.push({ title: "Verification", detail: String(evid.verifier) });
    if (evid.value != null) steps.push({ title: "Result", detail: `value = ${evid.value}` });
  }
  return steps;
}

export function WorkTrail({ data }) {
  const evid = readEvid(data?.summary);
  const inputs = formatProblemInputs(data?.problem);
  const steps = traceSteps(data?.trace_excerpt, evid);
  const equation =
    data?.problem?.kind === "voltage_divider"
      ? "Vout = Vin × R2 / (R1 + R2)"
      : data?.problem?.kind === "ohms_law"
        ? "I = V / R"
        : null;
  return (
    <section className="work-trail" aria-label="Work">
      <ol className="work-trail-list">
        <li className="work-trail-step">
          <span className="work-trail-title">Inputs</span>
          <ul className="work-inputs">
            {inputs.map((row) => (
              <li key={row.label}>
                {row.label} = {row.value}
                {row.unit ? ` ${row.unit}` : ""}
              </li>
            ))}
          </ul>
        </li>
        {equation ? (
          <li className="work-trail-step">
            <span className="work-trail-title">Equation</span>
            <p className="work-equation">{equation}</p>
          </li>
        ) : null}
        {steps.map((s, i) => (
          <li key={`${s.title}-${i}`} className="work-trail-step">
            <span className="work-trail-title">{s.title}</span>
            {s.detail ? <p className="hint">{s.detail}</p> : null}
          </li>
        ))}
      </ol>
      {data?.argument ? (
        <div className="work-prose">
          <h3>Explanation</h3>
          <pre className="work-argument">{data.argument}</pre>
        </div>
      ) : null}
    </section>
  );
}
