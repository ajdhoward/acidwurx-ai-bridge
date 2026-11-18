# TASKS_DISPATCH — Skill-Tagged Research Queue

Maintained by GOOGLE AI SEARCH (Stage 0 Lead Architect).
Status values: QUEUED / DISPATCHED / RETURNED / ACCEPTED / REJECTED.
Free-limit bound: context budget the target AI must respect.
Generated from self-contained task cards in `tasks/` (directive §3.1 schema);
relay drops must satisfy `schema/relay.schema.json` (validated by
`.github/workflows/validate-relay.yml` — data only, never executed).

| Task ID | Skill Tag | Objective | Free-Limit Bound | Status | Returned Proposal |
|---|---|---|---|---|---|
| S0-T1 | [SKILL:google-ai-search] | Map all initial stages with strict Verification Gates | — | QUEUED | — |
| S0-T2 | [SKILL:google-ai-search] | Survey llms.txt generators (shortlist <=3) | — | QUEUED | — |
| S0-T3 | [SKILL:google-ai-search] | Survey multi-agent GitHub Action relays (shortlist <=3) | — | QUEUED | — |
| S0-T4 | [SKILL:google-ai-search] | Survey git subtree automation patterns | — | QUEUED | — |
| S0-T5 | [SKILL:google-ai-search] | Survey MCP registries + Generative UI chat frameworks (shortlist <=3 each) | — | QUEUED | — |
| S0-T6 | [SKILL:claude] | Architecture + security critique of bridge structure | <3,500 tokens | QUEUED | — |
| T-0001 | [SKILL:google-ai-search] | Map Stage 0 Verification Gates (canonical card for S0-T1) | 8k in / 6k out | QUEUED | — |
| T-0010 | [SKILL:qwen] | Audit All Existing GitHub Repos for Consolidation (needs REPO_INVENTORY.json) | 24k in / 8k out | QUEUED | — |
| T-0020 | [SKILL:meta-ai] | Write idempotent deploy_all.sh for gh CLI bootstrap | 12k in / 6k out | QUEUED | — |

## Directive 2026-11-18 — Optimization Track (M1-OPTIMIZATION)

Added by architect-agent (zai session web-fa988852) per owner directive.
Canonical execution state lives in workspace-orchestrator `TASK_QUEUE.json`
v2.0; board status below tracks relay lifecycle only (QUEUED → DISPATCHED →
RETURNED → ACCEPTED/REJECTED). Governance: STAGE_0 freeze applies — all rows
are audit/research/blueprint work. Dependency gate: PROJ-*/AUTO-001 unlock
after OPT-001 completes.

| Task ID | Skill Tag | Objective | Free-Limit Bound | Status | Returned Proposal |
|---|---|---|---|---|---|
| OPT-001 | [SKILL:opencode-local] | Audit + optimize OpenCode inference routing (audit now; applied change needs STAGE_1 unlock) | — | QUEUED | — |
| OPT-002 | [SKILL:google-ai-search] | Discover free MCP servers for code quality/testing/security + OpenCode integration instructions | — | QUEUED | — |
| OPT-003 | [SKILL:claude] | Analyze provider ToS for multi-account usage; design compliant routing strategy | <3,500 tokens | QUEUED | — |
| PROJ-001 | [SKILL:qwen] | Blueprint: workspace-orchestrator (blocked on OPT-001) | — | QUEUED | — |
| PROJ-002 | [SKILL:qwen] | Blueprint: opencode-vault (blocked on OPT-001) | — | QUEUED | — |
| PROJ-003 | [SKILL:qwen] | Blueprint: acidwurx-ai-bridge (blocked on OPT-001) | — | QUEUED | — |
| PROJ-004 | [SKILL:qwen] | Blueprint: cloudflare-dashboard (blocked on OPT-001) | — | QUEUED | — |
| PROJ-005 | [SKILL:qwen] | Blueprint: omniroute-cf (blocked on OPT-001) | — | QUEUED | — |
| PROJ-006 | [SKILL:qwen] | Blueprint: acidwurx-nexus-telemetry (blocked on OPT-001) | — | QUEUED | — |
| PROJ-007 | [SKILL:qwen] | Blueprint: agent-hpc-conduit (blocked on OPT-001) | — | QUEUED | — |
| PROJ-008 | [SKILL:qwen] | Blueprint: personal-os (blocked on OPT-001) | — | QUEUED | — |
| PROJ-009 | [SKILL:qwen] | Blueprint: uk-home-ops (blocked on OPT-001) | — | QUEUED | — |
| PROJ-010 | [SKILL:qwen] | Blueprint: trevorcare (blocked on OPT-001) | — | QUEUED | — |
| AUTO-001 | [SKILL:meta-ai] | GitHub Actions for code quality gates (blocked on OPT-001) | — | QUEUED | — |

## Claim rules (directive §Universal Entry Protocol)

1. Read `routing/SKILL_MATRIX.json`; claim ONE task matching your skill tag.
2. Check `routing/LEDGER.md` for your account's remaining capacity.
3. Execute within the card's declared token ceilings; chunk if capped-tier.
4. Return ONE copy-paste Bash block per `protocols/RETURN_PROTOCOL.md`.
5. Near your limit? Set `status: PARTIAL`, write the checkpoint, set
   `next_action: REASSIGN_NEXT_ACCOUNT`.

Live infrastructure remains FROZEN (STAGE_0_RESEARCH_READY) until all Stage 0 rows
are ACCEPTED and the Verification Gate sign-off is recorded in
workspace-orchestrator MILESTONES.md.
