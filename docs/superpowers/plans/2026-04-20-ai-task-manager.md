# AI-Powered Task Management System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-ready, extensible CLI-based Task Management System in Python with AI-driven prioritization.

**Architecture:** Modular Plugin-based architecture. A central `TaskManager` handles core logic and storage, while an extensible plugin system allows for AI prioritization and future features.

**Tech Stack:** Python 3.x, `pytest` for testing, `argparse` for CLI, and standard `json` for storage.

---

### Task 1: Project Setup & Core Task Model

**Files:**
- Create: `src/core/task.py`
- Test: `tests/core/test_task.py`

- [ ] **Step 1: Write the failing test for Task model**

```python
# tests/core/test_task.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/core/test_task.py -v`
Expected: FAIL (Module not found/Import error)

- [ ] **Step 3: Write minimal implementation of Task class**

```python
# src/core/task.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    status: str = "pending"
    priority: int = 0
    deadline: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/core/test_task.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/core/task.py tests/core/test_task.py
git commit -m "feat: add core task model"
```

---

### Task 2: Task Manager (CRUD & Dependencies)

**Files:**
- Create: `src/core/manager.py`
- Test: `tests/core/test_manager.py`

- [ ] **Step 1: Write failing tests for TaskManager**

```python
# tests/core/test_manager.py
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
```

- [ ] **Step 2: Run tests to verify failure**

Run: `pytest tests/core/test_manager.py -v`
Expected: FAIL

- [ ] **Step 3: Implement TaskManager**

```python
# src/core/manager.py
from typing import Dict, List, Optional
from src.core.task import Task

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

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
        for task in self.tasks.values():
            if task.status == "completed":
                continue
            
            is_blocked = False
            for dep_id in task.dependencies:
                dep = self.tasks.get(dep_id)
                if not dep or dep.status != "completed":
                    is_blocked = True
                    break
            
            if is_blocked:
                task.status = "blocked"
            elif task.status == "blocked":
                task.status = "pending"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_manager.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/core/manager.py tests/core/test_manager.py
git commit -m "feat: add TaskManager with dependency logic"
```

---

### Task 3: Data Layer (Atomic JSON Storage)

**Files:**
- Create: `src/core/storage.py`
- Test: `tests/core/test_storage.py`

- [ ] **Step 1: Write failing tests for Storage**

```python
# tests/core/test_storage.py
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

- [ ] **Step 2: Run tests to verify failure**

Run: `pytest tests/core/test_storage.py -v`
Expected: FAIL

- [ ] **Step 3: Implement JSONStorage with atomic writes**

```python
# src/core/storage.py
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

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/core/test_storage.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/core/storage.py tests/core/test_storage.py
git commit -m "feat: add JSONStorage with atomic writes"
```

---

### Task 4: Plugin System Base

**Files:**
- Create: `src/plugins/base.py`
- Modify: `src/core/manager.py`

- [ ] **Step 1: Create BasePlugin class**

```python
# src/plugins/base.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def execute(self, task_manager):
        pass
```

- [ ] **Step 2: Update TaskManager to support plugins**

```python
# src/core/manager.py (Update)
from src.plugins.base import BasePlugin

# Add to __init__:
# self.plugins: List[BasePlugin] = []

# Add methods:
# def register_plugin(self, plugin: BasePlugin):
#     self.plugins.append(plugin)

# def run_plugins(self):
#     for plugin in self.plugins:
#         plugin.execute(self)
```

- [ ] **Step 3: Commit**

```bash
git add src/plugins/base.py src/core/manager.py
git commit -m "feat: add plugin base and registry"
```

---

### Task 5: AI Prioritizer Plugin

**Files:**
- Create: `src/plugins/ai_prioritizer.py`
- Test: `tests/plugins/test_ai_prioritizer.py`

- [ ] **Step 1: Write failing test for AI Prioritizer**

```python
# tests/plugins/test_ai_prioritizer.py
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
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/plugins/test_ai_prioritizer.py -v`
Expected: FAIL

- [ ] **Step 3: Implement AIPrioritizerPlugin logic**

```python
# src/plugins/ai_prioritizer.py
from src.plugins.base import BasePlugin
from datetime import datetime

class AIPrioritizerPlugin(BasePlugin):
    def execute(self, manager):
        for task in manager.tasks.values():
            score = 0
            
            # 1. Keyword Check (Urgency)
            urgency_words = ["critical", "urgent", "asap", "important"]
            if any(word in task.title.lower() for word in urgency_words):
                score += 3
            
            # 2. Dependency Impact
            dependents = [t for t in manager.tasks.values() if task.id in t.dependencies]
            score += len(dependents) * 2
            
            # 3. Deadline Proximity (Simplified)
            if task.deadline:
                try:
                    due = datetime.fromisoformat(task.deadline)
                    days_left = (due - datetime.now()).days
                    if days_left < 3: score += 5
                    elif days_left < 7: score += 2
                except ValueError:
                    pass
            
            task.priority = min(score, 10)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/plugins/test_ai_prioritizer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/plugins/ai_prioritizer.py tests/plugins/test_ai_prioritizer.py
git commit -m "feat: add AI Prioritizer plugin"
```

---

### Task 6: CLI Interface

**Files:**
- Create: `src/cli/main.py`

- [ ] **Step 1: Implement CLI entry point**

```python
# src/cli/main.py
import argparse
import sys
import uuid
from src.core.manager import TaskManager
from src.core.storage import JSONStorage
from src.core.task import Task
from src.plugins.ai_prioritizer import AIPrioritizerPlugin

STORAGE_FILE = "tasks.json"

def main():
    storage = JSONStorage(STORAGE_FILE)
    manager = TaskManager()
    manager.tasks = storage.load()
    manager.register_plugin(AIPrioritizerPlugin())

    parser = argparse.ArgumentParser(description="AI Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Add Task
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("--desc", default="")
    add_parser.add_argument("--dep", nargs="*", default=[])

    # List Tasks
    subparsers.add_parser("list")

    # Prioritize
    subparsers.add_parser("prioritize")

    args = parser.parse_args()

    if args.command == "add":
        new_task = Task(id=str(uuid.uuid4())[:8], title=args.title, description=args.desc, dependencies=args.dep)
        manager.add_task(new_task)
        storage.save(manager.tasks)
        print(f"Task added: {new_task.id}")

    elif args.command == "list":
        for task in manager.tasks.values():
            print(f"[{task.status.upper()}] {task.id}: {task.title} (P:{task.priority})")

    elif args.command == "prioritize":
        manager.run_plugins()
        storage.save(manager.tasks)
        print("AI Prioritization complete.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify CLI works manually**

Run: `python -m src.cli.main add "Fix everything" --desc "Urgent bug"`
Run: `python -m src.cli.main prioritize`
Run: `python -m src.cli.main list`

- [ ] **Step 3: Commit**

```bash
git add src/cli/main.py
git commit -m "feat: implement CLI interface"
```

---

### Task 7: Final Polish & Verification

- [ ] **Step 1: Run full test suite**

Run: `pytest`
Expected: ALL PASS

- [ ] **Step 2: Final Commit**

```bash
git commit --allow-empty -m "docs: finalize AI Task Manager implementation"
```
