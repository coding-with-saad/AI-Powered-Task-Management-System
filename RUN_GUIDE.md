# Run Guide: AI-Powered Task Management System

This guide outlines the commands to interact with the system, manage tasks, and run the automated test suite.

## 1. Prerequisites
- **Python 3.x**
- **pytest** (for running tests)

## 2. Running the CLI Tool
The system is executed through the main CLI module.

### Core Commands
All commands follow this structure: `python -m src.cli.main [command] [options]`

#### Add a Task
Adds a new task with an optional description, deadline, and dependencies.
```bash
python -m src.cli.main add "Task Title" --desc "Detailed description" --deadline "2026-04-25"
```

#### Add a Task with Dependencies
Specify the IDs of the tasks this new task depends on. It will automatically be marked as `BLOCKED` until all dependencies are `COMPLETED`.
```bash
python -m src.cli.main add "Deploy to Production" --dep 2a5ba236
```

#### List Tasks
Lists all tasks, color-coded by their status.
```bash
python -m src.cli.main list
```
*Optional: Use `--sort [priority|status|date]` to change the display order.*

#### AI Prioritization
Runs the AI plugin to automatically calculate priority scores based on keywords, dependencies, and deadlines.
```bash
python -m src.cli.main prioritize
```

#### Mark a Task as Completed
Completes a task by its ID and automatically unblocks any dependent tasks.
```bash
python -m src.cli.main complete [TASK_ID]
```

#### Delete a Task
Removes a task by its ID and re-evaluates dependency statuses.
```bash
python -m src.cli.main delete [TASK_ID]
```

## 3. Running the Test Suite
Ensure that the `src` directory is in your Python path by running tests from the project root.

### Run All Tests
```bash
python -m pytest
```

### Run Tests for Specific Components
- **Core Engine**: `python -m pytest tests/core/`
- **AI Plugins**: `python -m pytest tests/plugins/`

## 4. Troubleshooting
- **ModuleNotFoundError**: Ensure you are running commands from the root directory of the project. Use `python -m src.cli.main` rather than running the script directly.
- **JSON Corruption**: If the `tasks.json` file is manually edited and becomes invalid, delete it or restore from a backup. The system uses atomic writes to prevent this automatically during normal operation.
