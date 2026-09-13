"""Deterministic local simulation for a meeting-to-action workflow.

This is a simulation only. It does not call Alexa+, external APIs, or user accounts.
"""

from __future__ import annotations

import re

_ACTION = re.compile(
    r"^\s*action:\s*(?P<owner>[^\s:]+)\s+to\s+(?P<task>.+?)(?:\s+by\s+(?P<due>[^.]+))?\.?\s*$",
    re.IGNORECASE,
)
_DECISION = re.compile(r"^\s*decision:\s*(?P<decision>.+?)\s*$", re.IGNORECASE)


def transform_note(note: str) -> dict[str, list[object]]:
    """Extract de-duplicated decisions and confirmation-gated actions from a note."""
    if not note or not note.strip():
        raise ValueError("note must contain text")

    decisions: list[str] = []
    actions: list[dict[str, str | None]] = []
    seen: set[tuple[str, str, str | None]] = set()

    for line in note.splitlines():
        decision_match = _DECISION.match(line)
        if decision_match:
            decision = decision_match.group("decision").strip()
            if decision and decision not in decisions:
                decisions.append(decision)
            continue

        action_match = _ACTION.match(line)
        if not action_match:
            continue
        owner = action_match.group("owner").strip()
        task = action_match.group("task").strip().rstrip(".")
        due = action_match.group("due")
        due = due.strip().rstrip(".") if due else None
        identity = (owner.casefold(), task.casefold(), due.casefold() if due else None)
        if identity in seen:
            continue
        seen.add(identity)
        actions.append(
            {"owner": owner, "task": task, "due": due, "status": "needs_confirmation"}
        )

    return {"decisions": decisions, "actions": actions}
