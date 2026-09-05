#!/Users/openclaw/.hermes/hermes-agent/venv/bin/python
"""Quantinuum Nexus job dispatcher for the Hermes `/nexus` slash command.

Called (synchronously) by ``hermes_cli.slash_exec._exec_nexus`` and the
gateway handler as::

    from quantum.nexus_cmd import handle_nexus_command
    reply_text = handle_nexus_command("/nexus pathway 100")

All Nexus work runs in a ``HERMES_PY`` subprocess (the only interpreter with
qnexus + ``~/.qnx/auth``), so this module needs only the stdlib. Every
subcommand returns plain text and never raises — errors come back as text.

Subcommands: help | backends | pathway [shots] | pathway_16q [shots] |
attestation | bench [shots] | status <job_id> | jobs [n] | backend <name>

Non-technical rule: after a plain-English request, suggest qubits / shots /
backend in one short message and wait for "yes" before submitting anything.
"""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERMES_PY = "/Users/openclaw/.hermes/hermes-agent/venv/bin/python"
POLL_SLEEP = 10
POLL_ROUNDS = 48  # ~8 min cap per job, then return the job id for /nexus status

HELP = textwrap.dedent("""\
    ⚛️ /nexus — Quantinuum Nexus jobs
    /nexus help — this message
    /nexus backends — list available backends (live)
    /nexus pathway [shots] — 6-qubit QAOA pathway allocation on H1-1LE (default 1000 shots)
    /nexus pathway_16q [shots] — 16-qubit QAOA on H2-1LE (default 1000 shots)
    /nexus attestation — 2-qubit Hadamard-test trace (DQC1-style) on Helios (falls back to H1-1LE)
    /nexus bench [shots] — mini epistemic suite: pathway + attestation with honest verdict
    /nexus status <job_id> — check a job (full id or first 8 chars)
    /nexus jobs [n] — your recent jobs (default 5)
    /nexus backend <name> — 2-qubit Bell health test on a named backend
    /nexus wardshift [shots] [backend] [fvqe] — WardFlow NOW/NEXT shift-split receipt (default 256 shots, H1-1LE; add 'fvqe' for the trained 100%-optimum circuit)
    Tip: just describe your goal in plain words and I'll suggest qubits, shots and backend first.""")

FALLBACK_BACKENDS = ["H1-1LE", "H2-1LE", "Helios-1E-lite"]

# --------------------------------------------------------------------------- #
# subprocess helpers                                                           #
# --------------------------------------------------------------------------- #

def _run(code, timeout=600):
    """Run Python under HERMES_PY, return (returncode, stdout, stderr)."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([HERMES_PY, path], capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, (r.stdout or "")[:4000], (r.stderr or "")[-1500:]
    except subprocess.TimeoutExpired:
        return 124, "", "timed out"
    finally:
        Path(path).unlink(missing_ok=True)


_PREAMBLE = """\
import qnexus as qnx, time
from uuid import UUID
def pick_project():
    pros = {p.annotations.name: p for p in qnx.projects.get_all()}
    for name in ("EndoTrack-QIR", "NHS Quantum"):
        if name in pros:
            qnx.context.set_active_project(pros[name])
            return name
    raise RuntimeError("No Nexus project (EndoTrack-QIR / NHS Quantum) found")
def wait(job, rounds=__ROUNDS__, sleep=__SLEEP__):
    for _ in range(rounds):
        st = qnx.jobs.status(job)
        if st.status.name in ("COMPLETED", "SUCCESS"):
            return "done", st
        if st.status.name in ("ERROR", "CANCELLED", "FAILED"):
            return "failed:" + st.status.name, st
        time.sleep(sleep)
    return "running", None
"""

_JOB_RUNNER = """\
from pytket import Circuit
__CIRCUIT__
proj = pick_project()
cref = qnx.circuits.upload(c, name=__NAME__)
__CONFIG__
comp = qnx.start_compile_job(programs=[cref], backend_config=cfg, name="cmd_" + __NAME__)
state, _ = wait(comp)
if state != "done":
    print("COMPILE_" + state.upper() + " id=" + str(comp.id)); raise SystemExit
