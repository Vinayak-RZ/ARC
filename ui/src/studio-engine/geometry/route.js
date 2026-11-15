/** Orthogonal routing helpers (pure JS). */

export function orthoPath(x1, y1, x2, y2) {
  if (Math.abs(y1 - y2) < 1) return `M ${x1} ${y1} H ${x2}`;
  if (Math.abs(x1 - x2) < 1) return `M ${x1} ${y1} V ${y2}`;
  const midX = (x1 + x2) / 2;
  return `M ${x1} ${y1} H ${midX} V ${y2} H ${x2}`;
}

/** Local pin offset in grid units before rotation. */
export function pinOffset(type, pin) {
  const table = {
    resistor: { a: [-1, 0], b: [1, 0] },
    inductor: { a: [-1, 0], b: [1, 0] },
    capacitor: { a: [-0.5, 0], b: [0.5, 0] },
    switch: { a: [-1, 0], b: [1, 0] },
    vsource: { p: [0, -1], n: [0, 1] },
    isource: { p: [0, -1], n: [0, 1] },
    acsource: { p: [0, -1], n: [0, 1] },
    diode: { a: [-0.5, 0], k: [0.5, 0] },
    scr: { a: [-0.5, 0], k: [0.5, 0], g: [0, 0.5] },
    igbt: { c: [0, -0.75], e: [0, 0.75], g: [-0.75, 0] },
    ground: { a: [0, 0] },
    transformer: { p1: [-1, -0.5], p2: [-1, 0.5], s1: [1, -0.5], s2: [1, 0.5] },
    motor: { a: [-1, 0], b: [1, 0] },
    opamp: { inp: [-1, -0.4], inn: [-1, 0.4], out: [1, 0] },
    bjt: { c: [0, -0.75], b: [-0.75, 0], e: [0, 0.75] },
    junction: { a: [0, 0] },
    terminal: { a: [0, 0] },
  };
  return table[type]?.[pin] || [0, 0];
}

function rotate([x, y], rot) {
  const r = ((rot % 360) + 360) % 360;
  if (r === 90) return [-y, x];
  if (r === 180) return [-x, -y];
  if (r === 270) return [y, -x];
  return [x, y];
}

export function pinPosition(comp, pin, grid = 40) {
  const [dx, dy] = rotate(pinOffset(comp.type, pin), comp.rot || 0);
  const [ax, ay] = comp.at || [0, 0];
  return { x: (ax + dx) * grid, y: (ay + dy) * grid };
}

export function routeWire(a, b) {
  return orthoPath(a.x, a.y, b.x, b.y);
}
