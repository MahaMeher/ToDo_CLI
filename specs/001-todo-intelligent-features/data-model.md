# Data Model: todo-intelligent-features

**Feature Spec**: `specs/001-todo-intelligent-features/spec.md`
**Status**: Complete
**Created**: 2025-12-31

## Entity: Task (Extended)

### Attributes
- **id**: `int` (required) - Unique identifier for the task, auto-generated, positive integer
- **title**: `str` (required) - Short description of the task, max 100 characters
- **description**: `str` (optional) - Detailed information about the task, max 500 characters
- **status**: `str` (required) - Completion status, either "Complete" or "Incomplete", default "Incomplete"
- **priority**: `str` (optional) - Priority level, one of "high", "medium", "low"
- **tags**: `List[str]` (optional) - List of tags/categories for the task
- **due_date**: `str` (optional) - Due date in ISO format (YYYY-MM-DD)
- **is_recurring**: `bool` (optional) - Whether the task is recurring, default False
- **recurrence_config**: `RecurringTaskConfig` (optional) - Configuration for recurring tasks
- **original_task_id**: `int` (optional) - ID of the original task this is an instance of
- **reminder_time**: `int` (optional) - Minutes before due date to show reminder

### Validation Rules
- `id`: Must be a positive integer
- `title`: Required, non-empty, max 100 characters
- `description`: Max 500 characters
- `status`: Must be "Complete" or "Incomplete"
- `priority`: If provided, must be "high", "medium", or "low"
- `tags`: If provided, must be a list of non-empty strings
- `due_date`: If provided, must be in ISO format (YYYY-MM-DD)
- `is_recurring`: Must be a boolean
- `original_task_id`: If provided, must be a positive integer
- `reminder_time`: If provided, must be a non-negative integer

## Entity: RecurringTaskConfig

### Attributes
- **pattern_type**: `RecurrencePattern` (required) - Type of recurrence pattern (daily, weekly, custom)
- **interval_days**: `int` (optional) - Number of days between occurrences for custom patterns, default 1
- **end_date**: `datetime` (optional) - Optional end date for the recurrence
- **week_days**: `List[int]` (optional) - List of weekdays (0=Monday, 6=Sunday) for weekly patterns
- **enabled**: `bool` (optional) - Whether the recurrence is currently enabled, default True

### Validation Rules
- `pattern_type`: Must be a valid RecurrencePattern enum value
- `interval_days`: Must be a positive integer
- `week_days`: If provided, all values must be between 0 and 6
- `end_date`: If provided, cannot be in the past
- `enabled`: Must be a boolean

## State Transitions

### Task Status Transitions
- `"Incomplete"` → `"Complete"`: When user marks task as complete
- `"Complete"` → `"Incomplete"`: When user marks task as incomplete

### Task Recurrence Transitions
- Non-recurring task → Recurring task: When user sets recurrence configuration
- Recurring task completion → New occurrence: When recurring task is completed and next occurrence is created

## Relationships

### Task to RecurringTaskConfig
- One-to-one relationship: Each recurring task has one recurrence configuration
- Optional: Non-recurring tasks do not have a recurrence configuration

### Task to Original Task
- Many-to-one relationship: Multiple task instances can reference the same original task
- Optional: Original tasks do not reference other tasks