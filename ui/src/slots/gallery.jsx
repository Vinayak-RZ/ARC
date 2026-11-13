import { useEffect, useState } from "react";

export function VisualGallery() {
  const [data, setData] = useState({ components: [], goldens_base: "" });
  const [scorecard, setScorecard] = useState("");
  useEffect(() => {
    fetch("/api/visual-kit")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData({ components: [], goldens_base: "" }));
    fetch("/api/frontier/scorecard")
      .then((r) => r.json())
      .then((d) => setScorecard(d.markdown || ""))
      .catch(() => setScorecard(""));
  }, []);
  return (
    <section className="visual-gallery" aria-label="Arc Visual Kit gallery">
      <h1>Visuals</h1>
      <p className="visual-gallery-lede">Engine-bound figures from the Visual Kit. Numbers come from Arc kernels, not prompts.</p>
      {scorecard ? (
        <details className="scorecard-panel">
          <summary>Frontier scorecard (measured)</summary>
          <pre className="scorecard-md">{scorecard}</pre>
        </details>
      ) : null}
      <div className="gallery-grid">
        {(data.components || []).map((c) => (
          <figure key={c.id} className="gallery-card">
            <img src={`${data.goldens_base}${c.golden}`} alt={c.id} loading="lazy" />
            <figcaption>{c.id}</figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}
