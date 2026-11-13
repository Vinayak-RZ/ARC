/** Display-type answer: quantity name, value, muted unit (not monospace). */

export function AnswerLine({ parts, checked }) {
  const { name, value, unit } = parts;
  const cls = checked ? "answer-line is-checked" : "answer-line";
  return (
    <p className={cls}>
      <span className="answer-name">{name}</span>
      <span className="answer-eq"> = </span>
      <span className="answer-num">{value}</span>
      {unit ? <span className="answer-unit"> {unit}</span> : null}
    </p>
  );
}
