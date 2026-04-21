from typing import Dict, List, Optional
from src.core.task import Task
from src.plugins.base import BasePlugin

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.plugins: List[BasePlugin] = []

    def add_task(self, task: Task):
        self.tasks[task.id] = task
        self.refresh_statuses()

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.refresh_statuses()

    def refresh_statuses(self):
        changed = True
        while changed:
            changed = False
            for task in self.tasks.values():
                if task.status == "completed":
                    continue
                
                is_blocked = False
                for dep_id in task.dependencies:
                    dep = self.tasks.get(dep_id)
                    if not dep or dep.status != "completed":
                        is_blocked = True
                        break
                
                new_status = "blocked" if is_blocked else "pending"
                if task.status != new_status:
                    task.update_status(new_status)
                    changed = True

    def register_plugin(self, plugin: BasePlugin):
        self.plugins.append(plugin)

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.execute(self)

    def update_task_status(self, task_id: str, status: str):
        task = self.get_task(task_id)
        if task:
            task.update_status(status)
            self.refresh_statuses()
