from task_runner import (
    open_youtube, rename_files, delete_temp_files, search_youtube,
    download_pdfs, send_email, start_scheduler, open_google, search_google,
    download_images, take_screenshot, write_to_file,
    voice_command, web_scrape
)

from scheduler import run_scheduler
from llm_agent import run_llm_agent

from browser_manager import close_driver

def manual_menu():
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

def execute_subtasks(subtasks):
    for task in subtasks:
        print(f"\nExecuting: {task}")
        try:
            eval(task)
        except Exception as e:
            print(f"Error executing {task}: {e}")

def execute_voice_command():
    command = voice_command()
    if command:
        subtasks = run_llm_agent(command)
        if subtasks:
            print("\nSubtasks extracted:")
            for sub in subtasks:
                print(sub)
            confirm = input("\nDo you want to execute these tasks? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("\nStarting execution...\n")
                execute_subtasks(subtasks)
            else:
                print("Execution cancelled.")
        else:
            print("No subtasks extracted.")

def main():
    while True:
        manual_menu()
        choice = input("\nEnter choice (1-16): ").strip()

        if choice == '1':
            open_youtube(driver)
        elif choice == '2':
            folder = input("Enter folder path to rename files: ")
            rename_files(folder)
        elif choice == '3':
            folder = input("Enter folder path to delete temp files: ")
            delete_temp_files(folder)
        elif choice == '4':
            query = input("Enter search term: ")
            search_youtube(query)
        elif choice == '5':
            url = input("Enter website URL: ")
            download_pdfs(url)
        elif choice == '6':
            subject = input("Enter subject: ")
            body = input("Enter body: ")
            to_email = input("Enter recipient email: ")
            attach = input("Enter attachment path (leave blank if none): ")
            attach = attach if attach.strip() else None
            send_email(subject, body, to_email, attach)
        elif choice == '7':
            print("Scheduler started. Press Ctrl+C to exit.")
            start_scheduler()
        elif choice == '8':
            open_google()
        elif choice == '9':
            query = input("Enter search term: ")
            search_google(query, driver)
        elif choice == '10':
            query = input("Enter image search query: ")
            download_images(query)
        elif choice == '11':
            take_screenshot()
        elif choice == '12':
            filename = input("Enter filename: ")
            content = input("Enter text to write: ")
            write_to_file(filename, content)
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
                for task in subtasks:
                    try:
                        print(f"Executing: {task}")
                        exec(task)
                    except Exception as e:
                        print(f"Error executing {task}: {e}")
            else:
                print("Execution cancelled.")

        elif choice == '14':
            execute_voice_command()
        elif choice == '15':
            url = input("Enter URL to scrape: ")
            web_scrape(url)
        elif choice == '16':
            print("Exiting.")
            close_driver()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 16.")

if __name__ == "__main__":
    main()
