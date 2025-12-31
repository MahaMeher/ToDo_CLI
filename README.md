# Todo In-Memory Python Console Application

A console-based todo application that stores tasks in memory with full CRUD functionality (Add, View, Update, Delete) plus status management (Mark Complete/Incomplete). The application follows Python 3.13+ standards with clean architecture and proper error handling, featuring intelligent scheduling capabilities including recurring tasks and due date management.

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
2. All tasks will be displayed with ID, status, title, description, priority, tags, due date, and recurrence information

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

### Setting Task Priority
1. Select option "7. Set task priority"
2. Enter the task ID to update
3. Choose priority level (high, medium, low)
4. The task priority will be updated

### Adding/Removing Task Tags
1. Select option "8. Add tags to task" or "9. Remove tags from task"
2. Enter the task ID to update
3. Enter tags separated by commas
4. The task tags will be updated accordingly

### Searching Tasks
1. Select option "10. Search tasks"
2. Enter a keyword to search in titles and descriptions
3. Matching tasks will be displayed

### Filtering Tasks
1. Select option "11. Filter tasks"
2. Choose filter criteria (status, priority, tags, due date)
3. Filtered tasks will be displayed

### Sorting Tasks
1. Select option "12. Sort tasks"
2. Choose sort criteria (ID, title, status, priority, due date)
3. Choose sort order (ascending/descending)
4. Sorted tasks will be displayed

### Setting Due Dates
1. Select option "13. Set task due date"
2. Enter the task ID to update
3. Enter due date in YYYY-MM-DD format
4. The task due date will be updated

### Viewing Overdue Tasks
1. Select option "14. View overdue tasks"
2. All overdue tasks will be displayed
3. Overdue tasks are highlighted in the main task list

### Setting Recurring Tasks
1. Select option "15. Set task recurrence"
2. Enter the task ID to update
3. Choose recurrence pattern (daily, weekly, custom)
4. The task will be configured as recurring

### Setting Reminders
1. Select option "16. Set task reminder"
2. Enter the task ID to update
3. Enter minutes before due date for reminder
4. The task reminder will be configured

## Features

### Basic Features
- Add new todo tasks with title and description
- View all existing tasks with their status
- Update existing task information
- Delete tasks by ID
- Mark tasks as Complete/Incomplete

### Intermediate Features
- Task priorities (high, medium, low)
- Task tags for categorization
- Search functionality by keyword
- Filter tasks by status, priority, tags, or due date
- Sort tasks by various criteria
- Comprehensive input validation

### Intelligent Features
- Recurring tasks with daily, weekly, and custom intervals
- Due date assignment and management
- Automatic overdue task identification
- Reminder notifications for upcoming tasks
- Automatic task rescheduling when recurring tasks are completed

### Additional Features
- In-memory storage (data is lost when application exits)
- Graceful error handling for invalid inputs
- Menu-driven console interface
- Input validation for all user inputs
- Confirmation prompts for destructive operations
- Visual indicators for task status and priority
- Comprehensive logging and error reporting

## Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task data model and TaskList collection
│   │   ├── recurring_task.py # Recurring task configuration model
│   │   ├── exceptions.py    # Custom exceptions for task operations
│   │   └── task_list.py     # Task collection management
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic for task operations
│   ├── cli/
│   │   ├── __init__.py
│   │   └── interface.py     # Console interface and command handlers
│   ├── utils/
│   │   ├── __init__.py
│   │   └── datetime_utils.py # Date and time utility functions
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/
│   │   └── test_organization_features.py # Tests for organization features
│   ├── integration/
│   ├── test_intelligent_features.py      # Unit tests for intelligent features
│   └── test_intelligent_features_integration.py # Integration tests for intelligent features
├── specs/
│   ├── 001-todo-intelligent-features/    # Specification for intelligent features
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── data-model.md
│   │   ├── research.md
│   │   ├── quickstart.md
│   │   ├── checklists/
│   │   │   └── requirements-checklist.md
│   │   └── contracts/
│   │       └── task-api-contract.md
│   └── 001-todo-organization/            # Specification for organization features
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md
│       ├── checklists/
│       │   └── requirements.md
│       └── contracts/
│           └── task-organization-api.md
├── history/
│   └── prompts/                          # AI prompt history records
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
pytest test_intelligent_features.py  # Intelligent features tests
pytest test_intelligent_features_integration.py  # Intelligent features integration tests
```