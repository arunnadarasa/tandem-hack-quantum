#!/usr/bin/env python3
"""26q on Helios-1E-lite via Guppy -> HUGR direct execute (no compile jobs).
Generates an unrolled Guppy kernel (no qubit-array iteration), compiles to
HUGR, uploads, executes with HeliosConfig. Journals job ID immediately."""
import time, json, sys, tempfile, importlib.util, random
from pathlib import Path
import qnexus as qnx
from quantinuum_schemas.models.backend_config import HeliosConfig, HeliosEmulatorConfig
from quantinuum_schemas.models.emulator_config import (
    StatevectorSimulator, HeliosRuntime, NoErrorModel)

HERE = Path(__file__).parent
N = 26
random.seed(31)
EDGES = [(i, (i + 1) % N, random.randint(1, 4)) for i in range(N)]
EDGES += [(random.randrange(N), random.randrange(N), random.randint(1, 4)) for _ in range(13)]
EDGES = [(i, j, w) for i, j, w in EDGES if i != j]
GAMMA, BETA, SHOTS = 0.35, 0.4, 512

def render_kernel(kind: str) -> str:
    lines = [
        "from guppylang import guppy",
        "from guppylang.std.builtins import array, owned, output",
        "from guppylang.std.quantum import qubit, h, cx, rx, rz, measure_array",
        "from guppylang.std.angles import angle",
        "",
        "@guppy",
        "def main() -> None:",
        f"    qs = array(qubit() for _ in range({N}))",
    ]
    if kind == "ghz":
        lines.append("    h(qs[0])")
        for q in range(N - 1):
            lines.append(f"    cx(qs[{q}], qs[{q+1}])")
    else:  # qaoa
        for q in range(N):
            lines.append(f"    h(qs[{q}])")
        for i, j, w in EDGES:
            # ZZPhase(a) == CX; Rz(a); CX (this guppylang has no zz_phase)
            lines.append(f"    cx(qs[{i}], qs[{j}])")
            lines.append(f"    rz(qs[{j}], angle({GAMMA * w}))")
            lines.append(f"    cx(qs[{i}], qs[{j}])")
        for q in range(N):
            lines.append(f"    rx(qs[{q}], angle({BETA}))")
    lines.append("    ms = measure_array(qs)")
    lines.append(f"    output(\"c\", array(ms[i].read() for i in range({N})))")
    return "\n".join(lines) + "\n"

def compile_kernel(kind: str):
    src = render_kernel(kind)
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=str(HERE))
    f.write(src); f.close()
    spec = importlib.util.spec_from_file_location(f"k26_{kind}_{int(time.time())}", f.name)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.main.compile()

def main():
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs["NHS Quantum"])
    cfg = HeliosConfig(system_name="Helios-1E-lite",
        emulator_config=HeliosEmulatorConfig(n_qubits=N,
            simulator=StatevectorSimulator(), runtime=HeliosRuntime(),
            error_model=NoErrorModel()))
    jp = HERE / "ward26_jobs.json"
    jobs = json.loads(jp.read_text()) if jp.exists() else {}
    for kind in (sys.argv[1:] or ["ghz", "qaoa"]):
        hugr = compile_kernel(kind)
        href = qnx.hugr.upload(hugr_package=hugr, name=f"ward26_{kind}_helios_{int(time.time())}")
        ej = qnx.start_execute_job(programs=[href], n_shots=[SHOTS],
                                   backend_config=cfg, name=f"exe_ward26_{kind}_helios")
        jobs[f"Helios-1E-lite_{kind}"] = {"execute_job_id": str(ej.id), "shots": SHOTS}
        jp.write_text(json.dumps(jobs, indent=2))
        print(f"SUBMITTED helios {kind} exec={ej.id}")

if __name__ == "__main__":
    main()
