# routing/ledger/ — Append-Only Quota Store

Directory layout:
```
routing/ledger/<account-id>/<YYYY-MM-DD>.jsonl
```

Rules:
- APPEND-ONLY. Never edit or delete existing `.jsonl` lines.
- One JSON object per line, schema per `../LEDGER.md`.
- Logical account IDs only. Zero real credentials, ever.
- Source of truth for account state in `routing/ACCOUNT_POOL.json` — never edit
  account state inline in the pool; append a ledger row instead.

Full explanation for capped AIs: see `../LEDGER.md`.
