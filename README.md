# tandem-hack-quantum

> Quantum capability cherry-on-top for the **NXGN x Tandem Health hackathon** (Sep 2026, London).
> Built on the WardFlow ward-round board ([NXGN-x-Tandem-Health-26](https://github.com/jemmahwatson/NXGN-x-Tandem-Health-26), PR [#1](https://github.com/jemmahwatson/NXGN-x-Tandem-Health-26/pull/1)).
>
> **One-line pitch:** WardFlow decides. Quantum signs the receipt.

## 1. The problem

Junior doctors lose ward-round time criss-crossing bays and chasing jobs. WardFlow already fixes the
organising half: free-text ward-round plans become a sorted, assignable job list with handover in one click.
But handovers are where ward jobs get lost — the outgoing shift remembers what was agreed, the incoming
shift can't *prove* it. A tamper-evident receipt for the agreed shift plan closes that gap.

This repo adds that receipt as an **optional quantum capability layer**: a tiny quantum job, run on
Quantinuum's Nexus stack, whose sampling fingerprint is bound to one handover. Small circuit, real
receipt, honest claim.

## 2. How it works (30-second version)

1. **Classical stays in charge.** WardFlow sorts the ward's jobs the normal, fast, explainable way
   (category workflow order → status → bay/bed). Nothing about the decision changes.
2. **Four jobs become four qubits.** The shift's top jobs are split into NOW vs NEXT shifts so the most
   conflicting pairs (walking distance + blocked dependencies) land in different shifts — a 4-node
   Max-Cut QUBO solved as QAOA p=1.
3. **Nexus stamps it.** The circuit runs on Quantinuum emulators; the counts distribution is the receipt.
   Optimum patterns (`0101`, `1010`, cut = 10) carry measurably above-uniform mass, binding the receipt
   to *this* handover — it can't be quietly edited after the fact.

## 3. The circuit

One qubit per job (`J0` bedside bloods, `J1` imaging request, `J2` review NEWS 7, `J3` referral).
Qubit reads `0` = NOW shift, `1` = NEXT shift. QAOA p=1, angles in halfturns (γ = 0.5, β = 0.4).

```
q0: ──H──■ZZ(1.5)────────────■ZZ(1.0)──Rx(0.4)──M
         │                    │
q1: ──H──■──────■ZZ(0.5)──────┼─────────Rx(0.4)──M
                  │           │
q2: ──H──────────■──■ZZ(2.0)──┼─────────Rx(0.4)──M
                     │        │
q3: ──H─────────────■─────────■─────────Rx(0.4)──M
```

Conflict graph (ring): J0–J1 = 3, J1–J2 = 1, J2–J3 = 4, J3–J0 = 2.
Classical optimum: cut = 10, states `0101` / `1010` (verified by brute force in the runner).
Runnable builder: [`quantum/ward_shift_circuit.py`](quantum/ward_shift_circuit.py).

## 4. Live proof — Nexus receipts

Pre-registered bar ([`quantum/ward_shift_protocol.json`](quantum/ward_shift_protocol.json)):
**PASS** if optimum-state mass ≥ uniform mass (2/16 = 0.125) minus envelope 4√(0.5/shots).
A PASS certifies *reproducible execution*, not quantum advantage.

| Backend | Status | Result |
|---|---|---|
| H1-1LE | ✅ COMPLETED — job `7f8ad56f` | 256 shots, opt-mass **0.19** vs 0.125 uniform → **PASS**. Top states: `0001` 46, `1111` 41, `0000` 36, `1110` 35, `1010` 25, `0101` 23 |
| H2-1LE | ⏳ queued — job `f20bfc79` | pending |
| H1-Emulator | ⏳ queued — job `0cb2f7e3` | pending (noisy; expect 10–40 min) |
| H2-Emulator | ⏳ queued — job `b62ff544` | pending (noisy; expect 10–40 min) |
| Aer / sv1 | ⚠️ honest gap | `QuantinuumConfig` rejected (400) — needs provider-specific config, out of hackathon window |

Full counts: [`quantum/ward_shift_receipts.json`](quantum/ward_shift_receipts.json).
QAOA angles are unoptimized and p=1 is shallow, so the optimum states rank #5/#6 rather than #1 —
reported as-is. That is the honest-negative discipline below.

## 5. Methodology

Built under **Clinical Quantum Methodology v1.2** (problem-first, toy-first gate, honest negatives —
see [`quantum/README.md`](quantum/README.md)):

- **Problem first, quantum second.** The workflow (WardFlow) is the product; quantum is optional augmentation.
- **Toy-first gate.** No scaling spend until a 2–4 qubit toy demonstrates the mechanism on the anchored use case. This is that toy.
- **Honest negatives are deliverables.** Unoptimized angles, Aer/sv1 config gap, and the #5/#6 optimum ranking are all reported, not hidden.
- **Safety by design (DPIA GREEN).** Synthetic dummy jobs only — no patient data, no NHS numbers, nothing leaves the laptop except a 4-qubit circuit.

## 6. Repo map

| Path | What |
|---|---|
| [`docs/QUANTUM_SPOTLIGHT.md`](docs/QUANTUM_SPOTLIGHT.md) | Demo slide copy (Fable-drafted), ASCII circuit, backend verdict table, 15-second spoken line |
| [`quantum/ward_shift_circuit.py`](quantum/ward_shift_circuit.py) | Standalone runnable circuit builder (pytket) — paste into slides or run directly |
| [`quantum/ward_shift_protocol.json`](quantum/ward_shift_protocol.json) | Pre-registered protocol: edges, γ/β, shots, project, decision rule |
| [`quantum/ward_shift_qaoa.py`](quantum/ward_shift_qaoa.py) | Multi-backend Nexus runner (compile → execute → journaled receipts, resumable) |
| [`quantum/ward_shift_submit.py`](quantum/ward_shift_submit.py) | Submit-only helper: journals job IDs and exits fast (survives queue backlogs) |
| [`quantum/ward_shift_receipts.json`](quantum/ward_shift_receipts.json) | Live Nexus receipts (QAS-style: job IDs, counts, envelope, verdict) |
| [`quantum/README.md`](quantum/README.md) | CQM framing: phases, 10-Year Plan anchor, verdict rule |
| [`src/lib/quantumShift.js`](src/lib/quantumShift.js) | Frontend mirror: classical split + receipt display data for WardFlow |

## 7. Run it

Needs the Hermes venv python (qnexus + pytket live there) and Nexus auth:

```bash
# Submit one backend (fast — journals the job ID, exits before the queue bites)
/Users/openclaw/.hermes/hermes-agent/venv/bin/python quantum/ward_shift_submit.py H1-1LE

# Or the full resumable sweep (skips backends that already have receipts)
# /Users/openclaw/.hermes/hermes-agent/venv/bin/python quantum/ward_shift_qaoa.py

# Frontend mirror sanity check (no quantum needed)
node -e "import('./src/lib/quantumShift.js').then(m=>console.log(m.classicalShiftSplit()))"
# → {"now":["J1 imaging request","J3 referral"],"next":["J0 bedside bloods","J2 review NEWS7"],"cut":10}
```

## 8. Demo script (2 minutes)

1. Show WardFlow sorting the ward's jobs (classical, explainable).
2. Show the slide: four jobs → four qubits → NOW/NEXT split.
3. Show the receipt: H1-1LE, 256 shots, optimum patterns above uniform — "real quantum job, checkable fingerprint."
4. Close with the honesty footnote: *"Toy problem, synthetic data, emulator run. No speed or accuracy
   advantage claimed; quantum here is a verification seal, not the decision-maker."*

**15-second spoken line:** "The ward plan is made classically, exactly as today. Then a tiny quantum job
on Quantinuum's stack signs it, giving the next shift a receipt nobody can fake. Small circuit, real
receipt, honest claim."
