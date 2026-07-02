from __future__ import annotations

from typing import Any, Callable, Dict, List


class Dispatcher:
    """Central registry for dispatching named actions to Python callables."""

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., Any]] = {}

    def register(self, action_name: str, function: Callable[..., Any]) -> None:
        """Register a callable under a user-facing action name."""
        if not action_name:
            raise ValueError("Action name cannot be empty")
        if not callable(function):
            raise TypeError("Registered value must be callable")
        self._registry[action_name] = function

    def execute(self, action_name: str, *args: Any, **kwargs: Any) -> Any:
        """Execute a registered action with the provided arguments."""
        if action_name not in self._registry:
            raise KeyError(f"Unknown command: {action_name}")

        try:
            return self._registry[action_name](*args, **kwargs)
        except TypeError as exc:
            raise TypeError(
                f"Missing parameters or invalid arguments for action '{action_name}': {exc}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Execution failed for action '{action_name}': {exc}") from exc

    def list_actions(self) -> List[str]:
        """Return the names of all registered actions."""
        return sorted(self._registry.keys())
