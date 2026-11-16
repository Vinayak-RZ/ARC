import { useEffect, useState } from "react";

export function UnlockToast() {
  const [queue, setQueue] = useState([]);
  const current = queue[0] || null;
  const [hover, setHover] = useState(false);

  useEffect(() => {
    function onUnlock(e) {
      const titles = e.detail || [];
      if (!titles.length) return;
      setQueue((q) => [...q, ...titles.map(String)]);
    }
    window.addEventListener("arc:achievements", onUnlock);
    return () => window.removeEventListener("arc:achievements", onUnlock);
  }, []);

  useEffect(() => {
    if (!current || hover) return undefined;
    const t = window.setTimeout(() => setQueue((q) => q.slice(1)), 6000);
    return () => window.clearTimeout(t);
  }, [current, hover]);

  if (!current) return null;
  return (
    <div
      className="learn-unlock-toast"
      role="status"
      aria-live="polite"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <span>Unlocked: {current}</span>
      <button type="button" className="learn-unlock-toast-close" aria-label="Dismiss" onClick={() => setQueue((q) => q.slice(1))}>
        ×
      </button>
    </div>
  );
}