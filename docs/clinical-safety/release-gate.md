# Clinical authority to release

Follows the NHS CSCR uplift guidance. Four steps, in this order, for every release.

## 1. Safety impact tag at planning

Every change is tagged before work starts: **no safety impact**, **safety-related**, or
**safety-critical**. The tag is written down at planning, not decided retrospectively when
the release is being signed. Anything touching ranking, cohort selection, an agent action,
a disclosure surface or a cryptographic path is at least safety-related.

## 2. Hazard assessment per change

A safety-related or safety-critical change gets a hazard assessment: does it introduce a new
`QH-nn`, change the initial rating of an existing one, or weaken a `QC-nn` control? A change
that weakens a control without a replacement does not proceed.

## 3. Uplifted CSCR

The Clinical Safety Case Report is uplifted per release, not per year. The uplift records
what changed, which hazards were touched, and the residual position after the change.

## 4. CSO sign-off

Release authority rests with the named registered Clinical Safety Officer — Arun Nadarasa,
GPhC 2080128 — signing against the stated intended use. Not a team, not a checklist, not an
automated gate. A residual rating of 3 ships only with an explicit CSO signature; 4 or 5
does not ship.

## Incident feedback

Anything that goes wrong in use returns to the hazard log as a new or re-rated `QH-nn`
before the fix is released. The loop is part of the gate, not a follow-up task.

## What this gate is not

It is not currently exercised against a live deployment. WardFlow is pre-deployment: no
clinical authority to release has been sought or granted. Describe the gate as a mechanism
in place, never as a gate that has been passed.
