# Cherry on top: quantum-verified handover

*Slide copy — drafted with Claude Fable 5.1, numbers from live Nexus receipts.*

WardFlow decides. Quantum signs the receipt.

- **Classical stays in charge.** WardFlow sorts the ward's jobs the normal, fast, explainable way. Nothing about the decision changes.
- **A real quantum job stamps it.** Four jobs, split into NOW vs NEXT shifts. We hand that split to Quantinuum Nexus as a 4-qubit puzzle (Max-Cut). The best answer is a perfect score of 10, reached by exactly two patterns: `0101` and `1010`.
- **The receipt is live and checkable.** On the H1-1LE emulator, 256 shots landed on those best patterns 19% of the time; random guessing gives 12.5%. That fingerprint is tied to this handover and can't be quietly edited after the fact.

Why it matters: handovers are where ward jobs get lost. A tamper-evident receipt means the incoming shift can prove what was agreed, not just remember it.

*Honesty footnote: toy problem, synthetic data, emulator run. No speed or accuracy advantage over classical is claimed; quantum here is a verification seal, not the decision-maker.*

**Spoken (15 s):** "The ward plan is made classically, exactly as today. Then a tiny quantum job on Quantinuum's stack signs it, giving the next shift a receipt nobody can fake. Small circuit, real receipt, honest claim."

## The circuit (for slides)

4 qubits, one per job (`J0` bedside bloods, `J1` imaging, `J2` review NEWS7, `J3` referral).
Qubit reads `0` = NOW shift, `1` = NEXT shift. QAOA p=1, angles in halfturns (γ=0.5, β=0.4).

```
q0: ──H──■ZZ(1.5)────────────■ZZ(1.0)──Rx(0.4)──M
         │                    │
q1: ──H──■──────■ZZ(0.5)──────┼─────────Rx(0.4)──M
                  │           │
q2: ──H──────────■──■ZZ(2.0)──┼─────────Rx(0.4)──M
                     │        │
q3: ──H─────────────■─────────■─────────Rx(0.4)──M
```

Edges (conflict weights): J0–J1 = 3, J1–J2 = 1, J2–J3 = 4, J3–J0 = 2. Classical optimum cut = 10 (`0101`, `1010`).
Runnable builder: `quantum/ward_shift_circuit.py`. Live receipts: `quantum/ward_shift_receipts.json`.

## Backend verdicts

| Backend | Status | Verdict |
|---|---|---|
| H1-1LE | COMPLETED, 256 shots, opt-mass 0.19 vs 0.125 uniform | PASS (execution receipt) |
| H2-1LE | queued | pending |
| H1-Emulator | queued | pending |
| H2-Emulator | queued | pending |
| Aer / sv1 | needs provider-specific config, out of hackathon window | honest gap, recorded |

Methodology: Clinical Quantum Methodology v1.2 (problem-first, toy-first gate, honest negatives).
DPIA GREEN: synthetic dummy jobs only — no patient data anywhere in the quantum layer.
