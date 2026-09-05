# Quantum Capability Layer — WardFlow Shift-Split Toy (CQM v1.2)

Cherry on top for NXGN x Tandem Health hackathon. Classical app stays primary;
quantum is optional, honest, reproducible augmentation.

## Problem first (Phase 0)
Junior doctors lose ward-round time criss-crossing bays and chasing jobs.
WardFlow already sorts jobs by category workflow order. The quantum toy answers
one narrow question: split 4 candidate jobs into NOW vs NEXT so the most
conflicting pairs (walking distance + blocked dependencies) land in different
shifts — a 4-node Max-Cut QUBO, QAOA p=1.

## Why this toy (Alexandre's toy-first gate)
2–4 qubits, one mechanism, pre-registered bar in
`quantum/ward_shift_protocol.json`. Fail the bar → no scaling. Classical
efficiency sort remains the decision-maker regardless.

## Safety (Phase 1)
DPIA GREEN: synthetic dummy jobs only (`J0..J3` urgency scores). No patient
data, no NHS numbers, nothing leaves the laptop except a 4-qubit circuit.

## 10-Year Plan anchor
Fit for the Future: shift care from hospital to community and cut admin burden
via digital productivity. WardFlow targets the admin-burden half; the quantum
receipt adds tamper-evident auditability to handover prioritisation.

## Files
- `quantum/ward_shift_protocol.json` — pre-registered protocol (edges, γ, β, shots, bar)
- `quantum/ward_shift_qaoa.py` — Nexus runner (compile → execute → receipts)
- `quantum/ward_shift_receipts.json` — QAS-style receipts per backend (proof of concept)
- `src/lib/quantum-prioritizer.ts` — frontend hook: classical split + receipt display

## Honest verdict rule
PASS = optimum-state sampling mass ≥ uniform mass − envelope (4√(0.5/shots)).
A PASS certifies reproducible execution, NOT quantum advantage. Any BELOW-UNIFORM
or backend error is reported as-is — honest negatives are deliverables (CQM value 3).
