from __future__ import annotations

import atexit
import os
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from app_logging.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class BrowserManager:
    """Manage a single Chrome WebDriver instance with lazy initialization."""

    _instance: Optional["BrowserManager"] = None

    def __new__(cls) -> "BrowserManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self._driver = None
        self._initialized = True

    def get_driver(self):
        if self._driver is None:
            self._driver = self._create_driver()
        return self._driver

    def _create_driver(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if os.getenv("CHROME_HEADLESS", "").lower() in {"1", "true", "yes"}:
            options.add_argument("--headless=new")

        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException as exc:
            logger.exception("Failed to start Chrome WebDriver")
            raise RuntimeError(f"Unable to start Chrome driver: {exc}") from exc
        except Exception as exc:
            logger.exception("Unexpected error while creating Chrome WebDriver")
            raise RuntimeError(f"Unable to start Chrome driver: {exc}") from exc

        try:
            driver.set_page_load_timeout(settings.browser_timeout)
            driver.implicitly_wait(settings.browser_timeout)
        except Exception as exc:
            logger.warning("Browser started, but timeout configuration could not be applied: %s", exc)

        return driver

    def close(self) -> None:
        if self._driver is None:
            return

        try:
            self._driver.quit()
        except Exception as exc:
            logger.exception("Error while shutting down Chrome WebDriver")
        finally:
            self._driver = None


_manager = BrowserManager()
atexit.register(_manager.close)


def get_driver():
    return _manager.get_driver()


def close_driver():
    _manager.close()


__all__ = ["BrowserManager", "get_driver", "close_driver"]
