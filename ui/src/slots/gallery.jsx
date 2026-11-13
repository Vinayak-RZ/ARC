import { useEffect, useState } from "react";

export function VisualGallery() {
  const [data, setData] = useState({ components: [], goldens_base: "" });
  useEffect(() => {
    fetch("/api/visual-kit")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData({ components: [], goldens_base: "" }));
  }, []);
  return (
    <section className="visual-gallery" aria-label="Arc Visual Kit gallery">
      <h2>Visual Kit</h2>
      <p className="muted">Engine-bound figures. Numbers come from Arc kernels, not prompts.</p>
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
