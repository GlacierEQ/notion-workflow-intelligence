#!/usr/bin/env python3
"""Fail-closed public truth checks for the workflow-intelligence surface."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PUBLIC_TRUTH_FAIL: {message}")


def main() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    caps = json.loads((ROOT / "machine/capabilities.json").read_text(encoding="utf-8"))
    state = json.loads((ROOT / "machine/excellence-state.json").read_text(encoding="utf-8"))

    for marker in ("<<<<<<<", "=======", ">>>>>>>"):
        require(marker not in readme, f"README contains merge-conflict marker {marker}")

    forbidden = (
        "MCP Tool",
        "Connected to APEX Highway mesh",
        "mcp_client.call_tool",
        "API integration with Notion",
        "LLM-powered task decomposition",
    )
    for phrase in forbidden:
        require(phrase not in readme, f"README contains unsupported claim: {phrase}")

    require("No live Notion" in readme, "live Notion API nonclaim missing")
    require("No live MCP, APEX, Mastermind" in readme, "live mesh nonclaim missing")
    require("rule-derived score" in readme, "heuristic score boundary missing")

    allowed = {
        "deterministic-contextual-intent-heuristics",
        "dependency-aware-workflow-plan-construction",
        "local-workflow-step-coordination-simulation",
        "guarded-stage-transition-engine",
        "rule-derived-alignment-and-workflow-statistics",
    }
    require(set(caps.get("capabilities", [])) == allowed, "capability allowlist drift")
    require(caps.get("operational_authority") is False, "operational authority must be false")
    require(caps.get("live_notion_api_integration") is False, "live Notion claim must be false")
    require(
        caps.get("live_mcp_apex_mastermind_integration") is False,
        "live mesh claim must be false",
    )
    require(caps.get("llm_or_model_inference") is False, "model inference claim must be false")
    require(caps.get("persistent_learning") is False, "persistent-learning claim must be false")
    require(caps.get("external_agent_execution") is False, "external-agent claim must be false")

    require(state.get("principal_state") == "FUNCTIONAL_CANDIDATE", "stale promotion restored")
    require(state.get("operational_authority") is False, "state grants operational authority")
    proof_gate = state.get("gates", {}).get("DETERMINISTIC_PROOF_GREEN", {})
    require(proof_gate.get("status") == "PENDING_CANONICAL_CI", "fresh proof gate missing")

    print("PUBLIC_TRUTH_PASS")


if __name__ == "__main__":
    main()
