from src.core.manager import TaskManager
from src.core.task import Task

def test_add_and_get_task():
    manager = TaskManager()
    task = Task(id="1", title="Task 1")
    manager.add_task(task)
    assert manager.get_task("1").title == "Task 1"

def test_dependency_blocks_task():
    manager = TaskManager()
    task_a = Task(id="A", title="Task A")
    task_b = Task(id="B", title="Task B", dependencies=["A"])
    manager.add_task(task_a)
    manager.add_task(task_b)
    
    # Task B should be blocked because A is pending
    manager.refresh_statuses()
    assert manager.get_task("B").status == "blocked"

def test_dependency_unblocks_task():
    manager = TaskManager()
    task_a = Task(id="A", title="Task A", status="completed")
    task_b = Task(id="B", title="Task B", dependencies=["A"], status="blocked")
    manager.add_task(task_a)
    manager.add_task(task_b)
    
    manager.refresh_statuses()
    assert manager.get_task("B").status == "pending"
