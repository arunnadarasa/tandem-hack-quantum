# Standards, scope and the regulatory horizon

## DCB0129 — manufacturer

WardFlow is health IT intended to support a clinical pathway decision, so manufacturer
clinical risk management applies. Required before any deployment: a hazard log, a Clinical
Safety Case Report (CSCR), and a named Clinical Safety Officer who is a registered clinical
professional. Ours is Arun Nadarasa, GPhC 2080128.

## DCB0160 — deploying organisation

A trust deploying WardFlow runs its own clinical risk management: local hazard
assessment, local controls, training, and a local CSO signing the deployment safety case.
Never present our DCB0129 work as discharging a trust's DCB0160 duty.

## DTAC section C1

C1 requires either DCB0129 conformity or an exceptional rationale for non-applicability,
established from the stated intended use. We do not claim non-applicability. Saying so
plainly is stronger than an argued exemption.

## The medical-device boundary

Ranking for human review is decision support. Any change that lets the system act on the
ranking without a clinician — auto-discharge, auto-referral, autonomous booking — crosses
into UK MDR device territory and must not ship under this safety case. When a feature
request approaches that line, say which side it falls on before estimating it.

## DPIA and data protection

The DPIA is written prospectively, while no real patient data is in scope. Risks are `DP-nn`
and each row is anchorable. ICO Tech Horizons 2025 (quantum sensing and imaging in
healthcare) is the regulator's own horizon scan and sets the expectations the DPIA answers.
The UK Data (Use and Access) Act 2025 applies to any future live deployment.

## Regulatory horizon

- **EU AI Act** — enforced since 2 August 2026. Interactive AI must disclose that it is AI;
  generated or altered content must be labelled and machine-readable marked. Our disclosure
  copy exists; provenance marking on exported artefacts does not. That gap is logged as a
  hazard, not claimed as done.
- **FDA CDRH generative-AI discussion paper (August 2026)** — adopted as design discipline
  only: total-product-life-cycle framing, the consequences axis, safety-critical escalation,
  sequestered benchmarks, postmarket monitoring. Cite it as a request for feedback.
- **NICE HTG10877** early use guidance frames the endometriosis pathway itself.

## How to cite

Name the instrument, its version or date, and what it obliges. Never cite a standard as
evidence that we comply with it — cite it as the obligation we are writing against, and put
our actual status next to it.
