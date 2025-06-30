# executor.py

from task_runner import open_youtube, search_youtube

def parse_subtasks(subtasks):
    """ Simple parser to extract which actions to run """

    for task in subtasks:
        task_lower = task.lower()
        if 'open browser' in task_lower or 'youtube' in task_lower:
            open_youtube()
        elif 'search' in task_lower and 'dsa' in task_lower:
            search_youtube('DSA playlist')
        else:
            print(f"Subtask not recognized for automation: {task}")
