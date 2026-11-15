/** Lab registry — components filled in lab commits. */

export const LAB_REGISTRY = [];

export function registerLab(entry) {
  const i = LAB_REGISTRY.findIndex((l) => l.id === entry.id);
  if (i >= 0) LAB_REGISTRY[i] = entry;
  else LAB_REGISTRY.push(entry);
}
