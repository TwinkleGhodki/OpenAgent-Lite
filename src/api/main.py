from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from dispatcher.dispatcher import Dispatcher
    from plugins import discover_plugins
except ModuleNotFoundError:  # pragma: no cover - exercised when running via uvicorn from repo root
    from src.dispatcher.dispatcher import Dispatcher
    from src.plugins import discover_plugins


class ActionRequest(BaseModel):
    """Request body for executing a registered action."""

    action: str = Field(..., description="Registered action name")
    args: List[Any] = Field(default_factory=list, description="Positional arguments")
    kwargs: Dict[str, Any] = Field(default_factory=dict, description="Keyword arguments")


class ActionResponse(BaseModel):
    """Structured response for a successful action execution."""

    action: str
    result: Any


class ErrorResponse(BaseModel):
    """Structured response for action execution errors."""

    detail: str


app = FastAPI(title="OpenAgent-Lite API")


def _build_dispatcher() -> Dispatcher:
    """Create a dispatcher and register actions via the existing plugin discovery flow."""
    dispatcher = Dispatcher()
    for plugin in discover_plugins():
        dispatcher.register_plugin(plugin)
    return dispatcher


@app.get("/health")
def health() -> Dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.get("/actions", response_model=List[str])
def list_actions() -> List[str]:
    """List all registered actions exposed through the dispatcher."""
    return _build_dispatcher().list_actions()


@app.post("/execute", response_model=ActionResponse, responses={400: {"model": ErrorResponse}})
def execute_action(request: ActionRequest) -> ActionResponse:
    """Execute a registered action and return a structured JSON response."""
    dispatcher = _build_dispatcher()
    try:
        result = dispatcher.execute(request.action, *request.args, **request.kwargs)
    except (KeyError, TypeError, RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ActionResponse(action=request.action, result=result)
