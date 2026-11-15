import { useEffect, useMemo, useRef } from "react";
import {
  BadgeCheck,
  BookCheck,
  Compass,
  FlaskConical,
  GraduationCap,
  Layers,
  Trophy,
  X,
  Zap,
} from "lucide-react";
import { useAchievements } from "../hooks/useLearn.js";

const ICONS = {
  Zap,
  BadgeCheck,
  Layers,
  Compass,
  BookCheck,
  GraduationCap,
  Trophy,
  FlaskConical,
};

function groupOf(id) {
  if (id.startsWith("subject-complete:")) return "Subjects";
  if (id.startsWith("semester-complete:")) return "Semesters";
  if (id.startsWith("pack-first:")) return "Packs";
  return "General";
}

export function AchievementsPanel({ open, onClose }) {
  const { data, reload } = useAchievements();
  const closeRef = useRef(null);
  useEffect(() => {
    if (open) reload();
  }, [open, reload]);
  useEffect(() => {
    if (!open) return undefined;
    closeRef.current?.focus();
    function onKey(e) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const groups = useMemo(() => {
    const map = { General: [], Subjects: [], Semesters: [], Packs: [] };
    for (const a of data?.achievements || []) {
      map[groupOf(a.id)].push(a);
    }
    return map;
  }, [data]);

  if (!open) return null;

  return (
    <div className="learn-drawer-overlay" role="presentation" onClick={onClose}>
      <aside
        className="learn-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Achievements"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="learn-drawer-head">
          <h2>Achievements</h2>
          <button type="button" className="icon-btn" ref={closeRef} onClick={onClose} aria-label="Close">
            <X size={18} strokeWidth={1.5} />
          </button>
        </header>
        <div className="learn-drawer-body">
          {Object.entries(groups).map(([name, items]) =>
            items.length ? (
              <section key={name}>
                <h3 className="learn-code-label">{name}</h3>
                <ul className="learn-ach-grid">
                  {items.map((a) => {
                    const Icon = ICONS[a.icon] || Zap;
                    const unlocked = !!a.unlocked_at;
                    return (
                      <li key={a.id} className={unlocked ? "learn-ach unlocked" : "learn-ach locked"}>
                        <Icon size={20} strokeWidth={1.5} aria-hidden />
                        <strong>{a.title}</strong>
                        {unlocked ? (
                          <span className="hint">Unlocked {String(a.unlocked_at).slice(0, 10)}</span>
                        ) : (
                          <span className="hint">
                            {a.progress?.value ?? 0} / {a.progress?.target ?? 1}
                          </span>
                        )}
                        {!unlocked ? (
                          <div className="learn-progress-bar" aria-hidden>
                            <span
                              style={{
                                width:
                                  a.progress?.target > 0
                                    ? `${Math.min(100, (100 * (a.progress.value || 0)) / a.progress.target)}%`
                                    : "0%",
                              }}
                            />
                          </div>
                        ) : null}
                      </li>
                    );
                  })}
                </ul>
              </section>
            ) : null,
          )}
        </div>
      </aside>
    </div>
  );
}
