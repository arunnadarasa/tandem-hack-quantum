#!/usr/bin/env python3
"""Submit-only: compile + dispatch execute for one backend, journal job IDs, exit fast.
Usage: ward_shift_submit.py H1-1LE"""
import time, json, sys
from pathlib import Path
import qnexus as qnx
from ward_shift_qaoa import build_circuit, PROTO, HERE

def main():
    dev = sys.argv[1]
    circ = build_circuit()
    projs = {p.annotations.name: p for p in qnx.projects.get_all()}
    qnx.context.set_active_project(projs[PROTO["project"]])
    up = qnx.circuits.upload(circ, name=f"wardshift_{dev}_{int(time.time())}")
    cfg = qnx.QuantinuumConfig(device_name=dev)
    cj = qnx.start_compile_job(programs=[up], backend_config=cfg, name=f"cmp_wardshift_{dev}")
    qnx.jobs.wait_for(cj, timeout=280)
    comp = qnx.jobs.results(cj)[0].get_output()
    ej = qnx.start_execute_job(programs=[comp], n_shots=[PROTO["shots"]],
                               backend_config=cfg, name=f"exe_wardshift_{dev}")
    jp = HERE / "ward_shift_jobs.json"
    jobs = json.loads(jp.read_text()) if jp.exists() else {}
    jobs[dev] = {"execute_job_id": str(ej.id), "compile_job_id": str(cj.id)}
    jp.write_text(json.dumps(jobs, indent=2))
    print(f"SUBMITTED {dev} exec={ej.id}")

if __name__ == "__main__":
    main()
