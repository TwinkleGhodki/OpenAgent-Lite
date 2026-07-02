import logging
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app_logging import logger as app_logger


def test_configure_logger_returns_singleton_logger(tmp_path):
    app_logger._LOGGER = None

    with patch("app_logging.logger.settings") as settings:
        settings.logs_dir = str(tmp_path)
        settings.log_level = "INFO"

        configured = app_logger.configure_logger()
        same = app_logger.configure_logger()

    assert configured is same
    assert configured.name == "agentic_rpa"
    assert configured.level == logging.INFO


def test_log_action_uses_child_logger(tmp_path):
    app_logger._LOGGER = None

    with patch("app_logging.logger.settings") as settings:
        settings.logs_dir = str(tmp_path)
        settings.log_level = "INFO"

        with patch.object(app_logger, "get_logger") as mock_get_logger:
            mock_logger = logging.getLogger("test")
            mock_get_logger.return_value = mock_logger
            app_logger.log_action("task", "done")

    mock_get_logger.assert_called_once_with("actions")
