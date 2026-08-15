# Notion Workflow Intelligence

**Deterministic local intent heuristics, workflow planning, and guarded workflow execution.**

This repository is an independent portfolio project. It is not affiliated with Notion and it does not establish access to Notion APIs, workspaces, user data, or production automation authority.

## Implemented mechanisms

### Contextual intent heuristic

`src/workflow_intelligence.py` contains `IntentInferenceEngine`, which derives a local workflow intent from a caller-supplied request and `UserContext`.

The mechanism is deterministic rule logic:

- request keywords select an action and, when present, an organization strategy;
- caller-supplied active projects, recent-note text, and calendar records influence fallback strategy, targets, and priority ordering;
- the returned `confidence` value is a rule-derived score, not a calibrated probability or model confidence.

No language model, embedding model, Notion API, calendar API, or background learner is invoked by this mechanism.

### Dependency-aware workflow planning

`WorkflowPlanner` maps the inferred action to an ordered local step plan. Each generated step carries:

- an action;
- a target;
- a dependency on the preceding step when applicable;
- a local agent-role label; and
- a modeled duration value.

The agent labels are planning metadata. They do not prove that external autonomous agents were launched.

### Local workflow coordination simulation

`WorkflowCoordinator` executes the in-memory dependency plan, records completed steps, and derives a simple completion-based alignment score. The score is deterministic bookkeeping over local completion state, not a semantic evaluation of human intent.

### Guarded stage engine

`src/workflow_engine.py` provides a smaller `Workflow`/`Stage` mechanism. A workflow advances only when the next stage guard accepts current local state; otherwise it returns the blocking stage without skipping ahead.

## What this repository does not establish

- No live Notion database, page, block, user, or workspace integration.
- No Notion affiliation, endorsement, employment, or proprietary access.
- No live MCP, APEX, Mastermind, or provider-mesh integration.
- No LLM-powered content generation or semantic intent understanding.
- No persistent learning from prior workflows; in-memory logs are not a trained learner.
- No real multi-agent concurrency, external job execution, or autonomous side effects.
- No calibrated probability, production reliability, latency, throughput, or security guarantee.

## Verification

Repository CI is bound to the canonical `master` branch and verifies the bounded Python surfaces on Python 3.11, 3.12, and 3.13:

```bash
python -m compileall -q src tests scripts
python -m pytest -q
python scripts/verify_public_truth.py
```

The public-truth check fails closed if unresolved merge-conflict markers, live-provider claims, stale hyper-scaling capability metadata, or stale promoted authority reappear.

## Example

```python
from src.workflow_intelligence import NotionWorkflowIntelligence, UserContext

context = UserContext(
    recent_notes=["Project A notes", "Project B notes"],
    active_projects=["Project A", "Project B"],
    calendar_events=[{"project": "Project A", "time": "2026-08-20"}],
    previous_workflows=[],
    user_preferences={},
)

result = NotionWorkflowIntelligence().process_request(
    "Clean up my project notes",
    context,
)
print(result["inferred_intent"])
```

Everything in that example is local caller-supplied data and deterministic repository code.
