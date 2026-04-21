import argparse
import sys
import uuid
from datetime import datetime
from src.core.manager import TaskManager
from src.core.storage import JSONStorage
from src.core.task import Task
from src.plugins.ai_prioritizer import AIPrioritizerPlugin

STORAGE_FILE = "tasks.json"

# ANSI Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_status_color(status):
    if status == "completed": return GREEN
    if status == "blocked": return RED
    if status == "in_progress": return BLUE
    return YELLOW

def main():
    storage = JSONStorage(STORAGE_FILE)
    manager = TaskManager()
    manager.tasks = storage.load()
    manager.register_plugin(AIPrioritizerPlugin())

    parser = argparse.ArgumentParser(description="AI-Powered Task Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--desc", default="", help="Task description")
    add_parser.add_argument("--deadline", help="Task deadline (ISO format: YYYY-MM-DD)")
    add_parser.add_argument("--dep", nargs="*", default=[], help="IDs of tasks this task depends on")

    # List Tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--sort", choices=["priority", "status", "date"], default="priority", help="Sort order")

    # Prioritize
    subparsers.add_parser("prioritize", help="Run AI prioritization")

    # Complete Task
    comp_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    comp_parser.add_argument("id", help="Task ID")

    # Delete Task
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", help="Task ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "add":
        task_id = str(uuid.uuid4())[:8]
        new_task = Task(
            id=task_id,
            title=args.title,
            description=args.desc,
            deadline=args.deadline,
            dependencies=args.dep
        )
        manager.add_task(new_task)
        storage.save(manager.tasks)
        print(f"{GREEN}Task added successfully with ID: {task_id}{RESET}")

    elif args.command == "list":
        tasks = list(manager.tasks.values())
        if args.sort == "priority":
            tasks.sort(key=lambda t: t.priority, reverse=True)
        elif args.sort == "date":
            tasks.sort(key=lambda t: t.created_at)
        
        if not tasks:
            print("No tasks found.")
            return

        print(f"\n{'ID':<10} {'STATUS':<12} {'PRIO':<6} {'TITLE'}")
        print("-" * 50)
        for task in tasks:
            color = get_status_color(task.status)
            print(f"{task.id:<10} {color}{task.status.upper():<12}{RESET} {task.priority:<6} {task.title}")

    elif args.command == "prioritize":
        manager.run_plugins()
        storage.save(manager.tasks)
        print(f"{BLUE}AI Prioritization complete.{RESET}")

    elif args.command == "complete":
        task = manager.get_task(args.id)
        if task:
            manager.update_task_status(args.id, "completed")
            storage.save(manager.tasks)
            print(f"{GREEN}Task {args.id} marked as completed.{RESET}")
        else:
            print(f"{RED}Task not found: {args.id}{RESET}")

    elif args.command == "delete":
        if manager.get_task(args.id):
            manager.delete_task(args.id)
            storage.save(manager.tasks)
            print(f"{YELLOW}Task {args.id} deleted.{RESET}")
        else:
            print(f"{RED}Task not found: {args.id}{RESET}")

if __name__ == "__main__":
    main()
