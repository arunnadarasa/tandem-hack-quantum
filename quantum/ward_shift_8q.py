#!/usr/bin/env python3
"""WardFlow scale-up: 8-job shift-split QAOA p=2 (CQM Phase 4, toy bar passed on H1-1LE).

8 ward jobs -> 8 qubits, weighted ring + 2 cross-bay chords, QAOA p=2.
Classical optimum by brute force (256 states). 512 shots (noisy-safe).
Submit-only: journals job IDs to ward_shift_8q_jobs.json, exits fast.
"""
import time, json, sys, itertools
from pathlib import Path
import qnexus as qnx
from pytket import Circuit
from pytket.circuit import OpType

HERE = Path(__file__).parent
JOBS = ["J0 bloods A", "J1 imaging A", "J2 review NEWS7 B", "J3 referral B",
        "J4 TTO C", "J5 cannula C", "J6 discharge D", "J7 comms D"]
EDGES = [(0,1,3),(1,2,1),(2,3,4),(3,4,2),(4,5,3),(5,6,1),(6,7,4),(7,0,2),
         (0,4,2),(2,6,3)]  # ring + 2 cross-bay chords
GAMMA, BETA, SHOTS, PROJECT = 0.5, 0.4, 512, "NHS Quantum"

def classical_optimum():
    best, sols = -1, []
    for m in range(256):
        bits = [(m >> i) & 1 for i in range(8)]
        cut = sum(w for i, j, w in EDGES if bits[i] != bits[j])
        if cut > best: best, sols = cut, [bits]
        elif cut == best: sols.append(bits)
    return best, sols

def build_circuit():
    c = Circuit(8, 8)
    for q in range(8): c.H(q)
    for _ in range(2):  # p=2
        for i, j, w in EDGES:
            c.add_gate(OpType.ZZPhase, GAMMA * w, [i, j])
        for q in range(8):
            c.add_gate(OpType.Rx, BETA, [q])
    for q in range(8): c.Measure(q, q)
    return c

def main():
    dev = sys.argv[1]
    best, sols = classical_optimum()
    print(f"classical optimum cut={best} nsolutions={len(sols)}")
    circ = build_circuit()
    print(f"circuit: {circ.n_qubits}q depth={circ.depth()} gates={circ.n_gates}")
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs[PROJECT])
    up = qnx.circuits.upload(circ, name=f"wardshift8q_{dev}_{int(time.time())}")
    cfg = qnx.QuantinuumConfig(device_name=dev)
    cj = qnx.start_compile_job(programs=[up], backend_config=cfg, name=f"cmp_wardshift8q_{dev}")
    qnx.jobs.wait_for(cj, timeout=280)
    comp = qnx.jobs.results(cj)[0].get_output()
    ej = qnx.start_execute_job(programs=[comp], n_shots=[SHOTS],
                               backend_config=cfg, name=f"exe_wardshift8q_{dev}")
    jp = HERE / "ward_shift_8q_jobs.json"
    jobs = json.loads(jp.read_text()) if jp.exists() else {}
    jobs[dev] = {"execute_job_id": str(ej.id), "optimum": best,
                 "nsolutions": len(sols), "shots": SHOTS}
    jp.write_text(json.dumps(jobs, indent=2))
    print(f"SUBMITTED 8q {dev} exec={ej.id}")

if __name__ == "__main__":
    main()
