import { useEffect, useMemo, useState } from "react";

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

export function Library() {
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

  const books = useMemo(() => bookIds(items), [items]);

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
    const q = new URLSearchParams({
      rights: "true",
      filename: file.name,
      book_id: bid,
      chapter_id: chapter,
      domain_tag: domain,
      licence_tag: licence,
      folder_tag: folder,
    });
    try {
      const r = await fetch(`/api/rag/upload?${q}`, { method: "POST", body: file });
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
    <section className="library" aria-labelledby="library-title">
      <h1 id="library-title">Books</h1>
      <p className="hint">
        Add a PDF you have rights to; it stays on this machine. Tagged books become available to retrieve.
      </p>
      {loading ? <p className="hint">Loading books.</p> : null}
      {!loading && items.length === 0 ? (
        <p className="empty">No books yet. Add a PDF you have rights to; it stays on this machine.</p>
      ) : null}
      {items.length ? (
        <ul className="book-list">
          {books.map((id) => {
            const rows = items.filter((row) => row.book_id === id);
            const sample = rows[0] || {};
            return (
              <li key={id}>
                <strong>{id}</strong>
                <span className="hint">
                  {sample.licence_tag || "untagged"} · {rows.length} chunk{rows.length === 1 ? "" : "s"}
                </span>
              </li>
            );
          })}
        </ul>
      ) : null}
      <form className="library-form" onSubmit={ingest}>
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
          <input
            type="file"
            accept=".pdf,.md,.txt,application/pdf,text/markdown,text/plain"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
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
          <input type="checkbox" checked={rights} onChange={(e) => setRights(e.target.checked)} />
          I have rights to this file. Do not upload a commercial textbook into git.
        </label>
        <button className="button-primary" type="submit" disabled={!rights}>
          Ingest
        </button>
        {error ? <p className="error-text">{error}</p> : null}
        {status ? <p className="hint">{status}</p> : null}
      </form>
    </section>
  );
}
