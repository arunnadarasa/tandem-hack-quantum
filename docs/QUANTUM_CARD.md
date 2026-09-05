# QUANTUM_CARD.md — WardFlow Quantum Capability Layer

*Quantum model card per Everitt & Ji, "Model Cards for Quantum Technologies Reporting"
(arXiv:2412.13151), crossed with the NVIDIA-verified skill-card template
(docs.nvidia.com/skills — cataloged / scanned / evaluated / documented). One card, both
disciplines: quantum-technology transparency + agent-skill trust.*

---

## 1. Entity Details

| Field | Value |
|---|---|
| **Name** | WardFlow Quantum Capability Layer (shift-split receipts) |
| **Version** | 1.0 (2026-09-05, single-day build) |
| **Owner** | Arun Nadarasa · Association for Clinical Quantum · NXGN x Tandem Health hackathon team |
| **Repository** | [`arunnadarasa/tandem-hack-quantum`](https://github.com/arunnadarasa/tandem-hack-quantum) |
| **License** | Open (hackathon artifact); Quantinuum Nexus T&Cs govern backend access |
| **Entity type** | Hybrid quantum-classical capability: QUBO formulation + QAOA/F-VQE circuits + GHZ/parity attestation programs + receipt pipeline |
| **Methodology** | Clinical Quantum Methodology v1.3 ([`docs/clinical-quantum-methodology.md`](clinical-quantum-methodology.md)) |

## 2. Intended Use

| Field | Value |
|---|---|
| **Primary use case** | Tamper-evident execution receipts for ward-round handover: the classical WardFlow job sort stays the decision-maker; the quantum layer stamps the agreed shift-split with a checkable sampling fingerprint |
| **Intended users** | Hackathon judges, NHS digital teams evaluating quantum readiness, clinical quantum researchers |
| **Out-of-scope uses** | ❌ Clinical decision-making · ❌ patient-data processing (synthetic jobs only, DPIA GREEN) · ❌ any claim of quantum speed/accuracy advantage · ❌ production deployment |

## 3. Quantum System Characteristics

| Field | Value |
|---|---|
| **Hardware family** | Quantinuum trapped-ion (QCCD): H1 (20q), H2 (56q racetrack), Helios (98q tuning-fork, Ba⁺) |
| **Execution tier** | **Emulators only** (H1-1LE, H2-1LE, noisy H1/H2-Emulator, Helios-1E-lite, Aer). No QPU run claimed |
| **Simulator classes** | Statevector (≤26q verified) · Stabilizer/Clifford (98q verified) · noisy physical models (H1/H2-Emulator) |
| **Programming lanes** | pytket → Nexus compile → execute (H1/H2/Aer) · Guppy → HUGR → direct execute (Helios) |
| **Native gates** | 1q rotations, ZZ / parameterized-angle ZZ (per Quantinuum data sheets) |
| **Uncertainty envelope** | `4·√(0.5/shots)` on every probability claim (0.088 at 256 shots, 0.0625 at 512) |

## 4. Circuits & Performance (all receipts live in-repo)

| Circuit | Qubits | Backend(s) | Job ID(s) | Result | Verdict |
|---|---|---|---|---|---|
| Shift-split QAOA p=1 | 4 | H1-1LE, H2-1LE, H1/H2-Em, Aer | `7f8ad56f` +4 | opt-mass 0.125–0.1875 vs 0.125 uniform | weak PASS, reported honestly |
| **Shift-split F-VQE** (Amaro 2022) | 4 | H1-1LE | `bb1021a2` | **opt-mass 1.0000** (256/256 shots) | PASS — method-validated |
| Shift-split QAOA p=2 | 8 | 4 backends | `e7e1a809` +3 | mean-cut > uniform; opt-mass 0.01–0.04 | honest negative |
| Whole-ward QAOA p=1 | 26 | Helios-1E-lite (HUGR) | `67f9d2f4` | mean-cut 43.61 vs 43.05 | explores, doesn't concentrate |
| Whole-ward GHZ | 26 | Helios-1E-lite (HUGR) | `0fc1f87b` | **512/512 shots, GHZ-mass 1.0** | PASS |
| Hospital-scale GHZ | **98** | Helios-1E-lite (stabilizer) | `b3d1c274` | **256/256 shots, 2 outcomes / 3×10²⁹ space** | PASS |
| Parity attestation (Iceberg-style, arXiv:2504.21172) | **98** (90 data + 8 parity) | Helios-1E-lite (stabilizer) | `8eddb96d` | **256/256 shots, parities consistent** | PASS — tamper-evidence structure |

## 5. Evaluation Conditions (Everitt & Ji core requirement)

- **Pre-registered bars**: decision rules fixed in [`quantum/ward_shift_protocol.json`](../quantum/ward_shift_protocol.json) *before* submission; PASS = optimum-mass ≥ uniform − envelope.
- **Classical baselines**: brute-force optimum (4q/8q), 10k-sample uniform-random mean-cut (26q), stated per run.
- **Reproducibility**: seeds fixed (11/31), shots recorded, package pins (guppylang 1.0.x, pytket 2.18.1, qnexus), submit-journal pattern (`ward*_jobs.json`) — job IDs survive process death.
- **Verification gap (honest)**: emulator results are classically simulable by construction; no classically-unverifiable claim exists in this card.

## 6. Limitations & Risks

1. **No quantum advantage** — binding wording rule: emulator scale runs = "hardware-scale readiness". Advantage is a pre-registered future claim gated on real QPU + matched classical baselines.
2. **Unoptimized variational circuits explore, don't concentrate** (8q, 26q QAOA) — F-VQE fixes this at 4q; scaling F-VQE training is untested here.
3. **98q lane is Clifford-only** (stabilizer) — certifies entanglement scale + parity structure, not optimization.
4. **sv1 (Braket) gap** — needs AWS S3; `local=True` hit a Nexus 500. Recorded, not retried blind.
5. **Emulator noise models ≠ hardware** — noisy-emulator receipts approximate but do not replace QPU characterization.

## 7. Trust Controls (NVIDIA skill-card discipline)

| Control | Status |
|---|---|
| **Cataloged** | Skill + persona + methodology versioned in-repo (`skills/quantinuum/SKILL.md`, `AGENT_SOUL.md`, `docs/clinical-quantum-methodology.md`) |
| **Scanned** | Secret-scan before every skill push (no keys/tokens); no hidden instructions; declared purpose matches bundled behavior |
| **Evaluated** | With-vs-without discipline: unoptimized QAOA (without method) vs F-VQE (with) recorded per-dimension — correctness 0.1875→1.0000, all receipts diffable |
| **Signed** | Not yet — future work: detached signatures on receipt JSONs (Merkle-binding pattern exists in the EndoTrack reference implementation) |
| **Documented** | This card |

## 8. Provenance & Citations

- Everitt & Ji, *Model Cards for Quantum Technologies Reporting*, arXiv:2412.13151 (card structure)
- NVIDIA-Verified Agent Skills, docs.nvidia.com/skills (trust-pipeline structure)
- Amaro et al., *Filtering variational quantum algorithms for combinatorial optimization*, Quantum Sci. Technol. 7 015021 (2022) (F-VQE method)
- Jin, He, Amaro et al., arXiv:2504.21172 (Iceberg parity-check pattern)
- Niroula et al., arXiv:2511.03689 (Helios 98q real-time execution)
- Quantinuum H2 & Helios Product Data Sheets (hardware numbers — never invented)

---

*Card version 1.0 · 2026-09-05 · maintained alongside the receipts it describes; a card
whose numbers drift from `quantum/*.json` is a bug.*
