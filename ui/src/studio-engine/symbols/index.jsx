/** SVG symbol drawers. Pins in local grid units. */

const STROKE = { stroke: "currentColor", strokeWidth: 1.75, fill: "none", vectorEffect: "non-scaling-stroke" };

function ZigZag() {
  return <path d="M -20 0 H -12 L -8 -8 L 0 8 L 8 -8 L 12 0 H 20" {...STROKE} />;
}

export const SYMBOLS = {
  resistor: { pins: { a: [-1, 0], b: [1, 0] }, span: [2, 1], Draw: () => <ZigZag /> },
  inductor: {
    pins: { a: [-1, 0], b: [1, 0] },
    span: [2, 1],
    Draw: () => <path d="M -20 0 H -12 C -12 -10,-4 -10,-4 0 C -4 10,4 10,4 0 C 4 -10,12 -10,12 0 H 20" {...STROKE} />,
  },
  capacitor: {
    pins: { a: [-0.5, 0], b: [0.5, 0] },
    span: [1, 1],
    Draw: () => (
      <g>
        <path d="M -20 0 H -4" {...STROKE} />
        <path d="M -4 -12 V 12" {...STROKE} />
        <path d="M 4 -12 V 12" {...STROKE} />
        <path d="M 4 0 H 20" {...STROKE} />
      </g>
    ),
  },
  switch: {
    pins: { a: [-1, 0], b: [1, 0] },
    span: [2, 1],
    Draw: () => (
      <g>
        <circle cx={-16} cy={0} r={3} fill="currentColor" />
        <circle cx={16} cy={0} r={3} fill="currentColor" />
        <path d="M -16 0 L 12 -10" {...STROKE} />
      </g>
    ),
  },
  vsource: {
    pins: { p: [0, -1], n: [0, 1] },
    span: [1, 2],
    Draw: () => (
      <g>
        <circle r={14} {...STROKE} />
        <path d="M 0 -20 V -14 M 0 14 V 20" {...STROKE} />
        <path d="M -4 -6 H 4 M 0 -10 V -2" {...STROKE} />
        <path d="M -4 6 H 4" {...STROKE} />
      </g>
    ),
  },
  isource: {
    pins: { p: [0, -1], n: [0, 1] },
    span: [1, 2],
    Draw: () => (
      <g>
        <circle r={14} {...STROKE} />
        <path d="M 0 -8 V 8" {...STROKE} />
        <path d="M -4 4 L 0 8 L 4 4" {...STROKE} />
      </g>
    ),
  },
  acsource: {
    pins: { p: [0, -1], n: [0, 1] },
    span: [1, 2],
    Draw: () => (
      <g>
        <circle r={14} {...STROKE} />
        <path d="M -8 0 C -4 -10,4 10,8 0" {...STROKE} />
      </g>
    ),
  },
  diode: {
    pins: { a: [-0.5, 0], k: [0.5, 0] },
    span: [1, 1],
    Draw: () => (
      <g>
        <path d="M -20 0 H -6" {...STROKE} />
        <path d="M -6 -10 L 6 0 L -6 10 Z" stroke="currentColor" strokeWidth={1.75} fill="currentColor" />
        <path d="M 6 -10 V 10 M 6 0 H 20" {...STROKE} />
      </g>
    ),
  },
  scr: {
    pins: { a: [-0.5, 0], k: [0.5, 0], g: [0, 0.5] },
    span: [1, 1],
    Draw: () => (
      <g>
        <path d="M -20 0 H -6" {...STROKE} />
        <path d="M -6 -10 L 6 0 L -6 10 Z" stroke="currentColor" strokeWidth={1.75} fill="currentColor" />
        <path d="M 6 -10 V 10 M 6 0 H 20" {...STROKE} />
        <path d="M 0 0 L 0 14 L 8 14" {...STROKE} />
      </g>
    ),
  },
  igbt: {
    pins: { c: [0, -0.75], e: [0, 0.75], g: [-0.75, 0] },
    span: [1.5, 1.5],
    Draw: () => (
      <g>
        <path d="M 0 -20 V -6 M 0 6 V 20" {...STROKE} />
        <path d="M -8 -10 V 10" {...STROKE} />
        <path d="M -8 0 H -20" {...STROKE} />
        <path d="M -8 -6 H 0 M -8 6 H 0" {...STROKE} />
      </g>
    ),
  },
  ground: {
    pins: { a: [0, 0] },
    span: [1, 1],
    Draw: () => (
      <g>
        <path d="M 0 0 V 8 M -12 8 H 12 M -8 12 H 8 M -4 16 H 4" {...STROKE} />
      </g>
    ),
  },
  transformer: {
    pins: { p1: [-1, -0.5], p2: [-1, 0.5], s1: [1, -0.5], s2: [1, 0.5] },
    span: [2, 2],
    Draw: () => (
      <g>
        <path d="M -16 -16 V 16 M 16 -16 V 16" {...STROKE} />
        <path d="M -8 -12 C -2 -12,-2 0,-8 0 C -2 0,-2 12,-8 12" {...STROKE} />
        <path d="M 8 -12 C 2 -12,2 0,8 0 C 2 0,2 12,8 12" {...STROKE} />
      </g>
    ),
  },
  motor: {
    pins: { a: [-1, 0], b: [1, 0] },
    span: [2, 2],
    Draw: () => (
      <g>
        <circle r={16} {...STROKE} />
        <text textAnchor="middle" dominantBaseline="central" fontSize="11" fill="currentColor">
          M
        </text>
      </g>
    ),
  },
  opamp: {
    pins: { inp: [-1, -0.4], inn: [-1, 0.4], out: [1, 0] },
    span: [2, 1.5],
    Draw: () => (
      <g>
        <path d="M -20 -16 L 20 0 L -20 16 Z" {...STROKE} />
        <path d="M -14 -8 H -8 M -14 8 H -8 M -11 5 V 11" {...STROKE} />
      </g>
    ),
  },
  bjt: {
    pins: { c: [0, -0.75], b: [-0.75, 0], e: [0, 0.75] },
    span: [1.5, 1.5],
    Draw: () => (
      <g>
        <path d="M -10 -12 V 12" {...STROKE} />
        <path d="M -20 0 H -10" {...STROKE} />
        <path d="M -10 -6 L 8 -16 M -10 6 L 8 16" {...STROKE} />
      </g>
    ),
  },
  junction: {
    pins: { a: [0, 0] },
    span: [0.5, 0.5],
    Draw: () => <circle r={3} fill="currentColor" />,
  },
  terminal: {
    pins: { a: [0, 0] },
    span: [0.5, 0.5],
    Draw: () => <circle r={3} fill="none" stroke="currentColor" strokeWidth={1.75} />,
  },
};
