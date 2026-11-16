import { useEffect, useMemo, useState } from "react";
import { MascotState } from "../components/MascotState.jsx";
import { packLabel } from "../lib/packLabels.js";

const DOMAINS = [
  "circuits",
  "signals",
  "electronics",
  "machines",
  "power",
  "control",
  "power_electronics",
  "measurements",
  "em",
  "maths",
];
const LICENCES = ["CC-BY", "commercial-byo", "unknown"];
const NEW_BOOK = "__new__";

function bookIds(items) {
  return [...new Set((items || []).map((row) => row.book_id).filter(Boolean))];
}

function ReferenceTab() {
  const [domains, setDomains] = useState([]);
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch("/api/reference")
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((d) => setDomains(d.domains || []))
      .catch(() => setError("Could not load the reference catalog."))
      .finally(() => setLoading(false));
  }, []);

  async function search(ev) {
    ev?.preventDefault();
    setError("");
    const query = q.trim();
    if (!query) {
      setResults([]);
      return;
    }
    try {
      const r = await fetch(`/api/reference?q=${encodeURIComponent(query)}`);
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || "search");
      setResults(body.results || []);
    } catch (exc) {
      setError(exc.message || "Search failed.");
    }
  }

  async function openRecord(id) {
    setError("");
    try {
      const r = await fetch(`/api/reference/${encodeURIComponent(id)}`);
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || "missing");
      setSelected(body.record);
    } catch (exc) {
      setError(exc.message || "Could not open record.");
    }
  }

  if (loading) {
    return <MascotState kind="loading" size={56} title="Loading reference…" message="Bundled NEC/IEEE tables and course data." />;
  }
  if (error && !domains.length) {
    return <MascotState kind="error" title="Reference unavailable" message={error} />;
  }

  return (
    <div className="library-reference">
      <p className="hint">Curated open tables shipped with Arc. Search by title, alias, or id.</p>
      <form className="library-ref-search" onSubmit={search}>
        <input className="run-search" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="e.g. AWG 12 ampacity" aria-label="Search reference" />
        <button type="submit" className="button-primary button-compact">
          Search
        </button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="library-domain-chips" role="list">
        {domains.map((d) => (
          <button
            key={d.id}
            type="button"
            className="gallery-filter-chip"
            role="listitem"
            onClick={() => {
              setQ(d.id);
              setTimeout(() => search({ preventDefault() {} }), 0);
            }}
          >
            {packLabel(d.id)} · {d.count}
          </button>
        ))}
      </div>
      <ul className="library-ref-results">
        {results.map((row) => (
          <li key={row.id}>
            <button type="button" className="library-ref-hit" onClick={() => openRecord(row.id)}>
              <strong>{row.title}</strong>
              <span className="hint">
                {row.domain} · {row.id}
              </span>
            </button>
          </li>
        ))}
      </ul>
      {selected ? (
        <article className="library-ref-detail card-surface">
          <h3>{selected.title}</h3>
          <p className="hint">
            {selected.domain} · {selected.id}
          </p>
          <pre className="number-display">{JSON.stringify(selected.values, null, 2)}</pre>
          <p className="hint">
            {selected.source?.title} {selected.source?.edition} §{selected.source?.clause}
          </p>
        </article>
      ) : null}
    </div>
  );
}

