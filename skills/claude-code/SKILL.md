---
name: wardflow-quantum
description: Quantum capability layer for WardFlow (tandem-hack-quantum). Use when writing, running, or documenting Quantinuum Nexus circuits for this repo — QAOA/F-VQE shift-splits, GHZ/parity receipts, Helios Guppy→HUGR lane — or when editing README/Lovable/card surfaces that cite receipt numbers. Enforces receipt law, honest-negative discipline, and the no-advantage wording rule.
---

# WardFlow Quantum — Claude Code skill

You are working on the quantum capability layer for WardFlow (ward-round job board,
NXGN x Tandem Health hackathon). Load `AGENT_SOUL.md` (persona) and
`docs/clinical-quantum-methodology.md` (CQM v1.3 gates) alongside this skill.
When a general instruction conflicts with this skill, this skill wins.

## Binding rules (non-negotiable)

1. **Classical decides; quantum signs the receipt.** Never present the quantum layer
   as making any clinical or scheduling decision.
2. **Wording rule:** emulator scale runs = "hardware-scale readiness", NEVER
   "quantum advantage". Advantage is a pre-registered future claim only.
3. **Every number carries shots + envelope** `4·sqrt(0.5/shots)`. A number without a
   committed JSON receipt (job ID, counts, verdict) does not exist.
4. **Honest negatives are deliverables.** Report weak results as-is; never smooth.
5. **One method upgrade, then the verdict stands** (CQM v1.3): a weak toy bar earns
   exactly one published, cited method upgrade (e.g. F-VQE, Amaro 2022) re-run under
   the same pre-registered bar. No post-hoc angle/threshold tweaking.
6. **DPIA GREEN:** synthetic dummy jobs only — no patient data, no NHS numbers.
7. **Secret hygiene:** no tokens/keys in commits; bot tokens live in `.env` only.

## How to run circuits (verified recipes)

**Interpreter:** all Nexus work uses `/Users/openclaw/.hermes/hermes-agent/venv/bin/python`
(the only interpreter with `qnexus` + `~/.qnx/auth`). Bash tool: prefix every quantum
command with that path — never bare `python3`.

**Lane map** (config class is load-bearing):

| Backend | Max q | Config | Lane |
|---|---|---|---|
| H1-1LE / H1-Emulator | 20 | `qnx.QuantinuumConfig(device_name=...)` | upload → compile → execute |
| H2-1LE / H2-Emulator | 56 | `qnx.QuantinuumConfig` | same; ≥16q = physics-model emulation, budget 30–90+ min |
| aer_simulator | ~30 | `qnx.AerConfig()` — `QuantinuumConfig` 400s | same |
| Helios-1E-lite | 26 statevector / 98 stabilizer | `HeliosConfig` + `HeliosEmulatorConfig` | Guppy → HUGR → **direct execute** (compile jobs rejected) |
| sv1 (Braket) | 34 | needs AWS S3 — recorded honest gap | blocked |

**Submit-only pattern (mandatory for anything slow):** upload → compile → execute →
write `{backend: execute_job_id}` to `quantum/*_jobs.json` → exit. Poll later with
`qnx.jobs.get(id=...)` + `download_result()`. Never leave `wait_for` loops in a
process that can be killed — receipts must survive process death.

**Helios Guppy quirks (Hermes-venv guppylang 1.0.x):** no `zz_phase` → `CX·Rz·CX`;
import `output` (not `result`) from `std.builtins`; measure via
`ms = measure_array(qs)` then `output("c", array(ms[i].read() for i in range(N)))`
with a literal N; `@guppy` kernels must live in a real .py file (temp-module pattern
in `quantum/ward26_helios.py`). Official docs track guppylang v0.21 — do not paste
doc snippets unmodified.

**pytket traps:** QAOA mixer is `OpType.Rx` (1 param, halfturns) — `PhasedX` takes 2
params and throws. Angles in HALFTURNS everywhere.

**`RUNNING, error None` is healthy** on physics-model emulators — check
`running_time` from `qnx.jobs.status()` before cancelling.

## Canonical receipts (never contradict; source of truth = quantum/*.json)

- 4q F-VQE trained: job `bb1021a2` — 100% optimum mass (256/256), method-validated
- 26q GHZ Helios (HUGR): job `0fc1f87b` — perfect 512/512
- 98q GHZ Helios (stabilizer): job `b3d1c274` — perfect 256/256, full published capacity
- 98q parity receipt: job `8eddb96d` — perfect 256/256, Iceberg-style tamper evidence
- 8q QAOA p=2: `e7e1a809`+ — honest negative (explores, doesn't concentrate)

## Sync duties after any new receipt or finding

Update in the same commit: `README.md` (receipts table + section), `lovable-content.md`
(Lovable page pack), `docs/QUANTUM_CARD.md` (if circuits/limits changed). Card-vs-JSON
drift is a bug. Sibling skills to keep consistent: `skills/quantinuum/SKILL.md`
(Hermes) and `skills/openclaw/SKILL.md` (OpenClaw).

## Repo quick map

`quantum/ward_shift_*.py` 4q toy + F-VQE · `quantum/ward_shift_8q.py` scale step ·
`quantum/ward26*.py` Helios lanes · `quantum/ward98_helios.py` stabilizer finale ·
`telegram/dispatcher/nexus_cmd.py` `/nexus` team lane (incl. `wardshift` subcommand) ·
`docs/QUANTUM_CARD.md` model card · `AGENT_SOUL.md` persona · CQM v1.3 in `docs/`.
