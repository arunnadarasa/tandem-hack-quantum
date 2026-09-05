#!/usr/bin/env python3
"""WardFlow quantum capability toy (CQM Phase 3, toy-first gate).

Problem (Phase 0): junior doctors criss-cross Ward 31 chasing jobs.
Classical baseline (stays primary): CATEGORY_ORDER efficiency sort in
src/lib/ward-data.ts. Quantum cherry: 4-job shift-split QAOA p=1 —
partition 4 candidate jobs into NOW vs NEXT to maximise separated
conflict weight (walking + dependency). Max-Cut on a 4-node ring.

Pre-registered protocol: configs/ward_shift_protocol.json
Decision rule: PASS = Nexus counts distribution overlaps an exact
optimum cut within envelope 4*sqrt(0.5/shots) on total optimum mass.
Honest framing: classical sort stays the decision-maker; quantum is a
tamper-evident sampling receipt for handover, NO advantage claimed.
DPIA GREEN: synthetic dummy jobs only, no patient data.
"""
import time, json, itertools, math, sys
from pathlib import Path
import qnexus as qnx
from pytket import Circuit
from pytket.circuit import OpType

HERE = Path(__file__).parent
PROTO = json.loads((HERE / "ward_shift_protocol.json").read_text())
W = PROTO["edges"]            # [[i,j,w],...]
GAMMA = PROTO["gamma"]; BETA = PROTO["beta"]
SHOTS = PROTO["shots"]; PROJECT = PROTO["project"]

def classical_optimum():
    best, solutions = -1, []
    for bits in itertools.product([0,1], repeat=4):
        cut = sum(w for i,j,w in W if bits[i]!=bits[j])
        if cut > best: best, solutions = cut, [bits]
        elif cut == best: solutions.append(bits)
    return best, solutions

def build_circuit():
    c = Circuit(4, 4)
    for q in range(4): c.H(q)
    for i,j,w in W:
        c.add_gate(OpType.ZZPhase, GAMMA*w, [i,j])
    for q in range(4):
        c.add_gate(OpType.Rx, BETA, [q])  # mixer exp(-i pi*BETA X/2); angles in halfturns
    for q in range(4): c.Measure(q, q)
    return c

def run_one(device, circuit):
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs[PROJECT])
    up = qnx.circuits.upload(circuit, name=f"wardshift_{device}_{int(time.time())}")
    cfg = qnx.QuantinuumConfig(device_name=device)
    cj = qnx.start_compile_job(programs=[up], backend_config=cfg, name=f"cmp_wardshift_{device}")
    qnx.jobs.wait_for(cj, timeout=300)
    comp = qnx.jobs.results(cj)[0].get_output()
    ej = qnx.start_execute_job(programs=[comp], n_shots=[SHOTS], backend_config=cfg, name=f"exe_wardshift_{device}")
    qnx.jobs.wait_for(ej, timeout=1200)
    res = qnx.jobs.results(ej)[0].download_result()
    counts = res.get_counts() if hasattr(res, "get_counts") else res.register_counts()
    return str(ej.id), counts

def main():
    best, sols = classical_optimum()
    sol_strs = {"".join(map(str,s)) for s in sols}
    print(f"classical optimum cut={best} solutions={sorted(sol_strs)}")
    circ = build_circuit()
    out = {"protocol": PROTO, "classical_optimum": best,
           "optimum_states": sorted(sol_strs), "backends": {}}
    rp = HERE / "ward_shift_receipts.json"
    if rp.exists():  # resume: keep prior backends
        try: out["backends"] = json.loads(rp.read_text()).get("backends", {})
        except Exception: pass
    want = sys.argv[1:] or PROTO["backends"]
    for dev in want:
        if dev in out["backends"] and "counts" in out["backends"][dev]:
            print(f"{dev}: already have receipts, skipping"); continue
        try:
            jid, counts = run_one(dev, circ)
            norm = {str(k): int(v) for k,v in dict(counts).items()}
            # counts keys are tuples of bits; normalise to bitstring
            flat = {}
            for k,v in counts.items():
                try: bits = "".join(map(str, tuple(k)))
                except TypeError: bits = str(k)
                flat[bits] = flat.get(bits, 0) + int(v)
            opt_mass = sum(v for b,v in flat.items() if b in sol_strs)/SHOTS
            env = 4*math.sqrt(0.5/SHOTS)
            verdict = "PASS" if opt_mass >= (len(sol_strs)/16 - env) else "BELOW-UNIFORM"
            out["backends"][dev] = {"job_id": jid, "counts": flat,
                "optimum_mass": round(opt_mass,4), "envelope": round(env,4),
                "verdict": verdict, "backend_qualifier": "emulator"}
            print(f"{dev}: {verdict} opt_mass={opt_mass:.3f} job={jid}")
        except Exception as e:
            out["backends"][dev] = {"error": f"{type(e).__name__}: {e}"}
            print(f"{dev}: ERROR {type(e).__name__}: {e}")
        rp.write_text(json.dumps(out, indent=2))  # journal after EVERY backend
    print(f"receipts -> {rp}")

if __name__ == "__main__":
    main()
