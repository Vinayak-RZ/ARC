import { useEffect, useState } from "react";

export function useRun(id) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!id) {
      setData(null);
      setError("");
      return;
    }
    fetch(`/api/runs/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then((d) => {
        setData(d);
        setError("");
      })
      .catch(() => {
        setData(null);
        setError("failed");
      });
  }, [id]);
  return { data, error };
}

export function useRunsList() {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [seeding, setSeeding] = useState(false);

  function reload() {
    setLoading(true);
    setError(false);
    return fetch("/api/runs")
      .then((r) => {
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then((d) => {
        setRuns(d.runs || []);
        setSeeding(Boolean(d.seeding));
      })
      .catch(() => {
        setRuns([]);
        setError(true);
        setSeeding(false);
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    reload();
  }, []);

  useEffect(() => {
    if (!seeding) return undefined;
    const t = setInterval(() => {
      fetch("/api/runs")
        .then((r) => (r.ok ? r.json() : Promise.reject()))
        .then((d) => {
          setRuns(d.runs || []);
          setSeeding(Boolean(d.seeding));
        })
        .catch(() => {});
    }, 1500);
    return () => clearInterval(t);
  }, [seeding]);

  return { runs, loading, error, reload, seeding };
}
