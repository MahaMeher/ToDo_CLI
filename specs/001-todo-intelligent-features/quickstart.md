# Quickstart: todo-intelligent-features

**Feature Spec**: `specs/001-todo-intelligent-features/spec.md`
**Status**: Complete
**Created**: 2025-12-31

## Getting Started

### Prerequisites
- Python 3.13+
- UV environment (optional but recommended)

### Setup
1. Ensure you have the base todo application installed and working
2. The intelligent features are already integrated into the main application
3. No additional dependencies required

### Running the Application
```bash
python src/todo_app/main.py
```

## Key Features

### 1. Recurring Tasks
- Create tasks that repeat daily, weekly, or at custom intervals
- When a recurring task is marked complete, a new instance is automatically created
- Access via CLI option 14: Set task recurrence

### 2. Due Dates
- Assign due dates to tasks for deadline tracking
- Tasks display due date information in the task list
- Access via CLI option 13: Set task due date

### 3. Overdue Task Identification
- System automatically identifies tasks past their due date
- Overdue status displayed in task list
- Access via CLI option 15: View overdue tasks

### 4. Due Soon Reminders
- System identifies tasks approaching their due date
- Configurable time window for "due soon" notifications

## API Reference

### TaskService Methods
- `create_recurring_task()` - Create a new recurring task
- `process_completed_recurring_task()` - Process completion and create next occurrence
- `get_overdue_tasks()` - Get all tasks past their due date
- `get_due_soon_tasks()` - Get tasks approaching due date
- `update_task_due_date()` - Update a task's due date

### CLI Commands
- Option 13: Set task due date
- Option 14: Set task recurrence
- Option 15: View overdue tasks

## Testing
Run the test suite to verify all features work correctly:
```bash
python test_intelligent_features.py
python test_intelligent_features_integration.py
```

## Integration with Existing Features
All intelligent features maintain full compatibility with:
- Basic task operations (add, view, update, delete, mark complete)
- Organization features (priorities, tags, search, filter, sort)
- No breaking changes to existing functionality