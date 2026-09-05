---
name: telegram-quantum-hermes
description: "Run Nexus, Aqora & Marimo quantum jobs via Telegram. Unified Hermes runner + /nexus slash dispatcher."
version: 1.1.0
metadata:
  hermes:
    tags: [quantum, telegram, nexus, aqora, marimo, quantinuum]
    requires_toolsets: [terminal]
---

# Telegram Quantum Hermes

Two entries: `quantum_telegram.py` (CLI) and `dispatcher/nexus_cmd.py`
(mirrors the live `/nexus` slash dispatcher at
`<hermes-agent>/quantum/nexus_cmd.py`).

## /nexus slash commands (live in Telegram)

help | backends (12 live devices) | pathway [shots] (6q QAOA, H1-1LE) |
pathway_16q [shots] (16q QAOA, H2-1LE) | attestation (2q Hadamard-test
trace, Helios→H1-1LE fallback) | bench [shots] (pathway + attestation
with ±4√(0.5/shots) verdict) | status <id> (full or 8-char prefix) |
jobs [n] | backend <name> (2q Bell health test).

## Plain-English mode (non-technical users)

When the user describes a goal without jargon ("check if the quantum
computer is working", "run my pathway thing"), do NOT ask them for
qubits/shots/backends. Instead reply with one short suggestion message:

> "Here's what I suggest: [1-line plain description], [N] qubits,
> [S] shots on [backend] (free test machine). Reply 'yes' and I'll run it."

Mapping: health/test → Bell 2q, 100 shots, H1-1LE. Pathway/allocation →
6q, 1000 shots, H1-1LE. Bigger problem → 16q, 1000 shots, H2-1LE.
Randomness/attestation → trace circuit, Helios-1E-lite. Full check →
bench, 100 shots. Then run the matching /nexus subcommand and report the
result in one plain sentence + the receipt.

## Cost discipline

Zero-cost first (`help`, `backends`, local Selene smoke). Emulator jobs
(H1-1LE/H2-1LE/Helios-1E-lite) are quota-cheap but still need a "yes".
Never submit without explicit confirmation.
