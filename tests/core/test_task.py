from src.core.task import Task
from datetime import datetime

def test_task_creation():
    task = Task(
        id="1",
        title="Test Task",
        description="A test description",
        deadline="2026-04-25"
    )
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.status == "pending"
    assert task.priority == 0
    assert isinstance(task.created_at, str)
