import { subjectTag, displayTitle } from "../runDisplay.js";
import { runHeadline } from "../formatAnswer.js";
import { relativeTime } from "../units/format.js";

export function ProblemHeader({ runMeta, data }) {
  const subject = runMeta?.subject || subjectTag(runMeta || {});
  const evid = (() => {
    try {
      return JSON.parse(data?.summary || "{}");
    } catch {
      return {};
    }
  })();
  const headline = runHeadline(evid, data);
  const title = headline || displayTitle({ ...runMeta, title: data?.title || runMeta?.display_title });
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
