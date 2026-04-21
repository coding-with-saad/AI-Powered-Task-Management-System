# Project Summary: AI-Powered Task Management System

This project is a production-ready, extensible CLI-based Task Management System built in Python. It features a modular architecture with an AI-driven plugin system for smart task prioritization.

## 1. System Architecture

The system follows a **Modular Plugin-based Architecture**, separating the core business logic from data storage, user interface, and AI enhancements.

### Core Components
- **`src/core/task.py`**: Defines the `Task` data model using Python dataclasses. It includes automated timestamping and robust dictionary serialization for data persistence.
- **`src/core/manager.py`**: The `TaskManager` coordinates all operations. It handles CRUD logic and complex **dependency tracking**, ensuring that tasks are automatically marked as `BLOCKED` if their dependencies aren't `COMPLETED`. It uses a transitive dependency loop to propagate status changes correctly.
- **`src/core/storage.py`**: Implements `JSONStorage` with **atomic writes**. By writing to a `.tmp` file and then renaming it, the system ensures data integrity even if the process is interrupted.
- **`src/plugins/`**: A flexible extension system. Any new feature (e.g., AI analysis, backup tools) can be added by implementing the `BasePlugin` interface.
- **`src/plugins/ai_prioritizer.py`**: The first extension, an AI-driven plugin that calculates a "Priority Score" based on:
    - **Urgency Keywords**: Titles containing "CRITICAL", "ASAP", etc.
    - **Dependency Impact**: Tasks that unblock many other tasks receive higher priority.
    - **Deadline Proximity**: Tasks due sooner are automatically boosted.
- **`src/cli/main.py`**: A professional CLI interface with color-coded status output (Green for Completed, Red for Blocked, etc.).

## 2. Key Design Decisions & Trade-offs
- **Atomic Persistence**: Prioritized data safety by using the temporary-file-and-move pattern for JSON storage.
- **Automatic Status Management**: Minimized manual overhead by having the engine automatically manage `blocked` states.
- **Rule-based AI Foundation**: Used weighted scoring for the initial AI logic to ensure explainability and ease of debugging, while providing a clear path for future NLP integration.
- **JSON for Simplicity**: Chose JSON for storage to keep the system lightweight and human-readable, with a design that allows for an easy swap to SQLite if needed.

## 3. Development Process
The project was developed using a **Research -> Strategy -> Execution** lifecycle:
1. **Research & Design**: Fully mapped the requirements and designed the plugin-based architecture before writing code.
2. **TDD (Test-Driven Development)**: Followed a strict TDD workflow for every core component, ensuring 100% passing tests for the engine and plugins.
3. **Iterative Refinement**: Addressed feedback from code reviews, such as improving `updated_at` accuracy and handling transitive dependencies.
4. **Final Verification**: Confirmed the system's stability through both automated test suites and manual CLI verification.

## 4. Stability & Readiness
The system is fully verified with a comprehensive test suite (`pytest`) and is considered **production-ready** for personal and small-team task management.
