import os
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from actions.browser import browser_manager


def test_browser_manager_initializes_driver_lazily_and_reuses_singleton(monkeypatch):
    monkeypatch.delenv("CHROME_HEADLESS", raising=False)
    fake_driver = SimpleNamespace(
        set_page_load_timeout=lambda timeout: None,
        implicitly_wait=lambda timeout: None,
        quit=lambda: None,
    )

    with patch("actions.browser.browser_manager.webdriver.Chrome", return_value=fake_driver) as chrome_mock:
        manager = browser_manager.BrowserManager()
        manager._driver = None
        manager._initialized = True

        first = manager.get_driver()
        second = manager.get_driver()

    assert first is fake_driver
    assert second is fake_driver
    assert chrome_mock.call_count == 1


def test_browser_manager_close_handles_missing_driver_and_quit_errors():
    manager = browser_manager.BrowserManager()
    manager._driver = None

    manager.close()

    fake_driver = SimpleNamespace(quit=lambda: (_ for _ in ()).throw(RuntimeError("quit failed")))
    manager._driver = fake_driver

    manager.close()
    assert manager._driver is None
