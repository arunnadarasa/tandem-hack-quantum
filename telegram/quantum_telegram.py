#!/Users/openclaw/.hermes/hermes-agent/venv/bin/python
"""Unified Telegram quantum runner: Nexus + Aqora + Marimo (v2).
Telegram usage (Hermes or KrumpKlaw gateway, both have full tool access):
  quantum_telegram.py status                          # zero-cost health check
  quantum_telegram.py selene_smoke                    # local Selene Bell 64 shots, no HQCs
  quantum_telegram.py nexus_status                    # list Nexus projects (no job spend)
  quantum_telegram.py nexus_run pathway_allocation    # LIVE Nexus job (spends emulator time)
  quantum_telegram.py aqora_list                      # list Aqora workspaces (cold/warm)
  quantum_telegram.py aqora_run <ws_id> "print(1+1)"  # needs live runner (editor_url non-null)
  quantum_telegram.py marimo_check                    # local marimo version + PEP723 check

Rules: Hermes venv ONLY (/Users/openclaw/.hermes/hermes-agent/venv/bin/python).
Nexus auth: ~/.qnx/auth/token.json. Aqora: `aqora auth token` / AQORA_TOKEN.
Never run nexus_run without explicit user confirm (costs emulator quota).
"""
import sys, json, subprocess, os
from pathlib import Path

HERMES_PY = "/Users/openclaw/.hermes/hermes-agent/venv/bin/python"
TOOLS_DIR = Path(__file__).parent
SKILL_SCRIPTS = Path.home() / ".agents" / "skills" / "aqora-workspace" / "scripts"
WORKLOADS = {
    "pathway_allocation": "execute_pathway_nexus.py",
    "horizon_breakthroughs": "execute_horizon_breakthroughs_nexus.py",
    "advanced_suite": "execute_advanced_nexus_suite.py",
    "h2_helios": "execute_h2_and_helios_nexus.py",
}

def sh(cmd, timeout=60):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "")[:3000], (r.stderr or "")[:1000]

def cmd_status():
    out = {}
    rc, o, _ = sh([HERMES_PY, "-V"])
    out["hermes_python"] = o.strip()
    rc, o, _ = sh([HERMES_PY, "-c", "import qnexus,guppylang,pytket,marimo;print('lanes OK')"])
    out["lanes"] = o.strip() or "IMPORT FAIL"
    out["qnx_auth"] = (Path.home()/".qnx"/"auth"/"token.json").exists()
    rc, o, _ = sh([HERMES_PY.replace("/python","/aqora"), "auth", "token"])
    out["aqora_token"] = bool(o.strip().startswith("oauth2"))
    rc, o, _ = sh([HERMES_PY.replace("/python","/marimo"), "--version"])
    out["marimo"] = o.strip()
    out["wrapper_v2"] = True
    print(json.dumps(out, indent=2))

def cmd_selene_smoke():
    code = (
        "from guppylang import guppy\n"
        "from guppylang.std.builtins import output\n"
        "from guppylang.std.quantum import qubit, h, measure\n"
        "from selene_sim import Quest\n"
        "@guppy\ndef program() -> None:\n"
        "    q = qubit()\n    h(q)\n"
        "    output('result', measure(q).read())\n"
        "res = program.emulator(n_qubits=1).with_shots(64).with_simulator(Quest()).run()\n"
        "tot = sum(1 for s in res for _ in s.entries)\n"
        "z = sum(1 for s in res for _,v in s.entries if int(v)==0)\n"
        "print(f'SELENE_SMOKE shots={tot} P(0)={z/max(tot,1):.3f} (expect ~0.5)')\n"
    )
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code); p = f.name
    rc, o, e = sh([HERMES_PY, p], timeout=120)
    print(o or e)

def cmd_nexus_status():
    code = (
        "import qnexus as qnx\n"
        "pros=[p.annotations.name for p in qnx.projects.get_all()]\n"
        "print('PROJECTS:', pros)\n"
    )
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code); p = f.name
    rc, o, e = sh([HERMES_PY, p], timeout=90)
    print(o or e)

def cmd_nexus_run(workload):
    if workload not in WORKLOADS:
        print(json.dumps({"ok": False, "options": list(WORKLOADS)})); sys.exit(1)
    script = TOOLS_DIR / WORKLOADS[workload]
    if not script.exists():
        print(json.dumps({"ok": False, "error": f"missing {script}"})); sys.exit(1)
    print(f"-> LIVE Nexus job: {workload} (600s cap) ...")
    r = subprocess.run([HERMES_PY, str(script)], cwd=str(TOOLS_DIR.parent),
                       capture_output=True, text=True, timeout=600)
    print(r.stdout[-3000:])
    if r.stderr: print("STDERR:", r.stderr[-1000:])
    print(json.dumps({"ok": r.returncode==0, "workload": workload, "rc": r.returncode}))

def cmd_aqora_list():
    s = SKILL_SCRIPTS / "list-workspaces.sh"
    if not s.exists():
        print(json.dumps({"ok": False, "error": f"missing {s} — run: npx skills add aqora-io/skills --skill aqora-workspace"})); return
    env = dict(os.environ)
    if "AQORA_TOKEN" not in env:
        rc, o, _ = sh([HERMES_PY.replace("/python","/aqora"), "auth", "token"])
        if o.strip().startswith("oauth2"): env["AQORA_TOKEN"] = o.strip()
    r = subprocess.run(["bash", str(s)], capture_output=True, text=True, timeout=60, env=env)
    print((r.stdout or r.stderr)[:3000])

def cmd_aqora_run(ws, code):
    s = SKILL_SCRIPTS / "execute-code.py"
    env = dict(os.environ)
    if "AQORA_TOKEN" not in env:
        rc, o, _ = sh([HERMES_PY.replace("/python","/aqora"), "auth", "token"])
        if o.strip().startswith("oauth2"): env["AQORA_TOKEN"] = o.strip()
    r = subprocess.run([HERMES_PY, str(s), "--workspace", ws, "-c", code],
                       capture_output=True, text=True, timeout=300, env=env)
    print(((r.stdout or "") + (r.stderr or ""))[:3000])

def cmd_marimo_check():
    rc, o, _ = sh([HERMES_PY.replace("/python","/marimo"), "--version"])
    print("marimo", o.strip())
    print("workspace marimo 0.23.15 vs local 0.24.0 — use PEP723 app=marimo.App(width='full')")

CMDS = {"status": cmd_status, "selene_smoke": cmd_selene_smoke,
        "nexus_status": cmd_nexus_status, "aqora_list": cmd_aqora_list,
        "marimo_check": cmd_marimo_check}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h","--help","help"):
        print(__doc__); return
    c = sys.argv[1]
    if c == "nexus_run": cmd_nexus_run(sys.argv[2] if len(sys.argv)>2 else "pathway_allocation")
    elif c == "aqora_run":
        if len(sys.argv) < 4: print("usage: aqora_run <ws_id> \"code\""); sys.exit(1)
        cmd_aqora_run(sys.argv[2], sys.argv[3])
    elif c in CMDS: CMDS[c]()
    else: print(json.dumps({"ok": False, "unknown": c, "options": list(CMDS)+["nexus_run","aqora_run"]})); sys.exit(1)

if __name__ == "__main__":
    main()