function BooksTab() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [bookId, setBookId] = useState("");
  const [newBook, setNewBook] = useState("");
  const [chapter, setChapter] = useState("");
  const [domain, setDomain] = useState("circuits");
  const [licence, setLicence] = useState("commercial-byo");
  const [folder, setFolder] = useState("");
  const [rights, setRights] = useState(false);
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [filterBook, setFilterBook] = useState("");
  const [hit, setHit] = useState(null);

  const books = useMemo(() => bookIds(items), [items]);
  const sourceRows = useMemo(() => {
    const byBook = new Map();
    for (const row of items) {
      const bid = row.book_id;
      if (!bid) continue;
      const prev = byBook.get(bid);
      const chapters = new Set(prev?.chapters || []);
      if (row.chapter_id) chapters.add(row.chapter_id);
      byBook.set(bid, {
        book_id: bid,
        licence_tag: row.licence_tag,
        domain_tag: row.domain_tag,
        chapters,
        count: (prev?.count || 0) + 1,
      });
    }
    return [...byBook.values()];
  }, [items]);

  function load() {
    setLoading(true);
    fetch("/api/rag/inventory")
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((d) => setItems(d.items || []))
      .catch(() => {
        setItems([]);
        setError("Could not load the book inventory.");
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  async function ingest(ev) {
    ev.preventDefault();
    setError("");
    setStatus("");
    if (!rights) {
      setError("Confirm you have rights to this file.");
      return;
    }
    if (!file) {
      setError("Choose a .pdf, .md, or .txt file.");
      return;
    }
    const bid = bookId === NEW_BOOK ? newBook : bookId;
    if (!bid) {
      setError("Pick an existing book or name a new one.");
      return;
    }
    const params = new URLSearchParams({
      rights: "true",
      filename: file.name,
      book_id: bid,
      chapter_id: chapter,
      domain_tag: domain,
      licence_tag: licence,
      folder_tag: folder,
    });
    try {
      const r = await fetch(`/api/rag/upload?${params}`, { method: "POST", body: file });
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || "upload");
      setStatus(`Ingested ${file.name} as ${bid}.`);
      setFile(null);
      load();
    } catch (exc) {
      setError(exc.message || "Could not ingest the file.");
    }
  }

  return (
    <div className="library-books">
      <p className="hint">Add textbooks and lab sheets you have rights to. They stay on this machine.</p>
      <div className="library-sources-toolbar">
        <input className="run-search" type="search" placeholder="Search sources" value={query} onChange={(e) => setQuery(e.target.value)} />
      </div>
      <table className="library-sources-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Kind</th>
            <th>Subject</th>
            <th>Used in</th>
          </tr>
        </thead>
        <tbody>
          {sourceRows
            .filter((row) => !query || String(row.book_id).toLowerCase().includes(query.toLowerCase()))
            .slice(0, 40)
            .map((row) => (
              <tr key={row.book_id}>
                <td>{row.book_id}</td>
                <td>{row.licence_tag === "commercial-byo" ? "Textbook" : row.licence_tag || "—"}</td>
                <td>{row.domain_tag || "—"}</td>
                <td>{[...row.chapters].join(", ") || `${row.count} chunk${row.count === 1 ? "" : "s"}`}</td>
              </tr>
            ))}
        </tbody>
      </table>
      {loading ? <p className="hint">Loading books.</p> : null}
      {!loading && items.length === 0 ? (
        <MascotState kind="empty" size={48} title="No books yet" message="Add a PDF you have rights to; it stays on this machine." />
      ) : null}
      <form className="library-form card-surface" onSubmit={ingest}>
        <h2>Add a book</h2>
        <label className="field">
          Book
          <select value={bookId} onChange={(e) => setBookId(e.target.value)} aria-label="Book">
            <option value="">Select a book</option>
            {books.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
            <option value={NEW_BOOK}>New book</option>
          </select>
        </label>
        {bookId === NEW_BOOK ? (
          <label className="field">
            New book id
            <input value={newBook} onChange={(e) => setNewBook(e.target.value)} />
          </label>
        ) : null}
        <label className="field">
          File
          <input type="file" accept=".pdf,.md,.txt,application/pdf,text/markdown,text/plain" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        </label>
        <label className="field">
          Chapter
          <input value={chapter} onChange={(e) => setChapter(e.target.value)} />
        </label>
        <label className="field">
          Domain
          <select value={domain} onChange={(e) => setDomain(e.target.value)} aria-label="Domain">
            {DOMAINS.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          Licence
          <select value={licence} onChange={(e) => setLicence(e.target.value)} aria-label="Licence">
            {LICENCES.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          Folder tag
          <input value={folder} onChange={(e) => setFolder(e.target.value)} />
        </label>
        <label className="rights">
          <input type="checkbox" checked={rights} onChange={(e) => setRights(e.target.checked)} />I have rights to this file. Do not upload a commercial textbook into git.
        </label>
        <button className="button-primary" type="submit" disabled={!rights}>
          Ingest
        </button>
        {error ? <p className="error-text">{error}</p> : null}
        {status ? <p className="hint">{status}</p> : null}
      </form>
      <form
        className="library-form card-surface"
        onSubmit={async (ev) => {
          ev.preventDefault();
          setError("");
          setHit(null);
          const q = query.trim();
          if (!q) {
            setError("Enter a retrieve query.");
            return;
          }
          const payload = { query: q };
          if (filterBook) payload.book_id = filterBook;
          try {
            const r = await fetch("/api/rag/query", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            });
            const body = await r.json();
            if (!r.ok) throw new Error(body.error || "query");
            setHit(body);
          } catch (exc) {
            setError(exc.message || "Could not retrieve.");
          }
        }}
      >
        <h2>Retrieve</h2>
        <label className="field">
          Query
          <input value={query} onChange={(e) => setQuery(e.target.value)} aria-label="Retrieve query" />
        </label>
        <label className="field">
          Filter book
          <select value={filterBook} onChange={(e) => setFilterBook(e.target.value)} aria-label="Filter book">
            <option value="">All books</option>
            {books.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </label>
        <button className="button-secondary" type="submit">
          Search tagged books
        </button>
        {hit?.empty ? <p className="empty">No passages for that query.</p> : null}
        {hit && !hit.empty
          ? (hit.passages || []).map((p, idx) => (
              <article key={p.node_id || idx} className="passage">
                <p className="hint">
                  {p.book_id || "unknown"} {p.chapter_id ? `ch ${p.chapter_id}` : ""} {p.page ? `p. ${p.page}` : ""}
                </p>
                <p className="prose">{p.text}</p>
              </article>
            ))
          : null}
      </form>
    </div>
  );
}

export function Library() {
  const [tab, setTab] = useState("reference");
  return (
    <section className="library" aria-labelledby="library-title">
      <h1 id="library-title">Library</h1>
      <div className="settings-tabs tabs-underline" role="tablist">
        <button type="button" role="tab" className="tab-underline" aria-selected={tab === "reference"} onClick={() => setTab("reference")}>
          Reference
        </button>
        <button type="button" role="tab" className="tab-underline" aria-selected={tab === "books"} onClick={() => setTab("books")}>
          Your books
        </button>
      </div>
      {tab === "reference" ? <ReferenceTab /> : <BooksTab />}
    </section>
  );
}
