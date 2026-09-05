# tandem-hack-quantum

Quantum capability cherry-on-top for the **NXGN x Tandem Health hackathon** (WardFlow ward-round board).
Classical stays the decision-maker; quantum is a tamper-evident execution receipt for handover.

## What's here

| Path | What |
|---|---|
| `docs/QUANTUM_SPOTLIGHT.md` | Demo slide copy, ASCII circuit, backend verdict table |
| `quantum/ward_shift_circuit.py` | Runnable 4-qubit Max-Cut QAOA (p=1) circuit builder (pytket) |
| `quantum/ward_shift_protocol.json` | Pre-registered protocol (edges, angles, shots, bar) |
| `quantum/ward_shift_qaoa.py` | Nexus multi-backend runner (compile → execute → receipts) |
| `quantum/ward_shift_submit.py` | Submit-only helper (journal job IDs, fetch later) |
| `quantum/ward_shift_receipts.json` | Live Nexus receipts |
| `quantum/README.md` | CQM methodology framing |
| `src/lib/quantumShift.js` | JS mirror for the WardFlow frontend |

## Live proof (Quantinuum Nexus)

H1-1LE: 256 shots, optimum-mass 0.19 vs 0.125 uniform — PASS as execution receipt.
H2-1LE + noisy emulators queued; Aer/sv1 recorded as honest config gap.
Synthetic data only. No quantum advantage claimed.

## Run it

```bash
/Users/openclaw/.hermes/hermes-agent/venv/bin/python quantum/ward_shift_submit.py H1-1LE
```
