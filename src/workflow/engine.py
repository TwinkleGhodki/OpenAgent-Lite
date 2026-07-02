from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from dispatcher.dispatcher import Dispatcher


@dataclass
class WorkflowStep:
    """A single executable workflow step bound to an action name."""

    action_name: str
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)


class Workflow:
    """An ordered collection of workflow steps."""

    def __init__(self, steps: Optional[Sequence[WorkflowStep]] = None) -> None:
        self.steps: List[WorkflowStep] = list(steps or [])

    def add_step(self, step: WorkflowStep) -> None:
        """Append a step to the workflow."""
        self.steps.append(step)


class WorkflowExecutor:
    """Execute a workflow by dispatching each step through a dispatcher."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher

    def execute(self, workflow: Workflow) -> List[Dict[str, Any]]:
        """Run all workflow steps until one fails and return the results."""
        results: List[Dict[str, Any]] = []
        for step in workflow.steps:
            try:
                result = self.dispatcher.execute(step.action_name, *step.args, **step.kwargs)
                results.append({"action": step.action_name, "status": "success", "result": result})
            except Exception as exc:
                results.append({"action": step.action_name, "status": "failed", "error": str(exc)})
                break
        return results
