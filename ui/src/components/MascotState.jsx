import { ArcMascot } from "../mascot/index.js";

/**
 * Shared loading / empty / error block with Arc mascot + caption + optional action.
 */
export function MascotState({
  kind = "empty",
  title,
  message,
  actionLabel,
  onAction,
  size = 72,
  className = "",
}) {
  const mode = kind === "loading" ? "thinking" : kind === "error" ? "error" : "ambient";
  return (
    <div className={`mascot-state mascot-state-${kind}${className ? ` ${className}` : ""}`} role="status">
      <ArcMascot mode={mode} size={size} label={title || kind} arrive={kind === "loading"} />
      {title ? <h2 className="mascot-state-title">{title}</h2> : null}
      {message ? <p className="mascot-state-msg">{message}</p> : null}
      {actionLabel && onAction ? (
        <button type="button" className="button-primary button-compact" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </div>
  );
}