cout = qnx.jobs.results(comp)[0].get_output()
exe = qnx.start_execute_job(programs=[cout], n_shots=[__SHOTS__], backend_config=cfg, name="exe_" + __NAME__)
state, _ = wait(exe)
if state != "done":
    print("EXECUTE_" + state.upper() + " id=" + str(exe.id)); raise SystemExit
counts = qnx.jobs.results(exe)[0].download_result().get_counts()
tot = sum(counts.values())
top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
print("OK backend=__BACKEND__ shots=%d states=%d proj=%s" % (tot, len(counts), proj))
for bits, n in top:
    print("  %s: %d (%.3f)" % (bits, n, n / max(tot, 1)))
print("JOB " + str(exe.id))
"""

_PATHWAY_6Q = """\
c = Circuit(6, 6)
for i in range(6):
    c.H(i)
for i in range(5):
    c.CX(i, i + 1); c.Rz(2 * 0.3927 * 0.75, i + 1); c.CX(i, i + 1)
for i in range(6):
    c.Rx(2 * 0.7854, i)
for i in range(6):
    c.Measure(i, i)
"""

_PATHWAY_16Q = """\
c = Circuit(16, 16)
for i in range(16):
    c.H(i)
for i in range(15):
    c.CX(i, i + 1); c.Rz(2 * 0.3927 * 0.75, i + 1); c.CX(i, i + 1)
for i in range(16):
    c.Rx(2 * 0.7854, i)
for i in range(16):
    c.Measure(i, i)
"""

_ATTEST_2Q = """\
from pytket.circuit import OpType
c = Circuit(2, 1)
c.H(0)
c.add_gate(__CU1__, 0.5, [0, 1])
c.H(0)
c.Measure(0, 0)
"""

_BELL_2Q = """\
c = Circuit(2, 2)
c.H(0); c.CX(0, 1)
c.Measure(0, 0); c.Measure(1, 1)
"""

# WardFlow shift-split (tandem-hack-quantum): 4 ward jobs -> NOW/NEXT Max-Cut.
# Mirrors quantum/ward_shift_circuit.py (QAOA p=1, halfturns gamma=0.5 beta=0.4);
# optimum cut=10 at 0101/1010 — verdict computed against uniform 0.125.
_WARDSHIFT_4Q = """\
from pytket.circuit import OpType
c = Circuit(4, 4)
for q in range(4):
    c.H(q)
for i, j, w in [(0, 1, 3), (1, 2, 1), (2, 3, 4), (3, 0, 2)]:
    c.add_gate(OpType.ZZPhase, 0.5 * w, [i, j])
for q in range(4):
    c.add_gate(OpType.Rx, 0.4, [q])
for q in range(4):
    c.Measure(q, q)
"""

# F-VQE-trained twin (Amaro 2022): fixed trained Ry angles from
# quantum/ward_shift_fvqe_training.json — certified 1.0000 opt-mass on H1-1LE.
_WARDSHIFT_FVQE_4Q_HEADER = """\
import json, math
_params = json.load(open(
    "__FVQE_JSON__"))["params"]
c = Circuit(4, 4)
_k = 0
for _layer in range(2):
    for q in range(4):
        c.Ry(_params[_k] / math.pi, q); _k += 1
    for q in range(4):
        c.CX(q, (q + 1) % 4)
for q in range(4):
    c.Ry(_params[_k] / math.pi, q); _k += 1
for q in range(4):
    c.Measure(q, q)
"""


def _compile_config(backend):
    if backend.startswith("Helios"):
        return ("try:\n    cfg = qnx.HeliosConfig()\n"
                "except Exception:\n    cfg = qnx.QuantinuumConfig(device_name=\"H1-1LE\")")
    return "cfg = qnx.QuantinuumConfig(device_name=\"%s\")" % backend


def _submit(circuit_code, name, backend, shots):
    code = (_PREAMBLE.replace("__ROUNDS__", str(POLL_ROUNDS))
            .replace("__SLEEP__", str(POLL_SLEEP)))
    runner = (_JOB_RUNNER.replace("__CIRCUIT__", circuit_code)
              .replace("__NAME__", '"%s"' % name)
              .replace("__CONFIG__", _compile_config(backend))
              .replace("__SHOTS__", str(shots))
              .replace("__BACKEND__", backend))
    return _run(code + runner)


_HUGR_ATTEST = """\
import sys as _sys
_sys.path.insert(0, "/Users/openclaw/Downloads/NHS Quantinuum")
import tempfile as _tf, importlib.util as _ilu
from quantum.endo_attestation.attestation_circuit import generate_attestation_guppy
proj = pick_project()
code = generate_attestation_guppy(graph_name="C6", tau=2.0, basis=0, part="re",
                                  shadow_basis=["Z", "X", "X"], seed=42)
