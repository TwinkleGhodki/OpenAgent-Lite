from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import List, Type

from .base import Plugin


def discover_plugins() -> List[Plugin]:
    """Discover and instantiate plugins from the plugins package automatically."""
    plugins: List[Plugin] = []
    package_path = Path(__file__).resolve().parent

    for module_info in pkgutil.iter_modules([str(package_path)]):
        if module_info.name.startswith("_"):
            continue
        if module_info.name == "base":
            continue

        module = importlib.import_module(f"plugins.{module_info.name}")
        for _, obj in vars(module).items():
            if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                plugin = obj()
                plugins.append(plugin)

    return plugins


__all__ = ["Plugin", "discover_plugins"]
