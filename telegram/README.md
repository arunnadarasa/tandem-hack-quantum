# Telegram lane — run Nexus quantum receipts from your phone

Team members don't need a laptop, qnexus, or Python knowledge to fire a WardFlow quantum
receipt: the **`/nexus` slash command in Telegram** (via a Hermes gateway) submits jobs to
Quantinuum Nexus and returns plain-text receipts.

Source skill: [`arunnadarasa/telegram-quantum-hermes`](https://github.com/arunnadarasa/telegram-quantum-hermes)
(vendored here: `telegram/` + `skills/telegram-quantum-hermes/SKILL.md`).

## Commands (in the Telegram chat with the Hermes bot)

| Command | What it runs |
|---|---|
| `/nexus help` | command list |
| `/nexus backends` | live list of the 12 Nexus devices |
| `/nexus backend H1-1LE` | 2q Bell health test on a named backend |
| `/nexus pathway [shots]` | 6q QAOA allocation on H1-1LE (default 1000) |
| `/nexus pathway_16q [shots]` | 16q QAOA on H2-1LE |
| `/nexus attestation` | 2q Hadamard-test trace (Helios → H1-1LE fallback) |
| `/nexus bench [shots]` | pathway + attestation with ±4√(0.5/shots) verdict |
| `/nexus status <job_id>` | check any job (8-char prefix works) — e.g. the IDs in this repo's receipts |
| `/nexus jobs [n]` | your recent jobs |
| **`/nexus wardshift [shots] [backend] [fvqe]`** | **WardFlow NOW/NEXT shift-split receipt** — this repo's own circuit; add `fvqe` for the trained 100%-optimum version. Live-tested: job `4d072831`, 100/100 shots optimal |

## Plain-English mode (clinicians welcome)

No jargon needed. Say *"check the quantum computer works"* and the bot replies with one
suggestion — "Bell test, 2 qubits, 100 shots on H1-1LE (free test machine). Reply 'yes'
and I'll run it" — and **submits nothing without an explicit yes**. That confirmation gate
is CQM discipline: cost-aware, consent-first.

## WardFlow tie-in

- `/nexus status 7f8ad56f` → live-checks this repo's 4q receipt from a phone mid-demo.
- The dispatcher (`telegram/dispatcher/nexus_cmd.py`) is stdlib-only; all qnexus work runs
  in a Hermes-venv subprocess.
- **`/nexus wardshift` is wired and live-tested**: submits this repo's 4q shift-split
  (QAOA, or the F-VQE-trained circuit with `fvqe`), waits, and replies with counts plus an
  honest receipt line (optimum-mass vs uniform, envelope, no-advantage disclaimer).
  Verified: `/nexus wardshift 100 fvqe` → job `4d072831`, 100/100 shots on `1010`/`0101`.

## Setup (one person on the team)

1. Run a Hermes gateway with a Telegram bot token (`TELEGRAM_BOT_TOKEN` in `~/.hermes/.env` — never committed).
2. Ensure the Hermes venv has `qnexus` and `~/.qnx/auth` is logged in.
3. Drop `telegram/dispatcher/nexus_cmd.py` at `<hermes-agent>/quantum/nexus_cmd.py`.
4. Team members message the bot. Done — receipts by phone.

**Stale-gateway trap** (from the skill): if Telegram says `Unknown command /nexus`, the
gateway process predates the command — send `/restart`, wait ~30 s, retry.
