import json
import os
import shutil
from typing import Dict
from src.core.task import Task

class JSONStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, tasks: Dict[str, Task]):
        data = {id: task.to_dict() for id, task in tasks.items()}
        temp_path = self.file_path + ".tmp"
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=4)
        shutil.move(temp_path, self.file_path)

    def load(self) -> Dict[str, Task]:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return {id: Task.from_dict(task_data) for id, task_data in data.items()}
