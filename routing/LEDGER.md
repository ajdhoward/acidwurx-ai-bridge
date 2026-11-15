# Routing Ledger — Capped Specialists Start Here

You (kimi / claude / any capped web AI) must read ONLY this file plus your single
assigned micro-task. Do not explore other files. Total context budget: <3,500 tokens.

## How to work

1. Read your task row below (or the one referenced in your dispatch).
2. Produce your deliverable exactly per `protocols/RETURN_PROTOCOL.md` — ONE Bash block.
3. If you are near your daily free-chat limit, emit the checkpoint
   `REASSIGN_NEXT_ACCOUNT <provider> <task-id>` instead of degrading quality.

## Task rows

| Task ID | Skill Tag | Deliverable | Status | Returned Proposal |
|---|---|---|---|---|
| (none assigned yet — see TASKS_DISPATCH.md) | — | — | — | — |

## Account state snapshot (mirror of ACCOUNT_POOL.json at last sync)

| Provider | Active | Reserve | Notes |
|---|---|---|---|
| google-ai-search | google-acct-1 | — | OK |
| qwen | qwen-acct-1 | qwen-acct-2 | OK |
| meta-ai | meta-ai-acct-1 | — | OK |
| kimi | kimi-acct-1 | kimi-acct-2 | OK |
| claude | claude-acct-1 | claude-acct-2 | OK |

## Checkpoint directives

- `REASSIGN_NEXT_ACCOUNT <provider> <task-id>` — free-limit hit; owner switches to
  the next account in the pool and updates the snapshot table above.
- `PULL_CONFLICT <file>` — rebase failed; owner resolves manually.
- `NEED_CONTEXT <what>` — required content was outside this ledger's scope.

Ledger rows are updated by the owner (or sync automation), never by web AIs.
