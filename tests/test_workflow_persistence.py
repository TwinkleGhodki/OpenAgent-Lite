import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workflow.engine import Workflow, WorkflowStep


def test_save_workflow_writes_json(tmp_path):
    workflow = Workflow([WorkflowStep("greet", args=("hello",))])
    path = tmp_path / "workflow.json"

    workflow.save(path)

    data = json.loads(path.read_text())
    assert data["steps"][0]["action_name"] == "greet"
    assert data["steps"][0]["args"] == ["hello"]


def test_load_workflow_restores_steps(tmp_path):
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps({"steps": [{"action_name": "echo", "args": ["world"], "kwargs": {}}]}))

    workflow = Workflow.load(path)

    assert len(workflow.steps) == 1
    assert workflow.steps[0].action_name == "echo"
    assert workflow.steps[0].args == ("world",)


def test_invalid_workflow_file_raises_value_error(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("not valid json")

    try:
        Workflow.load(path)
    except ValueError as exc:
        assert "Invalid workflow file" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid workflow file")
