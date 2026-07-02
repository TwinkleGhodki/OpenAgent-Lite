import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_actions_endpoint_lists_registered_actions():
    response = client.get("/actions")
    assert response.status_code == 200
    actions = response.json()
    assert "open_youtube" in actions
    assert "start_scheduler" in actions


def test_execute_endpoint_runs_registered_action():
    response = client.post(
        "/execute",
        json={"action": "open_youtube"},
    )
    assert response.status_code == 200
    assert response.json()["action"] == "open_youtube"


def test_execute_endpoint_returns_error_for_unknown_action():
    response = client.post(
        "/execute",
        json={"action": "does_not_exist"},
    )
    assert response.status_code == 400
    assert "Unknown command" in response.json()["detail"]