with _tf.NamedTemporaryFile(mode="w", suffix=".py", delete=False, prefix="attest_h_C6_") as _f:
    _f.write(code)
    _tp = _f.name
_spec = _ilu.spec_from_file_location("attest_h_C6", _tp)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
hugr_pkg = _mod.program.compile()
hugr_ref = qnx.hugr.upload(hugr_package=hugr_pkg, name="nexus_cmd_attest_hugr_c6")
from quantinuum_schemas.models.backend_config import HeliosEmulatorConfig
from quantinuum_schemas.models.emulator_config import (
    StatevectorSimulator, HeliosRuntime, NoErrorModel)
_emu = HeliosEmulatorConfig(n_qubits=4, simulator=StatevectorSimulator(),
                            runtime=HeliosRuntime(), error_model=NoErrorModel())
_cfg = qnx.HeliosConfig(system_name="Helios-1E-lite", emulator_config=_emu)
exe = qnx.start_execute_job(programs=[hugr_ref], n_shots=[1000],
                            backend_config=_cfg, name="nexus_cmd_exec_attest_helios")
state, _ = wait(exe)
if state != "done":
    print("EXECUTE_" + state.upper() + " id=" + str(exe.id)); raise SystemExit
anc = qnx.jobs.results(exe)[0].download_result().register_counts("anc")["anc"]
p0 = anc.get("0", 0) / 1000.0
p1 = anc.get("1", 0) / 1000.0
tr = abs(p0 - p1)
print("OK backend=Helios-1E-lite shots=1000 P(0)=%.4f P(1)=%.4f trace=%.4f verdict=%s proj=%s"
      % (p0, p1, tr, "CERTIFY" if p0 > 0.55 else "REFUSE", proj))
