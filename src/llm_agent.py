import ollama
import re

def run_llm_agent(user_goal):
    response = ollama.chat(
        model='phi3:3.8b-mini-128k-instruct-q4_0',
        messages=[
            {
                "role": "system",
                "content": """
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
            },
            {"role": "user", "content": user_goal}
        ]
    )

    content = response['message']['content']
    return parse_subtasks(content)

def parse_subtasks(content):
    # Match valid function calls line-by-line
    pattern = r'(?:^|\n)(open_youtube\(\)|search_youtube\(.*?\)|open_google\(\)|search_google\(.*?\)|rename_files\(.*?\)|delete_temp_files\(.*?\)|download_pdfs\(.*?\)|send_email\(.*?\)|download_images\(.*?\)|take_screenshot\(\)|write_to_file\(.*?\)|web_scrape\(.*?\))'
    matches = re.findall(pattern, content, flags=re.MULTILINE)

    # Filter out calls with any dummy placeholders
    blacklist_keywords = [
        'query', 'filepath', 'url', 'content', 'example.com',
        'spreadsheet', 'attachment', 'subject', 'to_email'
    ]

    def is_valid(call):
        return not any(keyword in call.lower() for keyword in blacklist_keywords)

    valid_calls = [call.strip() for call in matches if is_valid(call)]

    return valid_calls
