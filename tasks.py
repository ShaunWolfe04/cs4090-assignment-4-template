import json
import os
from datetime import datetime

# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def load_tasks(file_path=DEFAULT_TASKS_FILE):
    """
    Load tasks from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing tasks
        
    Returns:
        list: List of task dictionaries, empty list if file doesn't exist
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Handle corrupted JSON file
        print(f"Warning: {file_path} contains invalid JSON. Creating new tasks list.")
        return []

def save_tasks(tasks, file_path=DEFAULT_TASKS_FILE):
    """
    Save tasks to a JSON file.

    Args:
        tasks (list): List of task dictionaries
        file_path (str): Path to save the JSON file
    """
    try:
        with open(file_path, "w") as f:
            json.dump(tasks, f, indent=2)
    except (IOError, OSError) as file_error:
        print(f"Error saving tasks to file: {file_error}")
    except TypeError as json_error:
        print(f"Error serializing tasks to JSON: {json_error}")
    except Exception as e:
        print(f"Unexpected error in save_tasks: {e}")


def generate_unique_id(tasks):
    """
    Generate a unique ID for a new task.

    Args:
        tasks (list): List of existing task dictionaries

    Returns:
        int: A unique ID for a new task
    """
    try:
        if not tasks:
            return 1
        return max(task["id"] for task in tasks if isinstance(task.get("id"), int)) + 1
    except (TypeError, ValueError) as e:
        print(f"Error generating unique ID: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error in generate_unique_id: {e}")
        return 1

def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by priority level.

    Args:
        tasks (list): List of task dictionaries
        priority (str): Priority level to filter by (High, Medium, Low)

    Returns:
        list: Filtered list of tasks matching the priority
    """
    try:
        return [
            task for task in tasks 
            if isinstance(task, dict) and task.get("priority") == priority
        ]
    except Exception as e:
        print(f"Error in filter_tasks_by_priority: {e}")
        return []


def filter_tasks_by_category(tasks, category):
    """
    Filter tasks by category.
    
    Args:
        tasks (list): List of task dictionaries
        category (str): Category to filter by
        
    Returns:
        list: Filtered list of tasks matching the category
    """
    return [task for task in tasks if task.get("category") == category]

def filter_tasks_by_completion(tasks, completed=True):
    """
    Filter tasks by completion status.
    
    Args:
        tasks (list): List of task dictionaries
        completed (bool): Completion status to filter by
        
    Returns:
        list: Filtered list of tasks matching the completion status
    """
    return [task for task in tasks if task.get("completed") == completed]

def search_tasks(tasks, query):
    """
    Search tasks by a text query in title and description.

    Args:
        tasks (list): List of task dictionaries
        query (str): Search query

    Returns:
        list: Filtered list of tasks matching the search query
    """
    try:
        query = query.lower()
        return [
            task for task in tasks
            if isinstance(task, dict) and (
                query in task.get("title", "").lower() or
                query in task.get("description", "").lower()
            )
        ]
    except Exception as e:
        print(f"Error in search_tasks: {e}")
        return []


def get_overdue_tasks(tasks):
    """
    Get tasks that are past their due date and not completed.

    Args:
        tasks (list): List of task dictionaries

    Returns:
        list: List of overdue tasks
    """
    overdue = []
    today = datetime.now().date()

    try:
        for task in tasks:
            if not isinstance(task, dict):
                continue

            if task.get("completed", False):
                continue

            due_date_str = task.get("due_date", "")
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_date < today:
                    overdue.append(task)
            except ValueError:
                # Invalid date format, skip this task
                continue

        return overdue
    except Exception as e:
        print(f"Error in get_overdue_tasks: {e}")
        return []