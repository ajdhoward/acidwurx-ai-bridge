# SAFETY_AND_TOS.md — Provider Terms Compliance Statement

Status: BINDING for every participant (human or AI) in the AcidWurx ecosystem.
Last reviewed: 2026-11-16

## 1. Zero secrets, always

- `acidwurx-ai-bridge` is public. No tokens, account IDs, private domains,
  internal hostnames, or credentials of any kind may be committed here.
- Every relay passing through `validate-relay.yml` is scanned for secret
  patterns before acceptance. Violations reject the relay; nothing executes.

## 2. Account pooling policy

- Pooling covers only accounts the owner legitimately owns and is permitted
  to operate. Where a provider forbids multiple accounts, `pool_size_allowed`
  is 1 and additional slots in `routing/ACCOUNT_POOL.json` stay `enabled: false`.
- No automated sign-up. No credential sharing. No proxy rotation. No
  circumvention of technical limits, rate caps, or free-tier boundaries.
- Quota rotation is a manual pacing aid for the owner, never an evasion
  mechanism. `cooldown_hours` and `reset_convention` reflect provider-published
  reset windows.

## 3. Relay content contract

- Every AI response returns as a single copy-paste Bash block per
  `protocols/RETURN_PROTOCOL.md` — a heredoc writing ONE markdown file.
- Relay bodies are **data only**: findings, code snippets, schemas, proposals.
- Validators reject executable payloads (curl/wget/eval/sudo/rm/chmod/ssh/nc)
  and never run, eval, or pipe relay content.

## 4. Attribution and licensing

- Third-party repositories referenced in proposals keep their licenses;
  adoption proposals must state the license and compatibility.
- Generated artifacts record the producing provider and task ID in front
  matter for auditability.

## 5. Circuit breaker

- Repeated validation failures from one provider move that account to
  `EXHAUSTED_COOLDOWN` in `routing/LEDGER.md` and set
  `next_action: REASSIGN_NEXT_ACCOUNT` on affected tasks.
- Anything the owner flags in `OVERRIDE.md` (workspace-orchestrator) pauses
  dispatch immediately; OVERRIDE outranks every queue in this repo.
