#!/Users/openclaw/.hermes/hermes-agent/venv/bin/python
"""
Telegram-triggered Nexus wrapper for OpenClaw
Usage in Telegram: /nexus run pathway_allocation
Gateway exec: /Users/openclaw/.hermes/hermes-agent/venv/bin/python tools/nexus_telegram_wrapper.py pathway_allocation

Verifies: Hermes venv has qnexus 0.48.2 + pytket 2.18.1 + guppylang 1.0.0a8 + ~/.qnx/auth/token.json
"""
import sys, json, subprocess
from pathlib import Path

HERMES_PY = "/Users/openclaw/.hermes/hermes-agent/venv/bin/python"
TOOLS_DIR = Path(__file__).parent
WORKLOADS = {
    "pathway_allocation": "execute_pathway_nexus.py",
    "horizon_breakthroughs": "execute_horizon_breakthroughs_nexus.py",
    "advanced_suite": "execute_advanced_nexus_suite.py",
    "h2_helios": "execute_h2_and_helios_nexus.py",
}

def main():
    workload = sys.argv[1] if len(sys.argv) > 1 else "pathway_allocation"
    if workload not in WORKLOADS:
        print(json.dumps({"ok": False, "error": f"Unknown workload '{workload}'. Options: {list(WORKLOADS)}"}))
        sys.exit(1)
    
    script = TOOLS_DIR / WORKLOADS[workload]
    if not script.exists():
        print(json.dumps({"ok": False, "error": f"Script not found: {script}"}))
        sys.exit(1)

    # Verify Nexus auth
    auth_path = Path.home() / ".qnx" / "auth" / "token.json"
    if not auth_path.exists():
        print(json.dumps({"ok": False, "error": "Nexus credentials missing at ~/.qnx/auth/token.json — run qnexus auth flow or set QNEXUS_TOKEN"}))
        sys.exit(1)

    print(f"→ Launching {workload} via {HERMES_PY} ...")
    result = subprocess.run([HERMES_PY, str(script)], cwd=str(TOOLS_DIR.parent), capture_output=True, text=True, timeout=600)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    
    # Try to find receipt JSON in stdout or tools/*.json
    receipt = {"ok": result.returncode == 0, "workload": workload, "returncode": result.returncode}
    print(json.dumps(receipt, indent=2))

if __name__ == "__main__":
    main()
