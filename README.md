# Notion Workflow Intelligence

Notion Workflow Intelligence is the Notion control-plane node for GlacierEQ workflow orchestration.

It exists to make work visible, queueable, reviewable, and connected across GitHub, memory, document systems, and worker swarms.

## System Role

This repository belongs to the workflow-intelligence layer.

Its role is to define and document how Notion should operate as:

- queue surface
- mission dashboard
- repository status board
- review and approval layer
- worker status ledger
- integration map
- human-readable control plane

## README Swarm Role

For library-wide README maintenance, Notion should hold the queue and state model.

```text
Repo inventory
        │
        ▼
Notion README queue
        │
        ├── repo
        ├── category
        ├── current score
        ├── target score
        ├── assigned worker batch
        ├── branch
        ├── PR
        ├── status
        └── audit receipt
        │
        ▼
Worker swarm
        │
        ├── Make-It-Heavy drafts the README star map
        ├── APEX GitHub Worker commits and opens PRs
        ├── Memory captures repo role and integration map
        └── Notion receives status and receipt updates
```

## Status

**ACTIVE / CONTROL-PLANE CANDIDATE**

The existing repository is currently skeletal. It needs schemas, examples, queue templates, and worker status contracts to become fully operational.

## Suggested Notion Databases

```text
Repository Catalog
README Audit Queue
Worker Runs
Patch Receipts
Integration Registry
Category Index
Review Decisions
```

## Required Queue Fields

```yaml
repo: GlacierEQ/example-repo
category: document-automation
priority: high
status: queued
readme_score_before: 42
readme_score_after: null
worker_batch: readme-swarm-001
branch: docs/readme-star-map
pr_url: null
receipt_sha256: null
review_owner: Casey
last_updated_hst: null
```

## Fleet Ops

This repo may include `.integrity/` SHA-256 baselines, watchdog metadata, and health sidecars.

These are documented multi-repo fleet operations, not covert implants.

See `SECURITY_AND_FLEET_OPS.md` and `~/GlacierEQ_Swarm/state/PORTFOLIO_SHADOW_AND_GAUNTLET.md` when available.

## Helix Strand

See `HELIX_STRAND.md` when present for the portfolio double-helix role.

## Truth & Maintenance Notes

This README describes the intended control-plane role. Implementation details should be expanded as queue schemas, worker contracts, and deployment receipts are added.
