import { useEffect, useMemo, useState } from "react";
import { BookMarked, Compass } from "lucide-react";
import { useCurriculum, useAchievements } from "../hooks/useLearn.js";
import { MascotState } from "../components/MascotState.jsx";
import { ArcMascot } from "../mascot/index.js";

export function LearnPage({ onOpenSubject, onOpenAchievements }) {
  const { data, error, loading, reload } = useCurriculum();
  const { data: ach } = useAchievements();
  const current = data?.current_semester ?? 5;
  const [sem, setSem] = useState(null);
  useEffect(() => {
    if (data && sem == null) setSem(data.current_semester);
  }, [data, sem]);
  const semester = useMemo(
    () => (data?.semesters || []).find((s) => s.n === sem) || null,
    [data, sem],
  );
  const recentBadges = useMemo(() => {
    const list = (ach?.achievements || []).filter((a) => a.unlocked_at);
    list.sort((a, b) => String(b.unlocked_at).localeCompare(String(a.unlocked_at)));
    return list.slice(0, 4);
  }, [ach]);

  if (loading) {
    return (
      <div className="learn-page">
        <div className="shimmer learn-shimmer" aria-busy="true" />
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="learn-page">
        <MascotState kind="error" title="Could not load curriculum" actionLabel="Retry" onAction={reload} />
      </div>
    );
  }

  return (
    <div className="learn-page">
      <header className="page-header learn-header">
        <div>
          <h1>Learn</h1>
          <p className="home-lede">Your degree, semester by semester</p>
        </div>
        <ArcMascot className="page-mascot" size={48} mode="ambient" live label="" />
      </header>

      <section className="learn-achievements-strip" aria-label="Recent achievements">
        {recentBadges.length ? (
          <ul className="learn-badge-row">
            {recentBadges.map((b) => (
              <li key={b.id} className="learn-badge">
                <span className="learn-badge-title">{b.title}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="hint">Solve a problem or mark a topic done to unlock achievements.</p>
        )}
        <button type="button" className="button-secondary" onClick={onOpenAchievements}>
          View all
        </button>
      </section>

      <div
        className="learn-semester-rail"
        role="tablist"
        aria-label="Semesters"
        onKeyDown={(e) => {
          if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
          e.preventDefault();
          const next = e.key === "ArrowRight" ? Math.min(8, sem + 1) : Math.max(1, sem - 1);
          setSem(next);
        }}
      >
        {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
          <button
            key={n}
            type="button"
            role="tab"
            aria-selected={sem === n}
            tabIndex={sem === n ? 0 : -1}
            className={sem === n ? "chip is-pressed" : "chip"}
            onClick={() => setSem(n)}
          >
            S{n}
            {n === current ? <span className="learn-now">Now</span> : null}
          </button>
        ))}
      </div>

      {!semester?.subjects?.length ? (
        <p className="hint">No subjects listed for this semester.</p>
      ) : (
        <div className="learn-subject-grid">
          {semester.subjects.map((subj) => (
            <button
              key={subj.id}
              type="button"
              className="learn-subject-card"
              onClick={() => onOpenSubject(subj.id)}
            >
              <span className="learn-code-label">
                {subj.code || "No course code"}
              </span>
              <strong className="learn-subject-title">{subj.title}</strong>
              {subj.pack ? <span className="tag copper">{subj.pack}</span> : null}
              <span className={subj.source === "provided" ? "learn-source provided" : "learn-source inferred"}>
                {subj.source === "provided" ? (
                  <>
                    <BookMarked size={14} strokeWidth={1.5} aria-hidden /> Your notes
                  </>
                ) : (
                  <>
                    <Compass size={14} strokeWidth={1.5} aria-hidden /> Inferred syllabus
                  </>
                )}
              </span>
              <div className="learn-progress">
                <div
                  className="learn-progress-bar"
                  role="progressbar"
                  aria-valuenow={subj.progress?.done || 0}
                  aria-valuemin={0}
                  aria-valuemax={subj.progress?.total || 0}
                >
                  <span
                    style={{
                      width:
                        subj.progress?.total > 0
                          ? `${(100 * subj.progress.done) / subj.progress.total}%`
                          : "0%",
                    }}
                  />
                </div>
                <span className="hint">
                  {subj.progress?.done || 0} / {subj.progress?.total || 0} topics
                </span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
