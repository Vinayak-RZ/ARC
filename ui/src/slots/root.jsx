import { register } from "./registry.js";
import { AppShell } from "../shell/AppShell.jsx";
import { Canvas } from "./canvas/Canvas.jsx";
import { Inspector } from "./canvas/Inspector.jsx";
import { Library } from "./library.jsx";
import { VisualGallery } from "./gallery.jsx";
import { ControlStudio } from "./control_studio/ControlStudio.jsx";
import { buildAnswerRows, verificationNote } from "../formatAnswer.js";
import { AnswerLine } from "../components/AnswerLine.jsx";
import { displayTitle } from "../runDisplay.js";
import { useRun } from "../hooks/useRun.js";

function parseEvid(summary) {
  if (!summary) return {};
  try {
    return JSON.parse(summary);
  } catch {
    return {};
  }
}

function Result({ id }) {
  const { data, error } = useRun(id);
  const evid = parseEvid(data?.summary || "");
  const unchecked = evid.unchecked === true || evid.token === "unchecked";
  const title = displayTitle({
    title: data?.title || evid.title,
    id,
    recipe_id: evid.recipe_id,
  });
  const state = error ? "failed" : data?.state || "Working";
  const loading = !data && !error;
  const live =
    state === "waiting-human"
      ? "Waiting for topology confirm"
      : state === "failed"
        ? "Run failed to load."
        : state === "Working"
          ? "Working"
          : "";
  const { rows } = buildAnswerRows(evid, data);
  const verifierRaw = evid.verifier ? String(evid.verifier) : "";
  const note = verificationNote({ unchecked: error ? false : unchecked, error, verifierRaw, evid });
  if (loading) {
    return <p className="loading-block" aria-live="polite">Loading run…</p>;
  }
  return (
    <article className="answer-card" aria-live="polite">
      <h1>{error ? id : title || "Problem"}</h1>
      {error ? (
        <p className="answer-value">Run unavailable</p>
      ) : unchecked && rows.length === 0 ? (
        <p className="answer-value">Pending verification</p>
      ) : rows.length > 1 ? (
        <div className="answer-lines">
          {rows.map((row) => (
            <AnswerLine key={row.name} parts={row} checked={!unchecked} />
          ))}
        </div>
      ) : rows.length === 1 ? (
        <AnswerLine parts={rows[0]} checked={!unchecked && !error} />
      ) : (
        <p className="answer-line">Working…</p>
      )}
      <div className="answer-status-row">
        {error ? (
          <span className="status-badge failed">Failed</span>
        ) : unchecked ? (
          <span className="status-badge unchecked">Unchecked</span>
        ) : (
          <span className="status-badge checked">Checked</span>
        )}
        <p className="status-hint">{note}</p>
      </div>
      {live ? <p className="hint">{live}</p> : null}
    </article>
  );
}

function CanvasStub({ id }) {
  return <Canvas id={id} />;
}

function InspectorSlot() {
  return <Inspector />;
}

function Argument({ id }) {
  const { data, error } = useRun(id);
  const text = data?.argument || "";
  return (
    <section className="argument">
      <h2>Explanation</h2>
      {error ? <p className="failed">unavailable</p> : null}
      {!error && !text ? <p className="empty">No explanation yet.</p> : null}
      {text ? <div className="prose">{text}</div> : null}
    </section>
  );
}

function More({ id }) {
  const { data, error } = useRun(id);
  if (error || !data) return null;
  const excerpt = data.observation_excerpt || {};
  const spans = Array.isArray(data.trace_excerpt) ? data.trace_excerpt : [];
  return (
    <div className="disclosures diagnostics-panel">
      <details>
        <summary>Run id</summary>
        <p className="hint">
          <code>{id}</code>
        </p>
      </details>
      <details>
        <summary>Observation</summary>
        <dl className="obs-excerpt">
          <div>
            <dt>unchecked</dt>
            <dd>
              <code>{excerpt.unchecked ? String(excerpt.token || "unchecked") : "false"}</code>
            </dd>
          </div>
          {excerpt.unchecked_reason ? (
            <div>
              <dt>unchecked_reason</dt>
              <dd>
                <code>{excerpt.unchecked_reason}</code>
              </dd>
            </div>
          ) : null}
          <div>
            <dt>capabilities</dt>
            <dd>{(excerpt.capabilities || []).join(", ") || "—"}</dd>
          </div>
          <div>
            <dt>providers</dt>
            <dd>{(excerpt.providers || []).join(", ") || "—"}</dd>
          </div>
          <div>
            <dt>retrieve.empty</dt>
            <dd>{excerpt.retrieve_empty ? "true" : "false"}</dd>
          </div>
        </dl>
        <details>
          <summary>Raw observation JSON</summary>
          <pre className="number-display">{data.observation || ""}</pre>
        </details>
      </details>
      <details>
        <summary>Trace</summary>
        {spans.length === 0 ? (
          <p className="empty">No trace.jsonl for this run.</p>
        ) : (
          <ol className="trace-list">
            {spans.map((span, idx) => (
              <li key={`${span.name}-${idx}`}>
                <code>{span.name}</code>
                {span.node_id ? <span className="hint"> {span.node_id}</span> : null}
                {span.duration_ms != null ? (
                  <span className="hint"> {Number(span.duration_ms).toFixed(1)}ms</span>
                ) : null}
                {span.unchecked ? <span className="badge-pill">unchecked</span> : null}
              </li>
            ))}
          </ol>
        )}
      </details>
      <details>
        <summary>Evidentiary JSON</summary>
        <pre className="number-display">{data.evidentiary || ""}</pre>
      </details>
      <details>
        <summary>Plan</summary>
        {data.plan ? <pre className="number-display">{data.plan}</pre> : <p className="empty">No plan yet.</p>}
      </details>
      <details>
        <summary>Raw graph</summary>
        <pre className="number-display">{JSON.stringify(data.graph || {}, null, 2)}</pre>
      </details>
      <details>
        <summary>Artifacts</summary>
        <p className="hint">Library SVG/PNG from this run only.</p>
        <img className="plot" alt={`Run ${id} artifact`} src={`/api/runs/${id}/artifact.svg`} width="200" height="80" />
      </details>
    </div>
  );
}

function Root() {
  return <AppShell />;
}

register("root", Root);
register("run.result", Result);
register("run.canvas", CanvasStub);
register("run.inspector", InspectorSlot);
register("run.argument", Argument);
register("run.more", More);
register("photo.confirm", function PhotoConfirm() {
  return null;
});
register("rag.inventory", Library);
register("visual.gallery", VisualGallery);
register("control.studio", ControlStudio);