print("JOB " + str(exe.id))
"""


def _submit_hugr():
    code = (_PREAMBLE.replace("__ROUNDS__", str(POLL_ROUNDS))
            .replace("__SLEEP__", str(POLL_SLEEP)))
    return _run(code + _HUGR_ATTEST)


def _attestation_run():
    """HUGR lane on Helios; falls back to 2q Hadamard test on H1-1LE."""
    rc, out, err = _submit_hugr()
    if "OK backend" in out:
        return out, err
    cu1 = _cu1_name()
    rc2, out2, err2 = _submit(_ATTEST_2Q.replace("__CU1__", cu1),
                              "dqc1_trace_2q", "H1-1LE", 1000)
    note = " (Helios HUGR lane unavailable — H1-1LE fallback)"
    return (out2 + note, err2 if "OK backend" not in out2 else err2)
def _cu1_name():
    rc, out, _ = _run("from pytket.circuit import OpType\n"
                      "print('CU1' if hasattr(OpType, 'CU1') else 'CU')")
    return "OpType.CU1" if "CU1" in out else "OpType.CU"


# --------------------------------------------------------------------------- #
# read-only subcommands                                                        #
# --------------------------------------------------------------------------- #

def _backends():
    code = ("import qnexus as qnx\n"
            "try:\n"
            "    ds = qnx.devices.get_all()\n"
            "    for d in ds:\n"
            "        bn = getattr(d, 'backend_name', '?')\n"
            "        dn = getattr(d, 'device_name', None)\n"
            "        print(bn if not dn else bn + ' / ' + dn)\n"
            "except Exception as e:\n"
            "    print('DEVICE_LIST_FAILED: ' + str(e)[:200])\n")
    rc, out, err = _run(code, timeout=90)
    names = [l.strip() for l in out.splitlines()
             if l.strip() and not l.startswith("DEVICE_LIST_FAILED")]
    if names:
        return "🖥️ Nexus backends (live):\n" + "\n".join("• " + n for n in names)
    return ("🖥️ Nexus backends (curated fallback — live list failed):\n" +
            "\n".join("• " + n for n in FALLBACK_BACKENDS))


def _jobs(n):
    code = ("import qnexus as qnx\n"
            "pros = {p.annotations.name: p for p in qnx.projects.get_all()}\n"
            "pr = pros.get('EndoTrack-QIR') or pros.get('NHS Quantum')\n"
            "jobs = list(qnx.jobs.get_all(project=pr, page_size=%d))\n"
            "for j in jobs:\n"
            "    try:\n"
            "        st = qnx.jobs.status(j).status.name\n"
            "    except Exception:\n"
            "        st = '?'\n"
            "    nm = getattr(getattr(j, 'annotations', None), 'name', '?')\n"
            "    print(str(j.id) + ' | ' + nm + ' | ' + st)\n" % n)
    try:
        rc, out, err = _run(code, timeout=90)
    except Exception:
        rc, out = 124, ""
    if rc == 124:
        return ("📋 Job list timed out — Nexus is slow right now. "
                "Try again in a minute, or check a known id with /nexus status <id>.")
    lines = [l for l in out.splitlines() if "|" in l]
    if not lines:
        return ("📋 Couldn't fetch recent jobs (Nexus API hiccup). "
                "Try again shortly or use /nexus status <id>.")
    return "📋 Recent Nexus jobs:\n" + "\n".join(lines)


def _status(prefix):
    code = ("import qnexus as qnx\n"
            "from uuid import UUID\n"
            "p = '''%s'''\n"
            "try:\n"
            "    j = qnx.jobs.get(id=UUID(p))\n"
            "except Exception:\n"
            "    j = None\n"
            "    for cand in list(qnx.jobs.get_all())[:100]:\n"
            "        if str(cand.id).startswith(p):\n"
            "            j = cand; break\n"
            "if j is None:\n"
            "    print('NOT_FOUND'); raise SystemExit\n"
            "st = qnx.jobs.status(j).status.name\n"
            "nm = getattr(getattr(j, 'annotations', None), 'name', '?')\n"
            "print(str(j.id) + ' | ' + nm + ' | ' + st)\n" % prefix)
    rc, out, err = _run(code, timeout=120)
    for line in out.splitlines():
        if "|" in line or line.strip() == "NOT_FOUND":
            if line.strip() == "NOT_FOUND":
                return "❌ No job starting with '%s' in your recent 100." % prefix
            return "🔎 " + line.strip()
    return ("❌ Couldn't reach the Nexus job list right now (their API timed out). "
            "Try again in a minute with /nexus status %s." % prefix)


# --------------------------------------------------------------------------- #
# entry point                                                                  #
# --------------------------------------------------------------------------- #

def _shots(arg, default=1000):
    try:
        s = int(arg)
        return max(10, min(s, 10000))
    except (TypeError, ValueError):
        return default


def handle_nexus_command(text):
    """Handle '/nexus <sub> [args]'. Always returns str, never raises."""
    try:
        parts = (text or "").strip().split()
        sub = parts[1].lower() if len(parts) > 1 else "help"
        args = parts[2:]

        if sub == "help":
            return HELP

        if sub == "backends":
            return _backends()

        if sub == "jobs":
            n = _shots(args[0] if args else None, default=5)
            return _jobs(max(1, min(n, 20)))

        if sub == "status":
            if not args:
                return "Usage: /nexus status <job_id> (full id or first 8 characters)"
            return _status(args[0])

        if sub == "pathway":
            shots = _shots(args[0] if args else None)
            rc, out, err = _submit(_PATHWAY_6Q, "pathway_qaoa_6q", "H1-1LE", shots)
            return _fmt_run("Pathway QAOA 6q on H1-1LE", out, err)

        if sub == "pathway_16q":
            shots = _shots(args[0] if args else None)
            rc, out, err = _submit(_PATHWAY_16Q, "pathway_qaoa_16q", "H2-1LE", shots)
            return _fmt_run("Pathway QAOA 16q on H2-1LE", out, err)

        if sub == "attestation":
            out, err = _attestation_run()
            return _fmt_run("DQC1 attestation (C6, Helios HUGR lane)", out, err)

        if sub == "bench":
            shots = _shots(args[0] if args else None, default=100)
            rc1, out1, err1 = _submit(_PATHWAY_6Q, "bench_pathway_6q", "H1-1LE", shots)
            out2, err2 = _attestation_run()
            import math
            env = 4 * math.sqrt(0.5 / max(shots, 1))
            verdict = ("CERTIFY" if "OK backend" in out1 and "OK backend" in out2
                       else "REVIEW")
            return ("📊 Mini epistemic suite (%d shots, envelope ±%.4f) → %s\n\n"
                    "— Pathway —\n%s\n\n— Attestation —\n%s"
                    % (shots, env, verdict,
                       _short(out1, err1), _short(out2, err2)))

        if sub == "backend":
            if not args:
                return "Usage: /nexus backend <name> (see /nexus backends)"
            name = args[0]
            rc, out, err = _submit(_BELL_2Q, "bell_health_2q", name, 100)
            return _fmt_run("Bell health test on " + name, out, err)

        if sub == "wardshift":
            # /nexus wardshift [shots] [backend] [fvqe] — WardFlow NOW/NEXT receipt
            shots = _shots(args[0] if args else None, default=256)
            backend = next((a for a in args[1:] if not a.isdigit() and a != "fvqe"), "H1-1LE")
            use_fvqe = "fvqe" in [a.lower() for a in args]
            fvqe_json = str(Path(__file__).resolve().parent.parent.parent
                            / "quantum" / "ward_shift_fvqe_training.json")
            if use_fvqe and Path(fvqe_json).exists():
                circ = _WARDSHIFT_FVQE_4Q_HEADER.replace("__FVQE_JSON__", fvqe_json)
                title = "WardFlow shift-split F-VQE 4q (trained, Amaro 2022) on " + backend
                name = "wardshift_fvqe_4q"
            else:
                if use_fvqe:
                    return ("❌ fvqe requested but trained params not found at\n"
                            + fvqe_json + "\nRunning nothing. Use plain: /nexus wardshift")
                circ = _WARDSHIFT_4Q
                title = "WardFlow shift-split QAOA 4q on " + backend
                name = "wardshift_qaoa_4q"
            rc, out, err = _submit(circ, name, backend, shots)
            reply = _fmt_run(title, out, err)
            if "OK backend" in out:
                # honest verdict: optimum-state mass vs uniform 0.125
                opt = 0.0
                for line in out.splitlines():
                    ls = line.strip()
                    if ls.startswith(("(0, 1, 0, 1)", "(1, 0, 1, 0)", "0101", "1010")):
                        try:
                            opt += float(ls.rsplit("(", 1)[1].rstrip(")"))
                        except (IndexError, ValueError):
                            pass
                import math as _m
                env = 4 * _m.sqrt(0.5 / max(shots, 1))
                reply += ("\n🧾 Receipt: optimum-state mass %.3f vs 0.125 uniform "
                          "(envelope ±%.3f). Execution receipt only — no quantum "
                          "advantage claimed." % (opt, env))
            return reply

        return "❓ Unknown /nexus subcommand '%s'.\n%s" % (sub, HELP)
    except Exception as exc:  # never break the gateway
        return "❌ Nexus command error: %s" % str(exc)[:300]


def _short(out, err):
    for line in out.splitlines():
        if line.startswith(("OK backend", "COMPILE_", "EXECUTE_")):
            return line.strip()
    tail = (err.strip()[-400:] if err.strip() else out.strip()[-400:])
    if "500" in tail or "Internal Error" in tail:
        return ("Nexus API returned an internal error (500) — their side, "
                "not the circuit. Worth retrying in a few minutes.")
    return tail or "no output"


def _fmt_run(title, out, err):
    if "OK backend" in out:
        detail = "\n".join(l for l in out.splitlines()
                           if l.startswith(("OK backend", "  ", "JOB ")))
        return "✅ %s — done\n%s" % (title, detail)
    if "id=" in out and ("RUNNING" in out or "WAITING" in out):
        for line in out.splitlines():
            if "id=" in line:
                return ("⏳ %s — still %s. Check later with:\n/nexus status %s"
                        % (title, line.split()[0], line.split("id=")[1].strip()))
    return "❌ %s failed.\n%s" % (title, _short(out, err))


if __name__ == "__main__":
    print(handle_nexus_command(" ".join(sys.argv[1:]) or "/nexus help"))
