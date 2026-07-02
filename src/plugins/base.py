from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class Plugin(ABC):
    """Simple base class for lightweight automation plugins."""

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the plugin action."""
        raise NotImplementedError
