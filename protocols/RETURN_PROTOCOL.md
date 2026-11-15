# RETURN_PROTOCOL.md — Universal Web-AI Response Contract (v2: 4 Relay Types)

> Every web-AI chat MUST return progress as a **single copy-and-paste Bash
> block** using single-quoted `'AI_RELAY_EOF'` heredocs, so the operator (or
> OpenCode) can paste it straight into a terminal for immediate ingestion.
>
> v2 adds FOUR relay types that nodes publish at different stages, so progress
> becomes visible to all other AIs the moment it exists (no coordination lag).
> Relay payloads must satisfy `schema/relay.schema.json` (validated data-only
> by `.github/workflows/validate-relay.yml`).

---

## RELAY TYPE 1 — TASK CLAIM (before starting any work)

Prevents duplicate work. **First push wins** — claims are atomic.

```bash
cd "${BRIDGE_DIR:-$HOME/acidwurx-ai-bridge}" && git pull --rebase --autostash && mkdir -p claims && cat << 'AI_RELAY_EOF' > claims/TASKID-ACCOUNT.json
{
  "task_id": "T-0000",
  "account": "<account-id>",
  "provider": "<provider>",
  "claimed_utc": "<ISO8601>",
  "lease_ttl_h": 6,
  "idempotency_key": "TASKID-ACCOUNT-ATTEMPT"
}
AI_RELAY_EOF
git add claims && git commit -m "claim(TASKID): ACCOUNT" && git push
```

If `git push` FAILS with a conflict: someone else claimed the task. Read
`claims/`, pick a DIFFERENT task, do not retry the same claim.

---

## RELAY TYPE 2 — CHECKPOINT (partial progress / quota failover)

Append-only. Timestamped filename. Publish when you finish a sub-step OR when
you hit quota limits.

```bash
cd "${BRIDGE_DIR:-$HOME/acidwurx-ai-bridge}" && git pull --rebase --autostash && mkdir -p checkpoints && cat << 'AI_RELAY_EOF' > checkpoints/TASKID-ACCOUNT-$(date -u +%Y%m%dT%H%M%SZ).md
---
task_id: T-0000
provider: <provider>
account_slot: <account-id>
status: PARTIAL
tokens_in_est: 0
tokens_out_est: 0
quota_state: NEAR_LIMIT
reset_hint_utc: <ISO8601 or unknown>
next_action: REASSIGN_NEXT_ACCOUNT
completed_units: ["unit1", "unit2"]
remaining_units: ["unit3", "unit4"]
findings_so_far: |
  <concise findings, <=800 tokens>
exact_next_instruction: "Continue with unit3; apply same analysis pattern"
---
AI_RELAY_EOF
git add checkpoints && git commit -m "checkpoint(TASKID): ACCOUNT partial" && git push
```

---

## RELAY TYPE 3 — COMPLETE (final deliverable)

Exclusive namespace: `proposals/<provider>-<task-id>.md`. On success, release
your claim file. (v1 contract — `proposals/<ai>-<task>.md` with one block per
response — remains valid and is now RELAY TYPE 3.)

```bash
cd "${BRIDGE_DIR:-$HOME/acidwurx-ai-bridge}" && git pull --rebase --autostash && mkdir -p proposals && cat << 'AI_RELAY_EOF' > proposals/PROVIDER-TASKID.md
---
task_id: T-0000
provider: <provider>
account_slot: <account-id>
status: COMPLETE
tokens_in_est: 0
tokens_out_est: 0
quota_state: AVAILABLE
reset_hint_utc: <ISO8601 or unknown>
next_action: CONTINUE
confidence: 7
---
<findings, code, schemas, proposals — Markdown data only>
AI_RELAY_EOF
git add proposals && rm -f claims/TASKID-ACCOUNT.json && git commit -m "relay(PROVIDER): TASKID complete" && git push
```

---

## RELAY TYPE 4 — LEDGER UPDATE (after EVERY relay event)

Append-only quota tracking. One row per relay event (claim / checkpoint /
complete / failover).

```bash
cd "${BRIDGE_DIR:-$HOME/acidwurx-ai-bridge}" && git pull --rebase --autostash && mkdir -p routing/ledger/ACCOUNT && cat << 'AI_RELAY_EOF' >> routing/ledger/ACCOUNT/$(date -u +%Y-%m-%d).jsonl
{"ts_utc":"<ISO8601>","account_id":"<account-id>","task_id":"T-0000","turns_used_est":1,"tokens_in_est":0,"tokens_out_est":0,"state":"AVAILABLE","reset_hint_utc":"<ISO8601 or unknown>","checkpoint_path":"checkpoints/TASKID-ACCOUNT-TIMESTAMP.md","next_action":"CONTINUE"}
AI_RELAY_EOF
git add routing/ledger && git commit -m "ledger(ACCOUNT): update quota" && git push
```

---

## Rules (carried from v1, binding)

1. Use the single-quoted heredoc delimiter `'AI_RELAY_EOF'` so content is never
   interpolated or executed.
2. Complete deliverables target `proposals/<provider>-<task-id>.md`
   (e.g. `proposals/kimi-S0-T6.md`).
3. The block is idempotent-safe: `git pull --rebase --autostash` first, then
   commit + push.
4. Never include secrets, account IDs, tokens, or private domains in the output.
5. If `git push` fails: STOP — do not force-push. Emit the failure directive below.
6. Replace all placeholders: `T-0000`, `<account-id>` (e.g. `kimi-acct-1`),
   `<provider>`, `<ISO8601>`, PROVIDER, TASKID, ACCOUNT.
7. Multiple relays in one response: stack labelled Bash blocks, one per type.

## Failure-mode directives (emit INSTEAD of a relay when blocked)

- `REASSIGN_NEXT_ACCOUNT <provider> <task-id>` — free-limit hit; switch account
  (pair with RELAY TYPE 2 + 4).
- `PULL_CONFLICT <file>` — rebase failed; owner resolves manually.
- `NEED_CONTEXT <what>` — required file/content was out of your reading scope.

## Failover flow (single account hits free limit)

1. RELAY TYPE 2 — checkpoint with `next_action: REASSIGN_NEXT_ACCOUNT`,
   `quota_state: NEAR_LIMIT`, `reset_hint_utc`, exact resume instruction.
2. RELAY TYPE 4 — ledger row with `state: NEAR_LIMIT`.
3. Next AI reading the ledger picks the first AVAILABLE same-provider account
   from `routing/ACCOUNT_POOL.json`, re-claims (TYPE 1, new idempotency_key),
   and resumes from the latest checkpoint.
