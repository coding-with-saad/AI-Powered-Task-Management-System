We implemented a modular, plugin-based Task Management System in Python featuring automated dependency tracking and atomic JSON storage fordata integrity.
An AI-driven prioritizer intelligently scores tasks based on deadlines, keywords, and impact, all accessible through a professional color-coded CLI interface.


✦ I'll provide you with a step-by-step guide to explore the AI Task Manager. You can copy and paste these commands into your terminal one by
  one.

  1. List All Tasks
  See the tasks I created during the final verification.
   1 python -m src.cli.main list

  2. Add a New Task
  Create a task to see how the system handles it.

   1 python -m src.cli.main add "Finalize Portfolio" --desc "A high-level project goal"

  3. Add a Task with Dependencies
  Create a task that depends on the one you just created. This task will be automatically marked as BLOCKED.

   1 python -m src.cli.main add "Go Live" --dep [PASTE_ID_FROM_PREVIOUS_STEP]
  (Replace [PASTE_ID_FROM_PREVIOUS_STEP] with the ID returned in step 2)

  4. Run AI Prioritization
  Let the system calculate priority scores based on keywords and dependencies.
   1 python -m src.cli.main prioritize

  5. Mark a Task as Completed
  Complete the main task to see how it unblocks the dependent task.

   1 python -m src.cli.main complete [PASTE_ID_FROM_PREVIOUS_STEP]

  6. Run the Test Suite
  Verify that all core logic and plugins are functioning correctly.

   1 python -m pytest

  Enjoy exploring your new AI-powered Task Management System!