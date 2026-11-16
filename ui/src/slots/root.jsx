import { lazy, Suspense } from "react";
import { register } from "./registry.js";
import { AppShell } from "../shell/AppShell.jsx";
import { Inspector } from "./canvas/Inspector.jsx";

const Canvas = lazy(() => import("./canvas/Canvas.jsx").then((m) => ({ default: m.Canvas })));
const Library = lazy(() => import("./library.jsx").then((m) => ({ default: m.Library })));
const VisualGallery = lazy(() => import("./gallery.jsx").then((m) => ({ default: m.VisualGallery })));
const ControlStudio = lazy(() =>
  import("./control_studio/ControlStudio.jsx").then((m) => ({ default: m.ControlStudio })),
);

function slot(Component) {
  return function LazySlot(props) {
    return (
      <Suspense fallback={null}>
        <Component {...props} />
      </Suspense>
    );
  };
}
import { buildAnswerRows, verificationNote } from "../formatAnswer.js";
import { AnswerLine, VerificationStrip } from "../components/AnswerLine.jsx";
import { MascotState } from "../components/MascotState.jsx";
import { displayTitle } from "../runDisplay.js";
import { useRun } from "../hooks/useRun.js";
import { useLayout } from "../store.js";

function parseEvid(summary) {
  if (!summary) return {};
  try {
    return JSON.parse(summary);
  } catch {
    return {};
  }
}

function Result({ id }) {
  const stale = useLayout((s) => s.parametersStale);
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
  const derivedStale = data?.lab_verify?.derivation_matches_graph === false;
  const needsReview = Boolean(data?.lab_verify?.needs_review) && !derivedStale;
  const { rows } = buildAnswerRows(evid, data);
  const verifierRaw = evid.verifier ? String(evid.verifier) : "";
  const note = verificationNote({ unchecked: error ? false : unchecked, error, verifierRaw, evid });
  if (loading) {
    return (
      <MascotState kind="loading" title="Loading run…" message="Pulling evidence for this problem." size={56} />
    );
  }
  return (
    <article className={`answer-card${stale ? " is-stale" : ""}`} aria-live="polite">
      {error ? (
        <p className="answer-value">Run unavailable</p>
      ) : unchecked && rows.length === 0 ? (
        <p className="answer-value">Pending verification</p>
      ) : needsReview ? null : rows.length > 1 ? (
        <div className="answer-lines">
          {rows.map((row) => (
            <AnswerLine key={row.name} parts={row} checked={!unchecked} />
          ))}
        </div>
      ) : rows.length === 1 && rows[0].plain ? (
        <p className="answer-line tabular-nums">{rows[0].display}</p>
      ) : rows.length === 1 ? (
        <AnswerLine parts={rows[0]} checked={!unchecked && !error} />
      ) : needsReview ? null : (
        <p className="answer-line">Working…</p>
      )}
      {!error ? (
        <VerificationStrip
          checked={!unchecked && !data?.lab_verify?.needs_review}
          unchecked={unchecked}
          modifiedAt={data?.modified_at}
          stale={stale}
          needsReview={needsReview}
          reviewNote={data?.lab_verify?.status_label || data?.lab_verify?.disagreement_banner}
          note={(data?.work_steps || []).find((step) => step.title === "Check")?.result}
        />
      ) : (
        <p className="status-hint">{note}</p>
      )}
      {live ? <p className="hint">{live}</p> : null}
    </article>
  );
}

function CanvasStub({ id }) {
  return (
    <Suspense fallback={null}>
      <Canvas id={id} />
    </Suspense>
  );
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

function ActivityFeed({ rows }) {
  if (!rows?.length) return null;
  return (
    <table className="data-table activity-feed">
      <thead>
        <tr>
          <th>Step</th>
          <th>What ran</th>
          <th>Status</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => {
          const status = row.unchecked ? "Unchecked" : row.ok === false ? "Failed" : "Done";
          const ms = row.duration_ms == null ? "—" : `${Number(row.duration_ms).toFixed(0)} ms`;
          return (
            <tr key={`${row.node}-${i}`}>
              <td>{i + 1}</td>
              <td>{row.role || row.node}</td>
              <td>{status}</td>
              <td className="tabular-nums">{ms}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

function More({ id }) {
  const { data, error } = useRun(id);
  if (error || !data) return null;
  const excerpt = data.observation_excerpt || {};
  const spans = Array.isArray(data.trace_excerpt) ? data.trace_excerpt : [];
  const feed = Array.isArray(data.activity_feed) ? data.activity_feed : [];
  return (
    <div className="disclosures diagnostics-panel">
      <ActivityFeed rows={feed} />
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
      {data.plan ? (
        <details>
          <summary>Plan</summary>
          <pre className="number-display">{data.plan}</pre>
        </details>
      ) : null}
      {data.graph && Object.keys(data.graph).length ? (
        <details>
          <summary>Raw graph</summary>
          <pre className="number-display">{JSON.stringify(data.graph, null, 2)}</pre>
        </details>
      ) : null}
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
register("rag.inventory", slot(Library));
register("visual.gallery", slot(VisualGallery));
register("control.studio", slot(ControlStudio));
