# CSC-QT readiness

The Clinical Safety Case Quality Tool (Oskrochi & Grimes, BMJ Innovations 2026), hosted at
https://csc-qt.curistica.com/, reviews 36 indicators across five domains. It produces no
score, no percentage and no pass mark by design. Publish readiness per domain, never a grade.

## The five domains and where our evidence sits

| Domain | What it asks | Our evidence |
| --- | --- | --- |
| Scope and context | Is the intended use, clinical setting and decision-support boundary stated? | Intended-use statement plus the explicit medical-device line |
| Risk management process | Is the process published, not just described? | Hazard schema, 5×5 matrix, acceptability bands, release gate — all rendered |
| Hazard identification and analysis | Are the real failure modes present? | The quantum-specific modes most tools omit: non-determinism, emulator divergence, coherence drift, leakage-induced correlated error, mitigation-read-as-correction, silent fallback |
| Risk control and evidence | Does each control point at evidence? | Every control links to a live artefact on the site — the usual weak point, fixed by the anchoring layer |
| Governance and lifecycle | Who releases, and how does incident feedback return? | Named registered CSO with release authority, CSCR uplift per release, incidents feed the hazard log |

## Rules

- Do not total the domains, average them, or express readiness as a fraction.
- A domain claim must point at something a reviewer can open. "Documented internally" is
  not a readiness claim.
- When a domain is weak, publish it as weak. Readiness that is uniformly strong across five
  domains for a pre-deployment tool is not credible and reads as such.
