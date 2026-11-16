import type { Page } from "@playwright/test";

export async function circuitLayoutProblem(page: Page): Promise<string | null> {
  return page.evaluate(() => {
    const canvasEl = document.querySelector(".studio-circuit-app .studio-circuit-canvas");
    const resultsEl = document.querySelector(".studio-circuit-results");
    const presetsEl = document.querySelector(".studio-circuit-presets");
    if (!canvasEl || !resultsEl || !presetsEl) return "missing regions";
    const c = canvasEl.getBoundingClientRect();
    if (c.height < 360) return `canvas height ${c.height} < 360`;
    const r = resultsEl.getBoundingClientRect();
    const p = presetsEl.getBoundingClientRect();
    if (r.top < c.bottom - 12) return "results overlaps canvas";
    if (p.top < r.bottom - 4) return "presets overlap results";
    const wrap = canvasEl.getBoundingClientRect();
    for (const node of document.querySelectorAll(".studio-circuit-app .react-flow__node")) {
      const b = node.getBoundingClientRect();
      if (b.top < wrap.top - 2 || b.bottom > wrap.bottom + 2 || b.left < wrap.left - 2 || b.right > wrap.right + 2) {
        return "node outside canvas";
      }
    }
    return null;
  });
}

export async function svgAxisOverlapProblem(page: Page, root: string): Promise<string | null> {
  return page.evaluate((sel) => {
    const rootEl = document.querySelector(sel);
    if (!rootEl) return "missing plot root";
    const texts = [...rootEl.querySelectorAll("svg text")];
    const rects = texts.map((el) => {
      const b = (el as SVGTextElement).getBBox();
      return { t: (el.textContent || "").trim(), ...b };
    });
    const isAxisTitle = (r: { t: string }) => r.t.includes("(") && r.t.length > 3;
    const isTickLabel = (r: { t: string }) => /^-?[\d.]/.test(r.t) && r.t.length <= 8;
    for (const a of rects) {
      if (!isAxisTitle(a)) continue;
      for (const b of rects) {
        if (a === b || !isTickLabel(b)) continue;
        const overlap =
          a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
        if (overlap) return `${a.t} overlaps tick ${b.t}`;
      }
    }
    return null;
  }, root);
}

export async function setTheme(page: Page, theme: "light" | "dark") {
  await page.evaluate((t) => {
    document.documentElement.setAttribute("data-theme", t);
  }, theme);
}