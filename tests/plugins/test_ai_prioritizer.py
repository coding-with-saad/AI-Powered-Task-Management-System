from src.plugins.ai_prioritizer import AIPrioritizerPlugin
from src.core.manager import TaskManager
from src.core.task import Task

def test_prioritizes_urgent_keywords():
    manager = TaskManager()
    task = Task(id="1", title="CRITICAL: Fix bug")
    manager.add_task(task)
    
    plugin = AIPrioritizerPlugin()
    plugin.execute(manager)
    
    assert manager.get_task("1").priority > 0

def test_prioritizes_deadline_proximity():
    from datetime import datetime, timedelta
    manager = TaskManager()
    deadline = (datetime.now() + timedelta(days=1)).isoformat()
    task = Task(id="1", title="Quick task", deadline=deadline)
    manager.add_task(task)
    
    plugin = AIPrioritizerPlugin()
    plugin.execute(manager)
    
    assert manager.get_task("1").priority >= 5

def test_prioritizes_dependency_impact():
    manager = TaskManager()
    task_a = Task(id="A", title="Task A")
    task_b = Task(id="B", title="Task B", dependencies=["A"])
    task_c = Task(id="C", title="Task C", dependencies=["A"])
    manager.add_task(task_a)
    manager.add_task(task_b)
    manager.add_task(task_c)
    
    plugin = AIPrioritizerPlugin()
    plugin.execute(manager)
    
    # Task A has 2 dependents
    assert manager.get_task("A").priority == 4
