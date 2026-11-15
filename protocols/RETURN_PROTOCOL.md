# Return Protocol — Universal Web-AI Response Contract

Every web AI working on this repo MUST respond with a SINGLE copy-and-paste Bash
block that the owner pastes directly into the terminal. No prose beyond a one-line
summary above the block. Exact block shape:

```bash
cat << 'AI_RELAY_EOF' > proposals/<ai>-<task>.md
<deliverable content — markdown>
AI_RELAY_EOF
git pull --rebase
git add .
git commit -m "feat(relay): <summary> (<ai>-<task>)"
git push
```

## Rules

1. Use the single-quoted heredoc delimiter `'AI_RELAY_EOF'` so content is never
   interpolated or executed.
2. Target file path MUST be `proposals/<ai>-<task>.md` (e.g. `proposals/kimi-S0-T6.md`).
3. The block is idempotent-safe: `git pull --rebase` first, then commit + push.
4. Never include secrets, account IDs, tokens, or private domains in the deliverable.
5. If `git push` fails, STOP and emit a checkpoint directive instead of force-pushing.
6. ONE block per response. No extra commands outside the block.

## Checkpoint directives (emit INSTEAD of the block when blocked)

- `REASSIGN_NEXT_ACCOUNT <provider> <task-id>` — free-limit hit; switch account.
- `PULL_CONFLICT <file>` — rebase failed; owner resolves manually.
- `NEED_CONTEXT <what>` — required file/content was out of your allowed reading scope.
