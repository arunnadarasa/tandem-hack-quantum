---
name: quantum-clinical-safety
description: Use when a task touches clinical safety for a quantum-assisted health tool — hazards, DCB0129/DCB0160, DTAC, CSCR, DPIA, the risk matrix, safety exports, or any claim about WardFlow being safe to deploy.
---

# Quantum digital clinical safety

Use this skill when writing, editing or reviewing anything that appears in the `#safety`
section of the WardFlow dashboard, in the printable Clinical Safety & Quantum Synergy
report, in a safety export, or in any sentence that says a quantum result is fit for a
clinical pathway.

## The one thing to get right

A safety case is **hazard-led, not feature-led**. A new mechanism is not "safe because it
passed"; it is safe when the ways it can hurt a patient are named, controlled and rated.

Every quantum claim must be expressible as a row with all five parts:

```text
cause → hazard → hazardous situation → harm to a patient → control → residual rating
```

If a claim cannot be written that way, it is a capability statement, not a safety
statement. Do not let it into the safety case.

## Standards to reference (never invent others)

| Instrument | Who it binds | What it demands here |
| --- | --- | --- |
| DCB0129 | Us, as manufacturer | Hazard log, Clinical Safety Case Report, named CSO before any deployment |
| DCB0160 | The deploying NHS organisation | Local hazard assessment, local controls, training, local CSO signature |
| DTAC section C1 | Procurement | DCB0129 conformity, or an exceptional non-applicability rationale we do **not** claim |
| UK MDR | The boundary | Ranking for human review is decision support; acting on the ranking is a device |
| CSCR uplift guidance | Each release | Safety impact tag at planning, hazard assessment per change, uplifted CSCR, CSO sign-off |
| DPIA / UK GDPR, ICO | Data | Written prospectively; ICO Tech Horizons 2025 sets the quantum-in-healthcare expectation |
| EU AI Act (in force 2 Aug 2026) | Disclosure | AI must identify itself; generated content needs machine-readable marking |
| FDA CDRH GenAI discussion paper (Aug 2026) | Design discipline only | Cited as a request for feedback, never as a requirement |

## Fixed project facts — do not restate them differently

- Intended use: rank and triage suspected-endometriosis referrals **for clinician review**.
  No diagnosis, no auto-booking, no discharge. Every state change needs a named approval.
- Lifecycle status: **pre-deployment**. No live patient data has ever entered the system.
  No clinical authority to release has been sought. No NHS organisation has deployed it.
- Clinical Safety Officer: Arun Nadarasa, GPhC 2080128. Release authority rests with a
  named registered individual, not with a team or a process.
- Registers: hazards are `QH-nn`, controls are `QC-nn`, hazardous situations `HS-nn`,
  harms `Harm-n`, DPIA risks `DP-nn`. Anchors are live — `#QH-17`, `#DP-13` must resolve.
- Scale: 5×5, severity Minor→Catastrophic against likelihood Very low→Very high, scored
  1–5. Bands: 1–2 acceptable, 3 undesirable (CSO sign-off), 4–5 unacceptable — do not deploy.

## Claim discipline

- "Planned" and "not started" are publishable statuses. Say them rather than implying done.
- A filename is not a receipt. An engine, shot count, seed and job ID make a receipt.
- Never call a hazard closed. Hazards carry a residual rating and stay open.
- Never claim clinical efficacy, patient-outcome improvement or cost saving. The waiting-list
  argument is capacity, cost and patient experience — outcome claims need outcome evidence.
- Never say the system is quantum-safe end to end while any signature path is ECDSA.
- Emulator is not hardware. Simulated-only external work enters at its own tier, taken from
  the methods section, never from the title.

## CSC-QT readiness — never a score

The Clinical Safety Case Quality Tool (Oskrochi & Grimes, BMJ Innovations 2026) reviews 36
indicators across five domains: scope and context; risk management process; hazard
identification and analysis; risk control and evidence; governance and lifecycle. It
deliberately produces **no score, no percentage and no pass mark**. Publish readiness per
domain. Never compute a total, a percentage or a grade from it.

## Synergy — the two-way argument

Quantum work strengthens the safety case: Merkle-bound cohort provenance means the cohort
behind a result cannot be swapped silently; on-chain anchoring gives an immutable audit
trail; the published negative record supplies the failure evidence that is normally the
weakest part of a safety case.

Clinical safety constrains the quantum work: it forces a hazard frame onto every claim, a
pre-registered KPI gate instead of a moved bar, and a release gate with a named signature.

State both directions. A one-sided version reads as marketing.

## Verification — before declaring a safety edit done

1. Every new hazard has at least one `QC-nn` control and a residual rating.
2. Every control links to a live artefact on the site, not to a description of one.
3. Every register anchor referenced in prose resolves (`#QH-nn`, `#DP-nn`, `#QC-nn`).
4. The PDF and JSON safety exports regenerate and contain the new row.
5. The printable report still builds and the new content appears in it.
6. No sentence added claims deployment, efficacy or a CSC-QT score.

## References

| Task | Read |
| --- | --- |
| Writing or amending a hazard | `references/hazard-log.md` |
| Standards, DTAC, DPIA, regulatory horizon | `references/standards.md` |
| CSC-QT domains and evidence mapping | `references/csc-qt.md` |
| Shipping a release under the safety case | `references/release-gate.md` |
