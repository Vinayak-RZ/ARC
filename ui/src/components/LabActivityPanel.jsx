import { LabActivity } from "./LabActivity.jsx";

export function LabActivityPanel({ labMeta }) {
  if (!labMeta) return null;
  return (
    <section className="lab-activity-panel card-surface" aria-labelledby="lab-activity-heading">
      <h2 id="lab-activity-heading">Lab activity</h2>
      <LabActivity labMeta={labMeta} />
    </section>
  );
}