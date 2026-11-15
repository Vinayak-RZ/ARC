export function converterMetrics(p) {
  const { topology, vin, d, l, c, fs, r } = p;
  let Vo;
  let deltaIl;
  let deltaVo;
  let Lcrit;
  if (topology === "buck") {
    Vo = d * vin;
    deltaIl = ((vin - Vo) * d) / (l * fs);
    deltaVo = deltaIl / (8 * c * fs);
    Lcrit = ((vin - Vo) * (1 - d)) / (2 * fs * (Vo / r));
  } else if (topology === "boost") {
    Vo = vin / (1 - d);
    deltaIl = (vin * d) / (l * fs);
    const Io = Vo / r;
    deltaVo = (Io * d) / (c * fs);
    Lcrit = (d * (1 - d) ** 2 * r) / (2 * fs);
  } else {
    // buck-boost
    Vo = (-vin * d) / (1 - d);
    deltaIl = (vin * d) / (l * fs);
    const Io = Math.abs(Vo) / r;
    deltaVo = (Io * d) / (c * fs);
    Lcrit = ((1 - d) ** 2 * r) / (2 * fs);
  }
  const ccm = l >= Lcrit;
  const points = [
    [0, 1],
    [d, 1 + deltaIl / 2],
    [1, 1],
  ];
  return { Vo, deltaIl, deltaVo, Lcrit, ccm, points };
}
