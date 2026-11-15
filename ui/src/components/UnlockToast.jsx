import { useEffect, useState } from "react";

export function UnlockToast() {
  const [queue, setQueue] = useState([]);
  const current = queue[0] || null;

  useEffect(() => {
    function onUnlock(e) {
      const ids = e.detail || [];
      if (!ids.length) return;
      setQueue((q) => [...q, ...ids]);
    }
    window.addEventListener("arc:achievements", onUnlock);
    return () => window.removeEventListener("arc:achievements", onUnlock);
  }, []);

  useEffect(() => {
    if (!current) return undefined;
    const t = window.setTimeout(() => setQueue((q) => q.slice(1)), 4000);
    return () => window.clearTimeout(t);
  }, [current]);

  if (!current) return null;
  return (
    <div className="learn-unlock-toast" role="status" aria-live="polite">
      Achievement unlocked: {current}
    </div>
  );
}
