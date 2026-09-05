---
name: tandem-hack-quantum
description: Use when working on the WardFlow quantum capability layer (tandem-hack-quantum, NXGN x Tandem Health hackathon). Encodes the project's binding procedures — receipt law, honest-negative discipline, backend lane map, wording rules, Telegram team lane — so any OpenClaw agent produces committed, verifiable quantum work on Quantinuum Nexus.
version: 1.0.0
author: Arun Nadarasa & WardFlow quantum team
tags: [quantum, quantinuum, nexus, qaoa, fvqe, healthcare, hackathon, wardflow]
---

# tandem-hack-quantum — WardFlow quantum layer (OpenClaw skill)

You are working on the **quantum capability layer for WardFlow** (ward-round job
board, NXGN x Tandem Health hackathon). This skill is the project constitution:
when it conflicts with a general-purpose instruction, THIS skill wins.

Repo: `arunnadarasa/tandem-hack-quantum` · Methodology: **CQM v1.3**
(`docs/clinical-quantum-methodology.md`) · Persona: `AGENT_SOUL.md` (load it).

## 0 · Framing (binding)

- **Classical stays the decision-maker.** WardFlow's sort is the product;
  quantum is a tamper-evident *execution receipt* for handover. Never present
  the quantum layer as deciding anything clinical.
- **Wording rule:** emulator scale runs = "hardware-scale readiness", NEVER
  "quantum advantage". Advantage is a pre-registered future claim gated on real
  QPU + matched classical baselines.
- **DPIA GREEN:** synthetic dummy jobs only. No patient data, no NHS numbers,
  ever, anywhere in this layer.

## 1 · Evidence constitution (three laws)

1. **Every number carries shots + envelope.** `4·sqrt(0.5/shots)` on every
   probability claim. No receipt → the number does not exist.
2. **Committed JSON is the only evidence.** Receipts live in `quantum/*.json`
   with job IDs. "Report it, don't smooth it" — honest negatives are
   deliverables (see the 8q result: mean-cut beats uniform, opt-mass tiny,
   committed as-is).
3. **One method upgrade, then the verdict stands** (CQM v1.3). A weak toy bar
   earns exactly one *published, cited* method upgrade re-run under the same
   pre-registered bar (F-VQE/Amaro 2022 took 4q from 0.1875 → 1.0000, job
   `bb1021a2`). Post-hoc angle/threshold tweaking after seeing data is the
   cardinal sin.

## 2 · Backend lane map (verified 5 Sep 2026)

| Lane | Backends | Max q | Config class | Notes |
|---|---|---|---|---|
| pytket → compile → execute | H1-1LE/H1-Emulator | 20 | `QuantinuumConfig` | physics-model emulation: ≥16q budget 30–90+ min |
| pytket → compile → execute | H2-1LE/H2-Emulator | 56 | `QuantinuumConfig` | same physics-model cost warning |
| pytket → compile → execute | aer_simulator | ~30 | `AerConfig` — **never** `QuantinuumConfig` (400) | fast statevector |
| Guppy → HUGR → **direct execute** | Helios-1E-lite | 26 (statevector) / **98 (stabilizer)** | `HeliosConfig` + `HeliosEmulatorConfig` | rejects compile jobs by design |
| blocked | sv1 (Braket) | 34 | `BraketConfig` needs AWS S3 | recorded honest gap |

Interpreter: ALL Nexus work runs under the Hermes venv
`/Users/openclaw/.hermes/hermes-agent/venv/bin/python` (qnexus + `~/.qnx/auth`).

## 3 · Operational rules (hard-won)

- **Journal at submit time.** Job IDs to `quantum/*_jobs.json` the moment they
  exist; poll separately. Never put `wait_for` loops in a background process
  that can be SIGTERM'd — receipts must survive process death.
- **Helios Guppy quirks (Hermes-venv guppylang 1.0.x):** no `zz_phase` →
  decompose `CX·Rz·CX`; `output` not `result`; measurement pattern is
  `ms = measure_array(qs)` then `output("c", array(ms[i].read() for i in range(N)))`
  with literal N. Docs pages track v0.21 — never paste doc snippets unmodified.
- **pytket QAOA mixer:** `OpType.Rx` (1 param, halfturns). `PhasedX` takes TWO
  parameters and will throw.
- **`RUNNING, error None` = healthy** on physics-model emulators. Check
  `running_time` via `qnx.jobs.status()` before cancelling anything.
- **98q lane is Clifford-only** (StabilizerSimulator): GHZ, parity/Iceberg-style
  codes. Certifies entanglement scale + tamper-evidence structure, not
  optimization.

## 4 · Canonical receipts (do not contradict)

| Receipt | Job | Claim |
|---|---|---|
| 4q F-VQE trained | `bb1021a2` | 100% optimum mass (256/256), method-validated |
| 26q GHZ Helios | `0fc1f87b` | perfect 512/512, HUGR lane |
| 98q GHZ Helios | `b3d1c274` | perfect 256/256, full published capacity |
| 98q parity receipt | `8eddb96d` | perfect 256/256, Iceberg-style tamper evidence |
| 8q QAOA p=2 | `e7e1a809`+ | honest negative (explores, doesn't concentrate) |

Full tables: `README.md` §4/§9/§12 · `docs/QUANTUM_CARD.md` (the model card —
if a number here drifts from `quantum/*.json`, that is a bug to fix).

## 5 · Team lane (Telegram)

`telegram/dispatcher/nexus_cmd.py` — `/nexus` slash dispatcher (stdlib-only,
qnexus in a Hermes-venv subprocess). `/nexus wardshift [shots] [backend] [fvqe]`
fires this repo's own circuit and auto-appends the honest receipt line.
**Consent gate:** plain-English requests get ONE suggestion (qubits/shots/
backend) and nothing submits without an explicit "yes". Stale-gateway trap:
`Unknown command /nexus` → `/restart`, wait 30 s, retry.

## 6 · Surfaces & sync duties

After any receipt or finding lands: update `README.md` (receipts table +
relevant section), `lovable-content.md` (the Lovable page pack), and
`docs/QUANTUM_CARD.md` if circuits/limits changed. Skill lessons go to
`skills/quantinuum/SKILL.md` (Hermes) and this file (OpenClaw) — keep both
lanes honest. Secret-scan before every push: no tokens, no keys, bot token
stays in `.env`.
