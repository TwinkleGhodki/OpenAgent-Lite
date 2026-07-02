import re
from typing import Any, Dict, List

import requests

from config.settings import settings

SYSTEM_PROMPT = """
You are a strict automation task decomposition agent.

Your job is to convert natural language requests into valid Python function calls based on a predefined set of functions.

Allowed functions:
- open_youtube()
- search_youtube('search_query')
- open_google()
- search_google('query')
- rename_files('folder_path')
- delete_temp_files('folder_path')
- download_pdfs('url')
- send_email('subject', 'body', 'to_email', 'attachment_path')
- download_images('query')
- take_screenshot()
- write_to_file('file_path', 'content')
- web_scrape('url')

RULES:
- Only output function calls if you are certain of the required arguments from user input.
- Carefully separate all arguments. Especially for send_email:
  - subject must be string
  - body must be string
  - to_email must be a valid email address, and must NOT be part of the body
- NEVER include the email address inside the body or subject.
- Output ONLY valid python function calls, one per line. NO explanation.
- Be strict, be literal.

Examples:
Input: "Open YouTube"
Output: open_youtube()

Input: "Search YouTube for cats"
Output: search_youtube('cats')

Input: "Take a screenshot"
Output: take_screenshot()

Input: "Send email to John" (missing subject, body, attachment)
Output: (Nothing)
"""


class OllamaLLMService:
    """Encapsulate LLM interaction and response parsing for the automation app."""

    def __init__(self) -> None:
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.timeout = settings.browser_timeout

    def _build_messages(self, user_goal: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_goal},
        ]

    def _request(self, user_goal: str) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": self._build_messages(user_goal),
            "stream": False,
        }
        endpoint = f"{self.host.rstrip('/')}/api/chat"

        try:
            response = requests.post(endpoint, json=payload, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise RuntimeError(f"Unable to connect to Ollama at {self.host}: request timed out after {self.timeout}s") from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(f"Unable to connect to Ollama at {self.host}: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc
        except ConnectionError as exc:
            raise RuntimeError(f"Unable to connect to Ollama at {self.host}: {exc}") from exc

        if response.status_code != 200:
            raise RuntimeError(f"Ollama request failed with status {response.status_code}: {response.text}")

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError("Ollama returned an invalid response payload") from exc

    def generate_subtasks(self, user_goal: str) -> List[str]:
        response = self._request(user_goal)
        content = response.get("message", {}).get("content", "")
        return parse_subtasks(content)


_llm_service = OllamaLLMService()


def run_llm_agent(user_goal: str) -> List[str]:
    return _llm_service.generate_subtasks(user_goal)


def parse_subtasks(content: str) -> List[str]:
    # Match valid function calls line-by-line
    pattern = r'(?:^|\n)(open_youtube\(\)|search_youtube\(.*?\)|open_google\(\)|search_google\(.*?\)|rename_files\(.*?\)|delete_temp_files\(.*?\)|download_pdfs\(.*?\)|send_email\(.*?\)|download_images\(.*?\)|take_screenshot\(\)|write_to_file\(.*?\)|web_scrape\(.*?\))'
    matches = re.findall(pattern, content, flags=re.MULTILINE)

    # Filter out calls with any dummy placeholders
    blacklist_keywords = [
        'query', 'filepath', 'url', 'content', 'example.com',
        'spreadsheet', 'attachment', 'subject', 'to_email'
    ]

    def is_valid(call: str) -> bool:
        return not any(keyword in call.lower() for keyword in blacklist_keywords)

    valid_calls = [call.strip() for call in matches if is_valid(call)]

    return valid_calls
