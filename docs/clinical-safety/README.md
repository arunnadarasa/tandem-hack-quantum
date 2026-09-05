# Quantum Clinical Safety — WardFlow adaptation

Adapted from the EndoTrack clinical-safety pack (Association for Clinical Quantum). Names
and intended use retargeted to WardFlow; the discipline is unchanged.

| File | What it governs |
|---|---|
| [`standards.md`](standards.md) | DCB0129 (manufacturer) vs DCB0160 (deploying trust), DTAC C1, the medical-device boundary, DPIA |
| [`hazard-log.md`](hazard-log.md) | Hazard schema (`QH-nn`), authoring procedure, 5×5 rating with controls OFF, quantum-specific failure modes |
| [`release-gate.md`](release-gate.md) | Four-step release authority: safety tag at planning → hazard assessment → CSCR uplift → named CSO sign-off |
| [`csc-qt.md`](csc-qt.md) | CSC-QT (BMJ Innovations 2026) five-domain readiness — published per domain, never as a score |

**WardFlow scope note (honest):** WardFlow is a hackathon proof of concept — in-memory, no
EPR, no auth, synthetic patients. Nothing here claims deployment readiness. This pack shows
*what the safety case would need to be* before any trust pilot: the hazard schema already
covers the quantum layer's real failure modes (emulator-result-presented-as-hardware,
non-determinism, silent fallback, mitigation-read-as-correction) — the same modes our
receipts and wording rules exist to control.

**Named CSO:** Arun Nadarasa, GPhC 2080128 (per `release-gate.md`). Medical-device line:
WardFlow's sort + quantum receipt is decision support; any auto-action on the ranking
crosses into UK MDR territory and must not ship under this case.
