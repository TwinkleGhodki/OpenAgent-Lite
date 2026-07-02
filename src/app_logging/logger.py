import logging
import os
from typing import Optional

from config.settings import settings

_LOGGER_NAME = "agentic_rpa"
_LOGGER: Optional[logging.Logger] = None


def configure_logger() -> logging.Logger:
    """Configure and return a reusable application logger."""
    global _LOGGER

    if _LOGGER is not None:
        return _LOGGER

    log_dir = settings.logs_dir
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "execution.log")

    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    logger.propagate = False

    if logger.handlers:
        _LOGGER = logger
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _LOGGER = logger
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger for a module or component."""
    parent_logger = configure_logger()
    if not name:
        return parent_logger
    return parent_logger.getChild(name)


def log_action(task: str, status: str, level: str = "info") -> None:
    """Write a simple action log entry while preserving the old call signature."""
    logger = get_logger("actions")
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(f"{task} - {status}")
