# Clinical Quantum Methodology™ (CQM v1.3)
### *The Agile for Quantum Medicine — Problem First, Quantum Second*
**Association for Clinical Quantum** · Expert Think Tank for NHS Quantum Integration · [clinicalquantum.com](https://clinicalquantum.com)
> *Workflow is the product. Quantum is optional augmentation. Honest negatives are deliverables.*

**Reference implementations:**
1. `arunnadarasa/nhsquantinuum-mentor` (EndoTrack, Quantinuum Singapore Grand Challenge 2026) — H2-Emulator verified, 25 cited signals, 20 DPIA-screened datasets, toy → 101D scale, QPU receipts.
2. `arunnadarasa/tandem-hack-quantum` (WardFlow, NXGN x Tandem Health hackathon 2026) — **CQM executed end-to-end in ONE DAY**: toy-first gate → 6-backend receipts → F-VQE method upgrade (0.1875 → 1.0000) → scale ladder 4q→8q→26q→98q incl. Helios Guppy→HUGR native lane; honest negatives committed at every rung.

---

## 1. Manifesto — 4 Values (Agile lineage)

> We value the Agile Manifesto's spirit, adapted for clinical quantum.

| We value | Over | Because |
|---|---|---|
| **Problem-first over quantum-first** | Demonstration of technology | NICE rejects tech without pathway benefit (NG73, GID-HTG10877). Old repo trap = 97% miRNA alone → fails primary care. |
| **Reproducible workflow over one-off accuracy** | Single AUC | Quantinuum must rerun in 2 years: same seed → same counts. Workflow is what is procured. |
| **Honest negatives over strained positives** | P-hacked advantage | CBET/Cochrane demand pre-registration; negative is still evidence (our 50D Δ -0.007, 101D Δ 0.000). |
| **Clinical safety over speed** | Hype | DPIA/DCS/DCB0129/0160, SAFE, DCB0160 — no personal data in repo, emulator-first. |

**Foundational quote (Quantinuum mentor):** *“Problem first — the tech comes afterwards. Workflow is most important so it is reproducible for Quantinuum to use later. You may realise you don't need quantum.”* — CQM encodes this as gates.

---

## 2. Principles — 12 (one per Agile principle)

1. **Satisfy the patient, not the qubit** — delay (7–8y), QALY, ICER are primary endpoints; fidelity is surrogate.
2. **Welcome changing evidence** — NICE monthly, GWAS yearly; protocol re-scan quarterly (our 5×5 bulletproof scan).
3. **Deliver working workflow frequently** — toy every sprint, scale every 2 sprints, always with QPU receipt.
4. **Clinicians + quantum engineers daily** — Dr Waters beacon (14 slides) steers every quantum choice.
5. **Build around motivated clinicians** — Trust Caldicott/SIRO/DPO sign-offs are dependencies, not blockers.
6. **Face-to-face + Marimo** — co-write in Aqora Marimo; `QPU(platform="nexus:H2-Emulator")` is pairing.
7. **Working workflow is progress** — `marimo check` PASS + `job.counts()` is definition of done.
8. **Sustainable pace, sustainable shots** — 1024 shots, seed 11, cost-aware (H2-Emulator before H2).
9. **Continuous attention to safety** — DCB0129 hazard log 6→2 residual; QH-15+ flagged.
10. **Simplicity — maximise work not done** — 50D toy before 101D; don't claim quantum where classical AUC 0.99 (11KT).
11. **Self-organising teams** — Sub-agents scan journals/datasets (our 5+5 parallel).
12. **Reflect honestly** — Retrospective = NEGATIVE.md; publish it.

---

## 2b. AI → Quantum State Preparation & Decision Gate (2026-09-03 mentor + audit)

**Mentor pathway (Jem Guhit, 2026-09-03):** Multimodal clinical data cannot enter a QPU raw.

```
Symptoms (questionnaires) ─┐
MRI (imaging) ─────────────┼─→ AI preprocessing (CNN / encoder) → latent vector (e.g. MRI 0.8, pain 0.6)
Biomarkers/genomics ───────┘         │                    │
                                    ▼                    ▼
                              qubit rotations  →  quantum circuit (correlations, entanglement)
                                                      │
                                                      ▼
                                              measurement → similarity / clustering / phenotype
```

- Each qubit = one clinical feature (Qubit 1 = MRI score, Qubit 2 = pain score)
- Simple AI first (CNN feature 0.8), gradual enrichment — mitigates hackathon risk
- Minimal qubits toy (2-4q) before scaling; emulator validation before hardware

**Audit decision gate (ENDOTRACK_PHASE1_AUDIT_2026-09-02, GPT-5.6 Sol, read-only):**

> *EndoTrack is not yet one coherent scientific project, and the quantum decision gate is closed. No clinical validation, no patient-level dataset, no measured classical bottleneck, no physical QPU result.*

**CQM v1.1 rule:** Quantum does not earn a role until three preconditions are met **and approved by clinical + IG + quantum review:**

1. **Agreed clinical use case — one population, one decision, prospective ground truth** — audit's recommendation: *preoperative prediction of complex MDT surgery (colorectal/urology) vs specialist imaging alone* — with measurable false-neg/pos harms. This is compatible with mentor's phenotyping if framed as: *phenotype discovery → surgical-need prediction*.
2. **Measured classical bottleneck** — classical baseline (e.g. `IDEA/#Enzian` imaging) run on the same patient-level data, with scaling profile (time/memory vs n/D). No bottleneck → no quantum.
3. **Patient-level dataset present** — operative findings as ground truth, not pseudobulk means; DPIA/DCS approved, `n≥240`, `n<10` suppression, retention/pentest.

Until gate opens, **pause implementation** — no new circuits/datasets pushed to `main` without PR approval. Reproducibility, evidence-ledger and safety work continue.

**Reconciled use case for EndoTrack (research, not decision support):**

> *Whether preoperative multimodal phenotypes (symptoms + MRI latent vectors) predict need for complex multidisciplinary surgery better than structured specialist imaging alone — with phenotype discovery (mentor) as feature engineering for the prediction task (audit).*

## 3. Lifecycle — 7 Phases (with Agile sprint mapping)

```
Phase 0  Discovery (Problem)          ─┐
Phase 1  Data Shape (DPIA GREEN)       │  Sprint 0: Blueprint  ← GATE CLOSED until use case + bottleneck + dataset approved
Phase 2  Bulletproof Protocol          ─┘
Phase 3  Toy (50D, n~400)               Sprint 1: Toy (PAUSED per audit until gate opens)
Phase 4  Scale (101D→10kD, n 600→10k)   Sprint 2..N: Scale
Phase 5  Minimum Quantum Advantage      Gate: Go/No-Go
Phase 6  Clinical Integration (NHS)     Sprint N+1: Care pathway
Phase 7  Surveillance (DCS in-vivo)     Continuous
```

### Phase 0 — Discovery (1 week)
- Define use case with clinician (slides 7–8 problem, not tech), value (delay, cost £78B US, QALY 0.049).
- Output: `configs/use_case.json`, `docs/use-case-definition.md`.

### Phase 1 — Data Shape (DPIA by design)
- List modalities (our 100–200D: 80 loci + TWAS 99 + 11KT + imaging), schemas (`schemas/`), provenance.
- DPIA screening: GREEN synthetic public vs AMBER controlled (UKB/All of Us). **No personal data in repo.**
- Output: `docs/qtda_datasets.md`, `results/dpia_screening_*.md`.

### Phase 2 — Bulletproof Protocol (2 weeks, think-tank grade)
- Parallel journal scan 5 domains (Biomarker/Genomics/Imaging/Economics/Guidelines) → 25 signals, DOIs.
- Beacon/laser: where classical loses (epistasis 1,709 combos 66–76% repl., PRS 5–8% h², TWAS 1,089 pairs, #Enzian fusion) — **not diagnosis where classical 0.99.**
- Reject gates (NICE NG73 1.5.x, #Enzian, QUADAS-2).
- Output: `docs/bulletproof_protocol_signals.md` + Do/DON'T.

### Phase 3 — Toy (2 weeks, Brian Johnson 42-day → 1 sprint)
- Lock config: `n_genes 50, n 400, seed 11`, 10-loci overlap + 11KT proxy, `go_threshold 0.03`.
- Generate synthetic FinnGen marginals, classical LinearSVC + Ripser baseline, quantum IQP RotorMap on **H2-Emulator** (Aqora `QPU` → `AutoRebase(GATESET)` 9 gates).
- Produce QAS receipt: `{backend_qualifier: emulator, shots, seed, commit, count, fidelity}`.
- Output: `data/synthetic/toy_*`, `notebooks/qtda_toy_quantum.py`, `results/phase2_toy_model/toy_run_*` + `NEGATIVE.md` if |Δ|≤0.03.

### Phase 4 — Scale (iterative, 50 → 101 → 1k → 10kD)
- Same seed line, scale factors locked: `configs/scale_80_twas.json` (80+20+1=101D, 600×101, PCA-12 → 12q ZZPhase 0.35, 300 shots).
- Classical baseline at each scale; quantum kernel same GATESET. Track time/memory vs fidelity.
- Output: `results/scale_*.json`, TDA Betti persistence.

### Phase 5 — Minimum Quantum Advantage (MQA)
- Define MQA: smallest D where |Δ|>0.03 **and** classical time >10× quantum **and** ICER dominates.
- Current toy/scale: Δ -0.007 / 0.000 → NO-GO (honest). Report, don't hide. Scale to real manifolds (GSE213216 370k cells, GZUCMEMsdata 781 TVUS) where classical PH intractable.
- Output: `results/phase2_toy_model/NEGATIVE*.md`, `results/scale_summary_*.md`.

### Phase 6 — Clinical Integration (NHS pathway)
- Second-line after negative TVUS (GID-HTG10877), #Enzian structured reporting (IDEA/ESUR), referral to specialist imaging; never rule-out on negative imaging.
- DCB0129 hazard log, DSPT, Cyber Essentials, retention/pentest — mirroring Lovable app 3-surface `clinicalSafety`.

### Phase 7 — Surveillance
- PROMS, QALY prospective, incident reporting, model retraining n≥240, rare-cell <10 suppression.

---

## 4. Roles (Scrum lineage)

| Role | CQM Name | Owns | Artefact |
|---|---|---|---|
| Product Owner | **Clinical Lead** (e.g. FRANZCOG) | Beacon, pathway, reject gates | Waters 14 slides |
| Scrum Master | **Quantum Safety Officer** | DPIA/DCB0129/0160, SAFE, QAS | Hazard log |
| Dev Team | **Quantum Engineer(s)** | Marimo QPU, GATESET, receipts | `notebooks/*.py` |
| Stakeholder | **IG/Caldicott/SIRO/DPO** | Sign-offs 4/5 | DPIA screening |
| Think Tank | **Association for Clinical Quantum** | Methodology, literacy, guidance | This doc |

---

## 5. Ceremonies & Artefacts

**Ceremonies:** Sprint Planning (lock config), Daily Marimo (pair `aqora login`), Toy Demo (counts + fidelity), Scale Review (Δ + ICER), Retrospective (NEGATIVE.md), Protocol Re-scan quarterly.

**Artefacts:**
- **QAS Envelope** `schemas/qas-envelope-0.1.json`: `backend_qualifier` (emulator/hardware), `platform`, `shots`, `seed`, `commit`, `counts`, `fidelity`, `hash` (SHA-256).
- **Evidence Ledger** `results/evidence_manifest.json`: append-only, hash-chained.
- **DPIA Bundle:** prospective DPIA (IG/Caldicott/SIRO/DPO), DPIA screening per dataset, DCS hazard log.

**Definition of Done (per story):**
1. `marimo check` PASS, `pytest` PASS, `GATESET` rebased
2. QPU receipt committed (emulator OK)
3. Classical baseline logged + comparison
4. Go/No-Go evaluated, NEGATIVE.md if NO-GO
5. No personal data committed (git hook)

---

## 6. Backends & Reproducibility (Quantinuum 2-year test)

| Backend | Platform string | Status 2026-09-02 | Use |
|---|---|---|---|
| **H2-Emulator** | `nexus:H2-Emulator` | **PASS** 53/47 @100 shots fidelity 1.0, 8q 199/200 @200 shots, 50 gates | Toy/scale default |
| H2-1SC/2SC | `nexus:H2-1SC/2SC` | PASS 10×00 (needs 100-shot retry) | SC calibration |
| H2-1/2 | `nexus:H2-1/2` | FAIL LookupError (not exposed) | Future via Julian templates |
| Nexus direct | `qnexus H2-1LE` | Closed per Irfan (11KT decoy) | Local verify only, not submission |

Repro script (Hermes venv):
```bash
/Users/openclaw/.hermes/hermes-agent/venv/bin/python -c "
import subprocess, os
import numpy as np
tok=subprocess.check_output(['/Users/openclaw/.hermes/hermes-agent/venv/bin/aqora','auth','token']).decode().strip()
os.environ['AQORA_TOKEN']=tok
from pytket.circuit import Circuit; from aqora import QPU; from aqora.pytket.backend import GATESET; from pytket.passes import AutoRebase
c=Circuit(2,2); c.H(0); c.CX(0,1); c.measure_all(); AutoRebase(GATESET).apply(c)
print(QPU(platform='nexus:H2-Emulator').run(c, shots=100).counts(timeout=600)[0])
"
# → {'00': 53, '11': 47} fidelity 1.0
```

**Two-year reproducibility:** same `seed 11`, `aqora==0.29.0`, `pytket==2.18.1`, `GATESET` hermetic. Re-run `data/synthetic/*.npz` (hash `818bfb7847e7`) → same QPU counts ± noise; evidence ledger hash-verified.

---

## 7. How to Apply to Any Clinical Use Case (Blueprint)

1. **Swap the beacon:** Replace Waters slides with your clinician's 10 slides (e.g. cardiology: HFpEF phenotyping; oncology: 100-gene panel). Keep Phase 0–2 structure.
2. **Swap dimensions:** Map your modalities to `fusion_dims` (genomics + transcriptomics + proteomics + imaging + wearables). Lock MQA hypothesis (where classical PH/kernels intractable).
3. **Keep toy:** 50D → scale ladder unchanged; only `configs/toy_model_50.json` values change.
4. **Keep gates:** NICE/ESHRE/QUADAS reject gates → your specialty's guideline gates.
5. **Keep safety:** Same DPIA 4 sign-offs, DCB0129, SAFE n≥240, emulator-first.

Template repo: duplicate `nhsquantinuum-mentor`, replace `docs/bulletproof_protocol_signals.md` + `configs/*.json` + `data/`; methodology stays.

---

## 8. Reference Implementation (this repo)

| Phase | Artefact | Status |
|---|---|---|
| 0–2 | `bulletproof_protocol_signals.md` (25 signals), `qtda_datasets.md` (20) | ✓ Done |
| 3 Toy | 50D 0.875 LIN → quantum -0.007 NO-GO | ✓ Honest negative |
| 4 Scale | 101D (80+20+1) LIN 0.641 > RBF 0.590 → quantum 0.528 Δ 0.000 NO-GO; QPU 8q 0.995 | ✓ Honest negative |
| Next | Real GSE213216 370k cells + UT-EndoMRI 133 where TDA hard | **PAUSED** — awaiting gate (use case + dataset + benchmark approval) |

Methodology provenance: Quantinuum mentor feedback + Bryan Johnson 42-day proof + Association for Clinical Quantum think-tank standards.

---

## 8b. Audit & Pause Protocol (2026-09-02/03)

- **Audit:** `ENDOTRACK_PHASE1_AUDIT_2026-09-02.md` 940 lines, SHA `9dd7ec9...`, 24 sections, 10 next actions — read-only, no code changed. Verdict: quarantine SwarmWorld/frontier, freeze public site claims until ledger validated, rotate token fragment, port via PRs.
- **Baseline:** `audit-baseline-2026-09-03` tag @ `a947c83` (real `H2-Emulator` 689-gate), `A/B trace` in `docs/audit_baseline_trace_2026-09-03.md`.
- **Pause:** No `main` pushes for new science until clinical + IG + quantum approval of use case + data spec + classical benchmark. Docs/traces allowed via PR.

---

## 9. Governance

Versioned `CQM v1.3` (2026-09-05 pm) — v1.2 + WardFlow same-day validation (second
reference implementation, one-day scale ladder, method-upgrade rule, wording rule,
Clifford scale lane). `v1.2` (2026-09-05 am) was Jem team-feedback integration (timeline
gates, decision-support endpoint, toy-first gate, phased-AI rule, team roles).
`v1.1` (2026-09-03) was mentor + audit integration; `v1.0` (2026-09-02) toy→scale
baseline. Amend via PR to `docs/clinical-quantum-methodology.md` with clinical +
safety + quantum review (like NICE). No membership — open expert committee per
Association model.

## 10. CQM v1.2 — Jem team-feedback integration (2026-09-05)

Source: team session with Jem Guhit (quantum), Alexandre (mentor), Natasha
(clinical lead), Sai Moody (tech lead), Shreya + Harlan (research), Liana +
Arunpirasath (clinical/data). What v1.1 already covered is not repeated —
only deltas that change gates, roles, or timelines.

### New timeline gates (hackathon-bound)
- **15 Oct checkpoint:** initial deliverables (toy + baseline + receipts).
- **November completion:** 3-month window. Jem's rule: narrow the clinical
  problem to fit the window — no scope that can't land by November.
- Ceremonies bend to reality: 30-minute slots, async updates by email/docs,
  decisions recorded (not re-debated) at the next slot.

### Decision-support endpoint (measurable, new beside delay/QALY)
- **Reduce unnecessary surgeries and emergency admissions** via better
  stratification and treatment planning (Natasha: delays up to 9.6 years,
  current approaches fail to predict response or personalise care).
- Lifetime lens: safer, cheaper, more effective pathways — the metric a board funds.

### Alexandre's toy-first gate (now explicit)
- No scaling spend until a **minimal-qubit toy** (2–4q) demonstrates the
  mechanism on the anchored use case. v1.1 said "toy every sprint" — v1.2
  makes the toy a *gate*: fail the toy bar (|Δ| vs classical on the same
  split, pre-registered) and scaling does not start.

### Phased AI simplicity (risk rule)
- First pass: simple encoders only (CNN image score e.g. 0.8, symptom scores).
  Enrich gradually as data + integration understanding grows. Each enrichment
  must re-pass the classical baseline before touching quantum.

### Roles update (section 4 mapping)
- Tech lead: **Sai Moody** (owns execution + data pipeline).
- Research/content: **Shreya + Harlan** (lit survey threads, technical research).
- Clinical insight + data organisation: **Arunpirasath, Natasha, Liana**.
- Open item: **Jem's email** (AI→quantum encoding diagrams) — tracked in
  `docs/jem-ai-models.md`; nothing downstream waits silently, the tracker does.

**Hermes workshop gold:** `docs/research/shritesh-hermes-gold.md` — Shritesh Hermes + local Qwen (freeCodeCamp × Encode) → cron morning-briefing pattern, 113 ms FTS memory, multi-agent team mapping to CQM roles, mem0 upgrade path. Informs CQM cron design (compare-with-memory digest, self-improving skills).


## 11. CQM v1.3 — WardFlow same-day validation (2026-09-05 pm)

The Tandem hackathon (`arunnadarasa/tandem-hack-quantum`) proved CQM compresses from
sprints to **hours** without dropping a gate. New deltas:

### The methodology scales DOWN (one-day mode)
Phase 0→5 executed in a single day on WardFlow (ward-round job list): problem
(handover proof gap) → DPIA GREEN (synthetic jobs only) → pre-registered protocol
(edges, angles, shots, bar in JSON before any submission) → 4q toy on 6 backends →
honest negative → method upgrade → scale. Rule: **in hackathon mode every ceremony
becomes an artifact commit** — the protocol JSON is sprint planning, the receipts JSON
is the demo, NEGATIVE notes in the README are the retrospective.

### Method-upgrade rule (new gate between Phase 3 and 4)
A failed/weak toy bar does NOT immediately close the door — it triggers ONE
literature-grounded method upgrade before the verdict is final. WardFlow: unoptimized
QAOA p=1 opt-mass 0.1875 (weak PASS) → **F-VQE (Amaro et al. 2022, Quantum Sci.
Technol. 7 015021, Quantinuum authors) → opt-mass 1.0000 on H1-1LE (job `bb1021a2`,
256/256 shots)**. Constraint: the upgrade must be a *published, cited* method (vendor
methods preferred), re-run under the same pre-registered bar. Homebrew tweaking of
angles/thresholds after seeing data remains forbidden.

### Wording rule (binding, new)
Emulator scale runs are **"hardware-scale readiness"**, never "quantum advantage".
Advantage is exclusively a pre-registered future claim gated on real QPU + matched
classical baselines. Applied to 26q and 98q Helios runs; belongs in every CQM report.

### Clifford scale lane (new Phase 4 option)
Beyond ~30 qubits statevector is physically impossible; the honest big-n lane is the
**stabilizer simulator (Clifford-only)** — which constrains circuit choice to GHZ,
parity/Iceberg-style codes, rep-codes. WardFlow: 98q GHZ + 98q block-parity receipt
(arXiv:2504.21172 pattern) on Helios-1E-lite, both 256/256 perfect (jobs
`b3d1c274`/`8eddb96d`). Rule: state the simulator class in the receipt; a stabilizer
run certifies entanglement-scale and tamper-evidence structure, not optimization.

### Dual-lane execution (Nexus, verified)
Two independent submission lanes now proven: **pytket → compile → execute** (H1/H2
lanes, Aer via `AerConfig` — NOT `QuantinuumConfig`) and **Guppy → HUGR → direct
execute** (Helios; compile jobs rejected by design). Cross-lane agreement on the same
problem is a cheap reproducibility check (CQM §6 two-year test, now cross-lane too).

### Receipt discipline additions
- **Journal at submit time**: job IDs written to disk the moment they exist;
  wait/poll separately. A timed-out process must never take its receipts with it.
- **Backend-specific config classes** are part of the receipt (config class name
  recorded), after the `QuantinuumConfig`-on-Aer 400 failure.

### Persona artifact (new)
The operating persona is now versioned in-repo: `AGENT_SOUL.md` (world-class clinical
quantum agent engineer — creed, operating loop, voice) + `skills/quantinuum/SKILL.md`
(executable pitfalls). Together they make the methodology *agent-portable*: any capable
agent loaded with both reproduces the working style. This is CQM's answer to the
"reproducible for Quantinuum in 2 years" test at the level of *practice*, not just data.

|**Cite:** `Association for Clinical Quantum. Clinical Quantum Methodology v1.3 — The Agile for Quantum Medicine. clinicalquantum.com. Reference implementation: NHSquantinuum-mentor.`

*Contact: via clinicalquantum.com Join Discussion · NHS Learning Hub Quantum Course for literacy.*
