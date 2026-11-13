import { subjectTag, displayTitle } from "../runDisplay.js";
import { relativeTime } from "../units/format.js";

export function ProblemHeader({ runMeta, data }) {
  const subject = runMeta?.subject || subjectTag(runMeta || {});
  const title = displayTitle(runMeta || { title: data?.title });
  const updated = relativeTime(runMeta?.modified_at);
  return (
    <header className="problem-header">
      <p className="problem-eyebrow">{subject.toUpperCase()}</p>
      <h1 className="problem-display-title">{title}</h1>
      <p className="problem-meta">
        Made by Agent · Updated {updated}
      </p>
    </header>
  );
}
