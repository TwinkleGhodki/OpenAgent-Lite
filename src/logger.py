import os
import datetime

# Get absolute path to logs folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'execution.log')

# Make sure logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log_action(task, status):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - {task} - {status}\n")
