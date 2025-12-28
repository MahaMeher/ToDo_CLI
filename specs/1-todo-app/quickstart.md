# Quickstart Guide: Todo In-Memory Python Console Application

## Prerequisites

- Python 3.13+ installed
- UV package manager installed (for dependency management)

## Setup

1. Clone or create the project directory
2. Navigate to the project root directory
3. Install dependencies using UV:
   ```bash
   uv sync
   ```
   Or if using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── interface.py
│   └── main.py
├── tests/
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

## Running the Application

1. Navigate to the project root directory
2. Run the application:
   ```bash
   python -m src.todo_app.main
   ```
   Or if the package is properly configured:
   ```bash
   python src/todo_app/main.py
   ```

## Basic Usage

1. The application starts with a menu showing available options
2. Enter the number corresponding to your desired action
3. Follow the prompts to provide required information

### Available Actions:
- Add Task: Creates a new task with title and description
- View Tasks: Displays all tasks with their status
- Update Task: Modifies an existing task's title or description
- Delete Task: Removes a task from the list
- Mark Complete/Incomplete: Changes the status of a task

## Running Tests

Execute the test suite using pytest:
```bash
pytest tests/
```

Or for specific test types:
```bash
pytest tests/unit/      # Unit tests
pytest tests/integration/  # Integration tests
```

## Development Workflow

1. Make changes to the appropriate module (models, services, or cli)
2. Run tests to ensure functionality works as expected
3. Update documentation if necessary
4. Commit changes with descriptive commit messages