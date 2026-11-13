const KEY = "arc-theme";

export function getStoredTheme() {
  try {
    return localStorage.getItem(KEY) || "system";
  } catch {
    return "system";
  }
}

export function resolveTheme(mode) {
  if (mode === "dark") return "dark";
  if (mode === "light") return "light";
  if (typeof matchMedia !== "undefined" && matchMedia("(prefers-color-scheme: dark)").matches) {
    return "dark";
  }
  return "light";
}

export function applyTheme(mode) {
  const resolved = resolveTheme(mode);
  document.documentElement.dataset.theme = resolved;
  try {
    localStorage.setItem(KEY, mode);
  } catch {
    /* ignore */
  }
  return resolved;
}
