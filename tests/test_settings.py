import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def test_settings_loads_environment_values(monkeypatch):
    monkeypatch.setenv("GMAIL_EMAIL", "test@example.com")
    monkeypatch.setenv("GMAIL_PASSWORD", "secret")
    monkeypatch.setenv("OLLAMA_HOST", "http://example:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "mini")
    monkeypatch.setenv("BROWSER_TIMEOUT", "15")
    monkeypatch.setenv("SMTP_PORT", "2525")

    sys.modules.pop("config.settings", None)
    settings_module = importlib.import_module("config.settings")

    assert settings_module.settings.gmail_email == "test@example.com"
    assert settings_module.settings.gmail_password == "secret"
    assert settings_module.settings.ollama_host == "http://example:11434"
    assert settings_module.settings.ollama_model == "mini"
    assert settings_module.settings.browser_timeout == 15
    assert settings_module.settings.smtp_port == 2525
