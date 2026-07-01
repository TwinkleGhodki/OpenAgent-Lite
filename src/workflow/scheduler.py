import schedule
import time
from task_runner import delete_temp_files, rename_files, open_youtube

def run_scheduler():
    # Scheduling the tasks
    schedule.every().day.at("18:00").do(delete_temp_files)
    schedule.every().monday.at("09:00").do(rename_files, folder_path="path/to/your/folder")
    schedule.every().day.at("08:00").do(open_youtube)

    print("Scheduler started. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(1)

