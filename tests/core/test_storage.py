import os
import json
import pytest
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
