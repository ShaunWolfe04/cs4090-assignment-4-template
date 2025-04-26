import sys
import os
import json
import pytest
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tasks import filter_tasks_by_priority, get_overdue_tasks

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 2),
    ("Medium", 1),
    ("Low", 0),
])
def test_filter_tasks_by_priority_param(priority, expected_count):
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "High"},
        {"id": 3, "priority": "Medium"},
        {"id": 4},  # No priority
    ]
    filtered = filter_tasks_by_priority(tasks, priority)
    assert len(filtered) == expected_count




def test_get_overdue_tasks_with_mocked_date(mocker):
    tasks = [
        {"id": 1, "title": "Task 1", "due_date": "2000-01-01", "completed": False},
        {"id": 2, "title": "Task 2", "due_date": "3000-01-01", "completed": False},
    ]

    mocked_now = datetime(2025, 4, 1)
    mocker.patch("tasks.datetime").now.return_value = mocked_now

    # Patch strptime too, to avoid MagicMock from breaking it
    mocker.patch("tasks.datetime.strptime", side_effect=datetime.strptime)

    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1
    assert overdue[0]["id"] == 1
