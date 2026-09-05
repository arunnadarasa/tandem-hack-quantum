#!/usr/bin/env python3
"""Ward-scale demo: 26-qubit shift-split QAOA p=1 on Nexus H2-1LE.

26 ward jobs -> 26 qubits (whole-ward NOW/NEXT split). Ring + cross-bay
chords, QAOA p=1, 512 shots. 2^26 = 67M states: too many to enumerate
honestly on a laptop, so the metric is MEAN SAMPLED CUT vs uniform-random
baseline (10k random bitstrings) — an honest, computable yardstick.

Framing (binding): "hardware-scale readiness demo". Emulator run, classically
simulable, NO quantum advantage claimed; advantage is a pre-registered
future claim gated on real QPU + matched classical baselines.
Also submits a 26q GHZ as the entanglement-scale slide asset.
"""
import time, json, sys, random
from pathlib import Path
import qnexus as qnx
from pytket import Circuit
from pytket.circuit import OpType

HERE = Path(__file__).parent
N = 26
random.seed(31)
# ring + 13 random cross-chords, weights 1-4 (synthetic ward conflicts)
EDGES = [(i, (i + 1) % N, random.randint(1, 4)) for i in range(N)]
EDGES += [(random.randrange(N), random.randrange(N), random.randint(1, 4)) for _ in range(13)]
EDGES = [(i, j, w) for i, j, w in EDGES if i != j]
GAMMA, BETA, SHOTS, PROJECT = 0.35, 0.4, 512, "NHS Quantum"

def cut_value(bits):
    return sum(w for i, j, w in EDGES if bits[i] != bits[j])

def random_baseline(n=10000):
    tot = 0
    for _ in range(n):
        bits = [random.randint(0, 1) for _ in range(N)]
        tot += cut_value(bits)
    return tot / n

def build_qaoa():
    c = Circuit(N, N)
    for q in range(N): c.H(q)
    for i, j, w in EDGES:
        c.add_gate(OpType.ZZPhase, GAMMA * w, [i, j])
    for q in range(N):
        c.add_gate(OpType.Rx, BETA, [q])
    for q in range(N): c.Measure(q, q)
    return c

def build_ghz():
    c = Circuit(N, N)
    c.H(0)
    for q in range(N - 1): c.CX(q, q + 1)
    for q in range(N): c.Measure(q, q)
    return c

def main():
    dev = sys.argv[1] if len(sys.argv) > 1 else "H2-1LE"
    base = random_baseline()
    qaoa, ghz = build_qaoa(), build_ghz()
    print(f"edges={len(EDGES)} random_baseline_cut={base:.2f}")
    print(f"qaoa: {qaoa.n_qubits}q depth={qaoa.depth()} gates={qaoa.n_gates}")
    print(f"ghz : {ghz.n_qubits}q depth={ghz.depth()} gates={ghz.n_gates}")
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs[PROJECT])
    cfg = qnx.QuantinuumConfig(device_name=dev)
    ts = int(time.time())
    u1 = qnx.circuits.upload(qaoa, name=f"ward26_qaoa_{ts}")
    u2 = qnx.circuits.upload(ghz, name=f"ward26_ghz_{ts}")
    cj = qnx.start_compile_job(programs=[u1, u2], backend_config=cfg, name=f"cmp_ward26_{dev}")
    qnx.jobs.wait_for(cj, timeout=280)
    comps = [r.get_output() for r in qnx.jobs.results(cj)]
    ej = qnx.start_execute_job(programs=comps, n_shots=[SHOTS, SHOTS],
                               backend_config=cfg, name=f"exe_ward26_{dev}")
    jp = HERE / "ward26_jobs.json"
    jobs = json.loads(jp.read_text()) if jp.exists() else {}
    jobs[dev] = {"execute_job_id": str(ej.id), "programs": ["qaoa26", "ghz26"],
                 "shots": SHOTS, "edges": EDGES, "random_baseline_cut": round(base, 2),
                 "gamma": GAMMA, "beta": BETA}
    jp.write_text(json.dumps(jobs, indent=2))
    print(f"SUBMITTED 26q {dev} exec={ej.id}")

if __name__ == "__main__":
    main()
