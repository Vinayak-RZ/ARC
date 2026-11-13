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
  function reload() {
    setLoading(true);
    fetch("/api/runs")
      .then((r) => r.json())
      .then((d) => setRuns(d.runs || []))
      .catch(() => setRuns([]))
      .finally(() => setLoading(false));
  }
  useEffect(() => {
    reload();
  }, []);
  return { runs, loading, reload };
}
