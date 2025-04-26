# tests/test_basic.py

import sys
import os
import json
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion


################################# load_tasks #################################
TEST_FILE = "test_tasks.json"

def setup_module(module):
    # This will run before all tests in this module
    with open(TEST_FILE, "w") as f:
        json.dump([{"task": "Do something"}], f)

def teardown_module(module):
    # Clean up after tests
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_load_valid_file():
    tasks = load_tasks(TEST_FILE)
    assert isinstance(tasks, list)
    assert tasks[0]["task"] == "Do something"

def test_file_not_found():
    assert load_tasks("non_existent_file.json") == []

def test_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid: json}")
    tasks = load_tasks(str(bad_file))
    assert tasks == []


################################# save_tasks #################################
def test_save_tasks_creates_file_with_correct_content():
    test_file = "test_tasks_output.json"
    tasks_data = [
        {"title": "Eat Rock", "completed": False}
    ]

    # Call the function
    save_tasks(tasks_data, file_path=test_file)

    # Verify file was created and contents are correct
    assert os.path.exists(test_file), "File was not created"
    with open(test_file, "r") as f:
        loaded_data = json.load(f)
    assert loaded_data == tasks_data, "Saved data does not match expected"

    # Clean up
    os.remove(test_file)

################################# generate_unique_id #################################
def test_generate_unique_id_empty_list():
    tasks = []
    assert generate_unique_id(tasks) == 1

def test_generate_unique_id_non_empty_list():
    tasks = [
        {"id": 1, "title": "Squidward"},
        {"id": 2, "title": "Your shoe is untied"},
        {"id": 5, "title": "super mario world central production 2"}
    ]
    assert generate_unique_id(tasks) == 6

################################# filter_tasks_by_priority #################################
def test_filter_tasks_by_priority_high():
    tasks = [
        {"id": 1, "title": "I burned my toast", "priority": "High"},
        {"id": 2, "title": "I got burnt by my toast", "priority": "Medium"},
        {"id": 3, "title": "my toast turned back into bread", "priority": "High"},
    ]
    filtered = filter_tasks_by_priority(tasks, "High")
    assert len(filtered) == 2
    assert all(task["priority"] == "High" for task in filtered)

def test_filter_tasks_by_priority_none():
    tasks = [
        {"id": 1, "title": "hi grader there is probably a 4 percent chance you are reading this", "priority": "Low"},
        {"id": 2, "title": "I was a grader for cs1570 back in the day", "priority": "Medium"},
    ]
    filtered = filter_tasks_by_priority(tasks, "High")
    assert filtered == []




################################# filter_tasks_by_category #################################
def test_filter_tasks_by_category_match():
    tasks = [
        {"id": 1, "title": "build a fish", "category": "Personal"},
        {"id": 2, "title": "win tic-tac-toe", "category": "Work"},
        {"id": 3, "title": "teach my cat how to make a mean stromboli", "category": "Personal"},
    ]
    filtered = filter_tasks_by_category(tasks, "Personal")
    assert len(filtered) == 2
    assert all(task["category"] == "Personal" for task in filtered)

def test_filter_tasks_by_category_none():
    tasks = [
        {"id": 1, "title": "experience left beef", "category": "Work"},
        {"id": 2, "title": "use your bones", "category": "School"},
    ]
    filtered = filter_tasks_by_category(tasks, "Personal")
    assert filtered == []

################################# filter_tasks_by_completion #################################
def test_filter_tasks_by_completion_true():
    tasks = [
        {"id": 1, "title": "remove all evidence", "completed": True},
        {"id": 2, "title": "jump right in joy", "completed": False},
        {"id": 3, "title": "throw a rock into a silo", "completed": True},
    ]
    filtered = filter_tasks_by_completion(tasks, True)
    assert len(filtered) == 2
    assert all(task["completed"] for task in filtered)

def test_filter_tasks_by_completion_false():
    tasks = [
        {"id": 1, "title": "activate bankruptcy mode", "completed": True},
        {"id": 2, "title": "learn how the knight moves", "completed": False},
    ]
    filtered = filter_tasks_by_completion(tasks, False)
    assert len(filtered) == 1
    assert filtered[0]["completed"] is False
################################# search_tasks #################################
#import list getting too long
from tasks import search_tasks

def test_search_tasks_found():
    tasks = [
        {"id": 1, "title": "play tennis with ambivalence", "description": "tennis is where you find peace"},
        {"id": 2, "title": "bullet william", "description": "there is a guy at my school named bullet william"},
        {"id": 3, "title": "this is taking too long", "description": "aaaaaaaaaaaaaaaaaaaaaaaaa bullet william"},
    ]
    query = "bullet william"
    results = search_tasks(tasks, query)
    assert len(results) == 2
    assert results[0]["title"] == "bullet william"
    results2 = search_tasks(tasks, "e")
    assert len(results2) == 3

def test_search_tasks_not_found():
    tasks = [
        {"id": 1, "title": "use the spoon", "description": "dont even think of using the wrench"},
        {"id": 2, "title": "quiz the frog", "description": "he needs to score well on this test"},
    ]
    query = "a"
    results = search_tasks(tasks, query)
    assert len(results) == 0
################################# get_overdue_tasks #################################
from tasks import get_overdue_tasks 

def test_get_overdue_tasks():
    tasks = [
        {"id": 1, "title": "Task 1", "completed": False, "due_date": "1025-05-31"},
        {"id": 2, "title": "Task 2", "completed": True, "due_date": "2025-04-09"},
        {"id": 3, "title": "Task 3", "completed": False, "due_date": "2025-05-31"},
        {"id": 4, "title": "Task 4", "completed": False, "due_date": "2025-05-31"},
        {"id": 5, "title": "Task 5", "completed": False, "due_date": "2025-04-09"},
    ]
    
    
    # Get overdue tasks
    overdue_tasks = get_overdue_tasks(tasks)
    
    # Check if the overdue tasks are correctly identified
    assert len(overdue_tasks) == 2  # There should be two overdue tasks
    
    # Check the specific tasks
    overdue_titles = [task["title"] for task in overdue_tasks]
    assert "Task 1" in overdue_titles  # Task 1 is overdue
    assert "Task 5" in overdue_titles  # Task 5 is overdue
    
    # Make sure tasks that are completed are not included
    assert "Task 2" not in overdue_titles  # Task 2 is completed, so it's not overdue
    
    # Make sure tasks that are not overdue are not included
    assert "Task 3" not in overdue_titles  # Task 3 is not overdue
    assert "Task 4" not in overdue_titles  # Task 4 is not overdue


################################# except blocks #################################
def test_generate_unique_id_invalid_task():
    tasks = [{"id": 1}, {}, {"name": "task with no id"}]
    assert generate_unique_id(tasks) == 2  # Only one valid ID

def test_filter_tasks_by_priority_invalid():
    tasks = [{"priority": "High"}, {"other": "other"}, "very cool string that is not a dict"]
    result = filter_tasks_by_priority(tasks, "High")
    assert result == [{"priority": "High"}]

def test_search_tasks_missing_fields():
    tasks = [{"title": "Buy milk"}, {"description": "milk"}, {}, {"title": None}]
    result = search_tasks(tasks, "milk")
    assert len(result) == 0 #if it is missing one field, it should raise an error

def test_get_overdue_tasks_edge_cases():
    tasks = [
        {"due_date": "2020-01-01", "completed": False},  
        {"due_date": "this is not a due date, it is a string!", "completed": False},  
        {"completed": False},                            
        "I dont think i am supposed to be here",                                    
    ]
    result = get_overdue_tasks(tasks)
    assert len(result) == 1
