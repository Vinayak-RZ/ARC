export function ResultsDock({ sessionId, results, margins }) {
  if (!results) {
    return (
      <footer className="studio-results empty">
        <p className="hint">Run Simulate to populate step, Bode, and root locus plots.</p>
      </footer>
    );
  }
  const sid = sessionId;
  const ts = results.ts || Date.now();
  return (
    <footer className="studio-results" aria-label="Simulation results">
      <h3>Results</h3>
      {margins ? (
        <p className="studio-margin-line">
          GM {margins.gain_margin_db != null ? `${margins.gain_margin_db.toFixed(2)} dB` : "—"} · PM{" "}
          {margins.phase_margin_deg != null ? `${margins.phase_margin_deg.toFixed(1)}°` : "—"} · ωcg{" "}
          {margins.gain_crossover_rad_s != null ? `${margins.gain_crossover_rad_s.toFixed(2)} rad/s` : "—"} · ωcp{" "}
          {margins.phase_crossover_rad_s != null ? `${margins.phase_crossover_rad_s.toFixed(2)} rad/s` : "—"}
        </p>
      ) : null}
      <div className="studio-results-grid">
        {results.step ? (
          <figure>
            <img src={`${results.step}?t=${ts}`} alt="Step response" loading="lazy" />
            <figcaption>Step</figcaption>
          </figure>
        ) : null}
        {results.bode ? (
          <figure>
            <img src={`${results.bode}?t=${ts}`} alt="Bode with margins" loading="lazy" />
            <figcaption>Bode</figcaption>
          </figure>
        ) : null}
        {results.rlocus ? (
          <figure>
            <img src={`${results.rlocus}?t=${ts}`} alt="Root locus" loading="lazy" />
            <figcaption>Root locus</figcaption>
          </figure>
        ) : null}
      </div>
    </footer>
  );
}
