import ast
from typing import Any, Tuple

from llm_agent import run_llm_agent

from browser_manager import close_driver
from dispatcher.dispatcher import Dispatcher
from plugins import discover_plugins


def build_dispatcher() -> Dispatcher:
    """Create a dispatcher and register the existing automation actions via plugins."""
    dispatcher = Dispatcher()
    for plugin in discover_plugins():
        dispatcher.register_plugin(plugin)
    return dispatcher


def manual_menu() -> None:
    print("\nManual Automation Options:")
    print("1. Open YouTube")
    print("2. Rename files")
    print("3. Delete temp files")
    print("4. Search YouTube")
    print("5. Download PDFs from website")
    print("6. Send email with attachment")
    print("7. Start scheduler")
    print("8. Open Google")
    print("9. Search Google")
    print("10. Download Images")
    print("11. Take Screenshot")
    print("12. Write to a Text File")
    print("13. Use LLM Agent")
    print("14. Voice Input Command")
    print("15. Web Scraping")
    print("16. Exit")


def parse_task_call(task: str) -> Tuple[str, Tuple[Any, ...]]:
    """Convert a simple function-call string into an action name and positional args."""
    try:
        parsed = ast.parse(task.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid task format: {task}") from exc

    if not isinstance(parsed.body, ast.Call) or not isinstance(parsed.body.func, ast.Name):
        raise ValueError(f"Unsupported task format: {task}")

    action_name = parsed.body.func.id
    args: list[Any] = []
    for arg in parsed.body.args:
        try:
            args.append(ast.literal_eval(arg))
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"Unsupported argument in task: {task}") from exc
    return action_name, tuple(args)


def execute_subtasks(subtasks: list[str], dispatcher: Dispatcher) -> None:
    for task in subtasks:
        print(f"\nExecuting: {task}")
        try:
            action_name, args = parse_task_call(task)
            dispatcher.execute(action_name, *args)
        except (ValueError, KeyError, TypeError, RuntimeError) as exc:
            print(f"Error executing {task}: {exc}")


def execute_voice_command(dispatcher: Dispatcher) -> None:
    command = dispatcher.execute("voice_command")
    if command:
        subtasks = run_llm_agent(command)
        if subtasks:
            print("\nSubtasks extracted:")
            for sub in subtasks:
                print(sub)
            confirm = input("\nDo you want to execute these tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("\nStarting execution...\n")
                execute_subtasks(subtasks, dispatcher)
            else:
                print("Execution cancelled.")
        else:
            print("No subtasks extracted.")


def main() -> None:
    dispatcher = build_dispatcher()
    while True:
        manual_menu()
        choice = input("\nEnter choice (1-16): ").strip()

        if choice == '1':
            dispatcher.execute("open_youtube")
        elif choice == '2':
            folder = input("Enter folder path to rename files: ")
            dispatcher.execute("rename_files", folder)
        elif choice == '3':
            folder = input("Enter folder path to delete temp files: ")
            dispatcher.execute("delete_temp_files", folder)
        elif choice == '4':
            query = input("Enter search term: ")
            dispatcher.execute("search_youtube", query)
        elif choice == '5':
            url = input("Enter website URL: ")
            dispatcher.execute("download_pdfs", url)
        elif choice == '6':
            subject = input("Enter subject: ")
            body = input("Enter body: ")
            to_email = input("Enter recipient email: ")
            attach = input("Enter attachment path (leave blank if none): ")
            attach = attach if attach.strip() else None
            dispatcher.execute("send_email", subject, body, to_email, attach)
        elif choice == '7':
            print("Scheduler started. Press Ctrl+C to exit.")
            dispatcher.execute("start_scheduler")
        elif choice == '8':
            dispatcher.execute("open_google")
        elif choice == '9':
            query = input("Enter search term: ")
            dispatcher.execute("search_google", query)
        elif choice == '10':
            query = input("Enter image search query: ")
            dispatcher.execute("download_images", query)
        elif choice == '11':
            dispatcher.execute("take_screenshot")
        elif choice == '12':
            filename = input("Enter filename: ")
            content = input("Enter text to write: ")
            dispatcher.execute("write_to_file", filename, content)
        elif choice == '13':
            goal = input("Enter your task goal: ")
            subtasks = run_llm_agent(goal)
            if not subtasks:
                print("No valid subtasks found. Please be more specific.")
                continue
            print("\nSubtasks extracted:")
            for task in subtasks:
                print(task)

            confirm = input("\nDo you want to execute these tasks? (yes/no): ").lower()
            if confirm == 'yes':
                print("\nStarting execution...\n")
                execute_subtasks(subtasks, dispatcher)
            else:
                print("Execution cancelled.")

        elif choice == '14':
            execute_voice_command(dispatcher)
        elif choice == '15':
            url = input("Enter URL to scrape: ")
            dispatcher.execute("web_scrape", url)
        elif choice == '16':
            print("Exiting.")
            close_driver()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 16.")


if __name__ == "__main__":
    main()
