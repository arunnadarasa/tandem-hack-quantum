// Quantum shift-split mirror (classical primary; quantum = verification seal).
// Data: quantum/ward_shift_receipts.json (live Nexus H1-1LE receipt + queued jobs).
export const SHIFT_JOBS = ["J0 bedside bloods", "J1 imaging request", "J2 review NEWS7", "J3 referral"];
export const SHIFT_EDGES = [[0, 1, 3], [1, 2, 1], [2, 3, 4], [3, 0, 2]];
export const SHIFT_OPTIMUM = { cut: 10, states: ["0101", "1010"] };
export const SHIFT_RECEIPT = {
  backend: "Nexus H1-1LE",
  shots: 256,
  optimumMass: 0.1875,
  uniformMass: 0.125,
  verdict: "PASS",
  note: "Execution receipt only — no quantum advantage claimed. Classical sort decides.",
};

export function classicalShiftSplit(jobs = SHIFT_JOBS, edges = SHIFT_EDGES) {
  let best = -1, bestBits = [0, 0, 0, 0];
  for (let m = 0; m < 16; m++) {
    const bits = [0, 1, 2, 3].map((i) => (m >> i) & 1);
    const cut = edges.reduce((s, [i, j, w]) => s + (bits[i] !== bits[j] ? w : 0), 0);
    if (cut > best) { best = cut; bestBits = bits; }
  }
  return {
    now: jobs.filter((_, i) => bestBits[i] === 0),
    next: jobs.filter((_, i) => bestBits[i] === 1),
    cut: best,
  };
}
