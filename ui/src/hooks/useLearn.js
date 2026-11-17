import { useCallback, useEffect, useState } from "react";

export function useCurriculum() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const reload = useCallback(() => {
    setLoading(true);
    fetch("/api/learn/curriculum")
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
      })
      .finally(() => setLoading(false));
  }, []);
  useEffect(() => {
    reload();
  }, [reload]);
  return { data, error, loading, reload };
}

export function useAchievements() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const reload = useCallback(() => {
    fetch("/api/learn/achievements")
      .then((r) => {
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then((d) => {
        setData(d);
        setError("");
        if (d.newly_unlocked?.length) {
          const byId = Object.fromEntries((d.achievements || []).map((a) => [a.id, a.title || a.id]));
          const titles = d.newly_unlocked.map((id) => byId[id] || String(id).replace(/-/g, " "));
          window.dispatchEvent(new CustomEvent("arc:achievements", { detail: titles }));
        }
      })
      .catch(() => {
        setData(null);
        setError("failed");
      });
  }, []);
  useEffect(() => {
    reload();
  }, [reload]);
  return { data, error, reload };
}

export function postProgress(body) {
  return fetch("/api/learn/progress", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then((r) => {
    if (!r.ok) throw new Error("failed");
    return r.json();
  });
}

export function tryRecipe(recipeId) {
  return fetch(`/api/learn/recipes/${encodeURIComponent(recipeId)}/try`, {
    method: "POST",
  }).then((r) => {
    if (!r.ok) throw new Error("failed");
    return r.json();
  });
}
