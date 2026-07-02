import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm.llm_agent import OllamaLLMService


class OllamaLLMServiceTests(unittest.TestCase):
    def test_generate_subtasks_uses_settings_host_and_parses_response(self):
        with patch("llm.llm_agent.settings") as settings:
            settings.ollama_model = "test-model"
            settings.ollama_host = "http://example"
            settings.browser_timeout = 12
            service = OllamaLLMService()

            fake_response = SimpleNamespace(status_code=200, json=lambda: {"message": {"content": "open_youtube()\nsearch_google('cats')"}}, text="")
            with patch("llm.llm_agent.requests.post", return_value=fake_response) as mock_post:
                subtasks = service.generate_subtasks("Open YouTube")

        self.assertEqual(subtasks, ["open_youtube()", "search_google('cats')"])
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 12)
        self.assertIn("http://example/api/chat", mock_post.call_args.args[0])

    def test_generate_subtasks_raises_clear_error_for_connection_failure(self):
        with patch("llm.llm_agent.settings") as settings:
            settings.ollama_model = "test-model"
            settings.ollama_host = "http://example"
            settings.browser_timeout = 8
            service = OllamaLLMService()

            with patch("llm.llm_agent.requests.post", side_effect=ConnectionError("connection refused")):
                with self.assertRaisesRegex(RuntimeError, "Unable to connect"):
                    service.generate_subtasks("Open Google")


if __name__ == "__main__":
    unittest.main()
