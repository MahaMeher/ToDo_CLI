# Todo In-Memory Python Console Application

A console-based todo application that stores tasks in memory with full CRUD functionality (Add, View, Update, Delete) plus status management (Mark Complete/Incomplete). The application follows Python 3.13+ standards with clean architecture and proper error handling.

## Setup Instructions

1. Ensure you have Python 3.13+ installed on your system
2. Clone or download this repository
3. Navigate to the project root directory
4. Install dependencies (if any) using your preferred method

## Usage

To run the application:

```bash
python -m src.todo_app.main
```

Using UV (recommended):

```bash
uv run python -m src.todo_app.main
```

Or if installed as a package:

```bash
todo-app
```

## Usage Examples

### Adding a Task
1. Run the application
2. Select option "1. Add new task"
3. Enter a title (required, max 100 characters)
4. Enter a description (optional, max 500 characters)
5. The task will be added with a unique ID

### Viewing All Tasks
1. Select option "2. View all tasks"
2. All tasks will be displayed with ID, status, title, and description

### Updating a Task
1. Select option "3. Update task"
2. Enter the task ID to update
3. Optionally enter a new title and/or description
4. The task will be updated with the new information

### Deleting a Task
1. Select option "4. Delete task"
2. Enter the task ID to delete
3. Confirm the deletion when prompted
4. The task will be removed from the list

### Marking Task Complete/Incomplete
1. Select option "5. Mark task as complete" or "6. Mark task as incomplete"
2. Enter the task ID to update
3. The task status will be updated accordingly

## Features

- Add new todo tasks with title and description
- View all existing tasks with their status
- Update existing task information
- Delete tasks by ID
- Mark tasks as Complete/Incomplete
- In-memory storage (data is lost when application exits)
- Graceful error handling for invalid inputs
- Menu-driven console interface
- Input validation for all user inputs
- Confirmation prompts for destructive operations

## Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task data model and TaskList collection
│   │   └── exceptions.py    # Custom exceptions for task operations
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic for task operations
│   ├── cli/
│   │   ├── __init__.py
│   │   └── interface.py     # Console interface and command handlers
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

## Development

To run tests:

```bash
pytest tests/
```

To run specific test suites:

```bash
pytest tests/unit/      # Unit tests
pytest tests/integration/  # Integration tests
```