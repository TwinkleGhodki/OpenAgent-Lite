import importlib.util
import os
import sys
from pathlib import Path

stdlib_logging_path = Path(os.__file__).resolve().parent / "logging" / "__init__.py"
spec = importlib.util.spec_from_file_location("logging", str(stdlib_logging_path))
stdlib_logging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stdlib_logging)

stdlib_logging.__file__ = str(stdlib_logging_path)
stdlib_logging.__package__ = "logging"
stdlib_logging.__path__ = [str(Path(__file__).resolve().parent)]

for name in dir(stdlib_logging):
    if not hasattr(sys.modules[__name__], name):
        globals()[name] = getattr(stdlib_logging, name)

sys.modules[__name__] = stdlib_logging
sys.modules["logging"] = stdlib_logging
