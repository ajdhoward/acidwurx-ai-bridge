# acidwurx-ai-bridge (PUBLIC — ZERO SECRETS)

Single public URL that routes any AI chat into exactly one role of the
AcidWurx Autonomous Ecosystem. **No secrets, account IDs, tokens, credentials,
or private domains may ever be committed to this repository.**

## Map

| Path | Purpose |
|---|---|
| `llms.txt` | Role router — paste this repo URL into any AI chat and it routes itself |
| `routing/SKILL_MATRIX.json` | Platform -> role / strengths / limits mapping |
| `routing/ACCOUNT_POOL.json` | Multi-account failover state (availability only — never credentials) |
| `routing/LEDGER.md` | The ONLY file capped specialists (kimi / claude) may read |
| `protocols/RETURN_PROTOCOL.md` | Universal single-Bash-block response contract |
| `TASKS_DISPATCH.md` | Skill-tagged research queue (maintained by google-ai-search) |
| `proposals/` | AI deliverables land here as `proposals/<ai>-<task>.md` |

## Hard rules

1. Zero secrets, zero account identifiers, zero private domains — enforced by audit before every push.
2. AI outputs are always ONE copy-paste Bash block per `protocols/RETURN_PROTOCOL.md`.
3. No live infrastructure changes until the Stage 0 Verification Gate passes (see workspace-orchestrator MILESTONES.md).
