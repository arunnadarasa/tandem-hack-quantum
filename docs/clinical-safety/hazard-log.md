# Authoring a hazard

## Schema

Each hazard in `clinicalSafety.hazards` (in `src/lib/quantum-data.server.ts`) carries:

```text
id          QH-nn, sequential, never reused
hazard      one sentence, the failure itself — not the feature
cause       the concrete mechanism, with the source if external
effect      what reaches the clinician or the patient
situation   HS-nn, the hazardous situation it lands in
harm        Harm-n, with its severity band
initial     1..25 raw product of the 5x5 grid position, before controls
controls    the QC-nn controls already in force
additional  the further control this hazard requires
residual    the rating after initial + additional controls
```

## Procedure

1. Name the failure, not the component. "Emulator result presented as hardware" is a
   hazard; "Selene emulator" is not.
2. Trace it to a hazardous situation already in the register (HS-01..HS-08). If none fits,
   the register is incomplete — add the situation before the hazard.
3. Choose the harm honestly. Most triage failures land on Harm-3 (delay to non-urgent
   treatment). Reserve Harm-4 and Harm-5 for missed serious pathology and permanent harm.
4. Rate the initial risk with the controls **switched off**. Rating it with controls on is
   the most common way a hazard log becomes decorative.
5. Attach existing controls before inventing new ones. Reuse `QC-01`..`QC-10`.
6. Write the additional control as an action someone performs or a gate the code enforces,
   never as an intention.
7. Residual must be justified by the additional control. A drop from 12 to 3 needs a
   control that plausibly moves both severity and likelihood; if it only moves likelihood,
   say so.

## Quantum-specific failure modes already in the register

These are the modes generic health-IT hazard logs omit. Reuse them as the pattern:

- Emulator-vs-QPU divergence — a result that survives the emulator and not the device.
- Shot-noise instability — the same patient ranks differently between runs.
- Silent fallback — a classical path presented as a quantum result.
- Stale or swapped cohort provenance.
- Mitigation read as correction — error mitigation described as error correction.
- Leakage-induced correlated error and coherence drift on hardware.
- Agent action taken without a named human approval.
- Harvest-now/decrypt-later exposure and ECDSA/secp256k1 signing exposure.
- Tuned result reported without its search budget, against an untuned baseline.
- External claim graded by the word "quantum" in its title rather than its backend.

## Rules

- Hazards are never closed, only controlled. There is no "resolved" state.
- A hazard whose residual sits at 4 or 5 blocks deployment; say that in the row rather than
  softening the rating.
- When an external paper or regulator changes what we may claim, log a hazard for it and
  cite the source inside `cause`. That is how QH-18 through QH-23 entered the register.
