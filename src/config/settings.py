from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR.parent / ".env")


@dataclass(frozen=True)
class Settings:
    """Centralized configuration values for the automation application."""

    gmail_email: str = os.getenv("GMAIL_EMAIL", "")
    gmail_password: str = os.getenv("GMAIL_PASSWORD", "")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "phi3:3.8b-mini-128k-instruct-q4_0")
    pexels_api_key: str = os.getenv("PEXELS_API_KEY", "")
    download_dir: str = os.getenv("DOWNLOAD_DIR", str(ROOT_DIR.parent / "downloads"))
    logs_dir: str = os.getenv("LOGS_DIR", str(ROOT_DIR.parent / "logs"))
    downloaded_images_dir: str = os.getenv("DOWNLOADED_IMAGES_DIR", str(ROOT_DIR.parent / "downloaded_images"))
    screenshot_path: str = os.getenv("SCREENSHOT_PATH", str(ROOT_DIR.parent / "screenshot.png"))
    browser_timeout: int = int(os.getenv("BROWSER_TIMEOUT", "30"))
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
