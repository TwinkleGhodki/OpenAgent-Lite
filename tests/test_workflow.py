import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dispatcher.dispatcher import Dispatcher
from workflow.engine import Workflow, WorkflowExecutor, WorkflowStep


def test_successful_workflow_returns_results_for_every_step():
    dispatcher = Dispatcher()
    dispatcher.register("first", lambda: "one")
    dispatcher.register("second", lambda: "two")

    workflow = Workflow([WorkflowStep("first"), WorkflowStep("second")])
    executor = WorkflowExecutor(dispatcher)

    results = executor.execute(workflow)

    assert [item["status"] for item in results] == ["success", "success"]
    assert [item["result"] for item in results] == ["one", "two"]


def test_failed_workflow_stops_on_first_failure():
    dispatcher = Dispatcher()
    dispatcher.register("first", lambda: "ok")
    dispatcher.register("second", lambda: (_ for _ in ()).throw(RuntimeError("boom")))

    workflow = Workflow([WorkflowStep("first"), WorkflowStep("second")])
    executor = WorkflowExecutor(dispatcher)

    results = executor.execute(workflow)

    assert len(results) == 2
    assert results[0]["status"] == "success"
    assert results[1]["status"] == "failed"
    assert "boom" in results[1]["error"]


def test_empty_workflow_returns_no_results():
    dispatcher = Dispatcher()
    executor = WorkflowExecutor(dispatcher)

    results = executor.execute(Workflow())

    assert results == []
