# Task 3: Data Layer (Atomic JSON Storage) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the JSON storage layer with atomic writes and address feedback from Task 2.

**Architecture:** Use `JSONStorage` for atomic JSON persistence and update `Task` and `TaskManager` to support status updates and task deletion with dependency re-evaluation.

**Tech Stack:** Python, pytest

---

### Task 1: Update Task and Manager

**Files:**
- Modify: `src/core/task.py`
- Modify: `src/core/manager.py`
- Modify: `tests/core/test_manager.py`

- [ ] **Step 1: Add update_status to Task**
```python
def update_status(self, new_status: str):
    from datetime import datetime
    self.status = new_status
    self.updated_at = datetime.now().isoformat()
```

- [ ] **Step 2: Update TaskManager to use update_status**
Update `refresh_statuses` to use `task.update_status`.
Add `update_task_status(self, task_id, status)`.

- [ ] **Step 3: Add test_delete_task to tests/core/test_manager.py**
```python
def test_delete_task():
    manager = TaskManager()
    task_a = Task(id="A", title="Task A", status="completed")
    task_b = Task(id="B", title="Task B", dependencies=["A"], status="pending")
    manager.add_task(task_a)
    manager.add_task(task_b)
    
    manager.delete_task("A")
    assert manager.get_task("A") is None
    assert manager.get_task("B").status == "blocked"
```

### Task 2: Implement JSONStorage (TDD)

**Files:**
- Create: `src/core/storage.py`
- Create: `tests/core/test_storage.py`

- [ ] **Step 1: Write failing test for JSONStorage**
Create `tests/core/test_storage.py`:
```python
import os
import json
from src.core.storage import JSONStorage
from src.core.task import Task

def test_save_and_load_tasks(tmp_path):
    file_path = tmp_path / "tasks.json"
    storage = JSONStorage(str(file_path))
    tasks = {"1": Task(id="1", title="Persisted Task")}
    
    storage.save(tasks)
    loaded_tasks = storage.load()
    
    assert "1" in loaded_tasks
    assert loaded_tasks["1"].title == "Persisted Task"
```

- [ ] **Step 2: Run test and verify it fails**
Run: `pytest tests/core/test_storage.py -v`

- [ ] **Step 3: Implement JSONStorage**
Create `src/core/storage.py`:
```python
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
```

- [ ] **Step 4: Run all tests**
Run: `pytest`

### Task 3: Commit Changes

- [ ] **Step 1: Commit everything**
```bash
git add src/core/task.py src/core/manager.py src/core/storage.py tests/core/test_manager.py tests/core/test_storage.py
git commit -m "feat: add JSONStorage with atomic writes and improve Task/Manager robustness"
```
