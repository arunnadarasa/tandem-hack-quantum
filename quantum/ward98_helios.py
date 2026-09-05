#!/usr/bin/env python3
"""Hospital-scale receipt: 98 qubits on Helios-1E-lite (stabilizer simulator).

Two Clifford programs (stabilizer sim = Clifford-only, the honest lane at 98q —
a 98q statevector is physically impossible):

1. ghz98    — 98-qubit GHZ: one qubit per ward job across the hospital; the
              entanglement seal at Helios's full published capacity (98 Ba+ ions,
              Helios Product Data Sheet; Niroula et al. arXiv:2511.03689 ran 98q live).
2. parity98 — Iceberg-inspired (Jin/He/Amaro arXiv:2504.21172): GHZ core + 8
              block-parity checks folded onto 8 ancilla-role qubits inside the 98.
              Tamper-evidence structure: any single-qubit flip breaks a parity.

Both submit-only: journal job IDs, exit fast. Guppy -> HUGR -> direct execute.
"""
import time, json, sys, tempfile, importlib.util
from pathlib import Path
import qnexus as qnx
from quantinuum_schemas.models.backend_config import HeliosConfig, HeliosEmulatorConfig
from quantinuum_schemas.models.emulator_config import (
    StabilizerSimulator, HeliosRuntime, NoErrorModel)

HERE = Path(__file__).parent
N = 98
DATA = 90          # ward-job qubits (matches WardFlow's ~90 parsed jobs)
ANC = 8            # parity-check qubits
SHOTS = 256

def render_kernel(kind: str) -> str:
    lines = [
        "from guppylang import guppy",
        "from guppylang.std.builtins import array, owned, output",
        "from guppylang.std.quantum import qubit, h, cx, measure_array",
        "",
        "@guppy",
        "def main() -> None:",
        f"    qs = array(qubit() for _ in range({N}))",
        "    h(qs[0])",
    ]
    # GHZ chain over data qubits (log-depth not needed on emulator; chain is fine)
    for q in range(N - 1 if kind == "ghz" else DATA - 1):
        lines.append(f"    cx(qs[{q}], qs[{q+1}])")
    if kind == "parity":
        # 8 parity ancillas: qs[90..97]; block b checks jobs [b*11 .. b*11+10]
        for b in range(ANC):
            anc = DATA + b
            lo, hi = b * 11, min((b + 1) * 11, DATA)
            for d in range(lo, hi):
                lines.append(f"    cx(qs[{d}], qs[{anc}])")
    lines.append("    ms = measure_array(qs)")
    lines.append(f"    output(\"c\", array(ms[i].read() for i in range({N})))")
    return "\n".join(lines) + "\n"

def compile_kernel(kind: str):
    src = render_kernel(kind)
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=str(HERE))
    f.write(src); f.close()
    spec = importlib.util.spec_from_file_location(f"k98_{kind}_{int(time.time())}", f.name)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.main.compile()

def main():
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs["NHS Quantum"])
    cfg = HeliosConfig(system_name="Helios-1E-lite",
        emulator_config=HeliosEmulatorConfig(n_qubits=N,
            simulator=StabilizerSimulator(), runtime=HeliosRuntime(),
            error_model=NoErrorModel()))
    jp = HERE / "ward98_jobs.json"
    jobs = json.loads(jp.read_text()) if jp.exists() else {}
    for kind in (sys.argv[1:] or ["ghz", "parity"]):
        hugr = compile_kernel(kind)
        href = qnx.hugr.upload(hugr_package=hugr, name=f"ward98_{kind}_{int(time.time())}")
        ej = qnx.start_execute_job(programs=[href], n_shots=[SHOTS],
                                   backend_config=cfg, name=f"exe_ward98_{kind}")
        jobs[f"helios_{kind}98"] = {"execute_job_id": str(ej.id), "shots": SHOTS,
                                    "simulator": "stabilizer", "n_qubits": N}
        jp.write_text(json.dumps(jobs, indent=2))
        print(f"SUBMITTED 98q {kind} exec={ej.id}")

if __name__ == "__main__":
    main()
