import { readFileSync } from "node:fs";
import { PNG } from "pngjs";
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
    const nodes = [...document.querySelectorAll(".studio-circuit-app .react-flow__node")];
    for (const node of nodes) {
      const b = node.getBoundingClientRect();
      if (b.top < wrap.top - 2 || b.bottom > wrap.bottom + 2 || b.left < wrap.left - 2 || b.right > wrap.right + 2) {
        return "node outside canvas";
      }
    }
    const hint = document.querySelector(".studio-circuit-hint");
    if (hint) {
      const style = getComputedStyle(hint);
      if (style.display !== "none" && style.visibility !== "hidden") {
        const h = hint.getBoundingClientRect();
        for (const node of nodes) {
          const b = node.getBoundingClientRect();
          const overlap =
            h.left < b.right - 2 && h.right > b.left + 2 && h.top < b.bottom - 2 && h.bottom > b.top + 2;
          if (overlap) return "hint overlaps node";
        }
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

export async function prepareTheme(page: Page, theme: "light" | "dark") {
  await page.addInitScript((t) => {
    try {
      localStorage.setItem("arc-theme", t);
    } catch {
      /* ignore */
    }
    document.documentElement.setAttribute("data-theme", t);
  }, theme);
}

export async function reinforceTheme(page: Page, theme: "light" | "dark") {
  await page.evaluate((t) => {
    try {
      localStorage.setItem("arc-theme", t);
    } catch {
      /* ignore */
    }
    document.documentElement.setAttribute("data-theme", t);
  }, theme);
}

/** Luminance of circuit canvas CSS background (0–1). Dark should be well below 0.2. */
export async function circuitCanvasLuminance(page: Page): Promise<number> {
  return page.evaluate(() => {
    const el = document.querySelector(".studio-circuit-app .studio-circuit-canvas");
    if (!el) return 1;
    const bg = getComputedStyle(el).backgroundColor;
    const m = bg.match(/[\d.]+/g);
    if (!m || m.length < 3) return 1;
    const [r, g, b] = m.map(Number);
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
  });
}

/** Sample PNG pixels in the circuit canvas band; fail if average RGB looks like light theme (#fafaf9). */
export function assertDarkPngCanvasNotLight(pngPath: string) {
  const png = PNG.sync.read(readFileSync(pngPath));
  const { width: w, height: h, data } = png;
  const pts: [number, number][] = [
    [Math.floor(w * 0.26), Math.floor(h * 0.22)],
    [Math.floor(w * 0.42), Math.floor(h * 0.32)],
    [Math.floor(w * 0.3), Math.floor(h * 0.38)],
  ];
  let sum = 0;
  for (const [x, y] of pts) {
    const i = (y * w + x) * 4;
    sum += (data[i] + data[i + 1] + data[i + 2]) / 3;
  }
  const avg = sum / pts.length;
  if (avg >= 95) {
    throw new Error(`dark capture looks light (avg rgb ${avg.toFixed(1)})`);
  }
}