from __future__ import annotations

from src.workflow_engine import Stage, Workflow
from src.workflow_intelligence import (
    IntentInferenceEngine,
    NotionWorkflowIntelligence,
    UserContext,
    WorkflowCoordinator,
    WorkflowPlanner,
)


def sample_context() -> UserContext:
    return UserContext(
        recent_notes=[
            "Project A meeting notes",
            "Project B design notes",
            "Project A launch checklist",
        ],
        active_projects=["Project A", "Project B"],
        calendar_events=[{"project": "Project A", "time": "2026-08-20"}],
        previous_workflows=[],
        user_preferences={},
    )


def test_contextual_intent_is_deterministic_local_heuristic() -> None:
    engine = IntentInferenceEngine()
    first = engine.infer("Clean up my notes", sample_context())
    second = engine.infer("Clean up my notes", sample_context())

    assert first == second
    assert first.primary_action == "organize"
    assert first.organization_strategy == "project"
    assert first.priority_order[0] == "Project A"
    assert set(first.target_objects).issubset({"Project A", "Project B"})
    assert 0.0 <= first.confidence <= 0.95


def test_explicit_action_keyword_changes_bounded_plan() -> None:
    engine = IntentInferenceEngine()
    intent = engine.infer("Summarize Project B", sample_context())
    plan = WorkflowPlanner().plan(intent, sample_context())

    assert intent.primary_action == "summarize"
    assert intent.target_objects == ["Project B"]
    assert [step.action for step in plan.steps] == [
        "read",
        "analyze",
        "synthesize",
        "present",
    ]
    assert plan.steps[0].dependencies == []
    for previous, current in zip(plan.steps, plan.steps[1:]):
        assert current.dependencies == [previous.step_id]


def test_local_coordinator_completes_dependency_plan() -> None:
    context = sample_context()
    intent = IntentInferenceEngine().infer("Organize project notes", context)
    plan = WorkflowPlanner().plan(intent, context)
    coordinator = WorkflowCoordinator()

    results = coordinator.execute_workflow(plan)
    alignment = coordinator.check_alignment(plan, results)

    assert results["completed"] == results["total_steps"] == len(plan.steps)
    assert all(row["status"] == "completed" for row in results["execution_log"])
    assert alignment == {
        "alignment_score": 1.0,
        "steps_completed": len(plan.steps),
        "total_steps": len(plan.steps),
        "status": "ALIGNED",
    }


def test_guarded_stage_engine_blocks_without_skipping() -> None:
    workflow = Workflow(
        "release",
        [
            Stage("triage", lambda state: bool(state.get("ticket")), 4),
            Stage("review", lambda state: bool(state.get("reviewed")), 8),
        ],
        state={"ticket": True},
    )

    assert workflow.advance() == {"advanced_to": "triage", "done": False}
    assert workflow.advance() == {"blocked_at": "review", "done": False}
    assert workflow.history == ["triage"]
    workflow.state["reviewed"] = True
    assert workflow.advance() == {"advanced_to": "review", "done": True}


def test_full_facade_remains_local_and_observable() -> None:
    runtime = NotionWorkflowIntelligence()
    result = runtime.process_request("Clean up my project notes", sample_context())
    stats = runtime.get_stats()

    assert result["inferred_intent"]["action"] == "organize"
    assert result["results"]["completed"] == result["results"]["total_steps"]
    assert result["alignment"]["status"] == "ALIGNED"
    assert stats["total_workflows"] == 1
    assert stats["avg_alignment"] == 1.0
