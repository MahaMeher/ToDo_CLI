# API Contract: Task Service for Intelligent Features

**Feature Spec**: `specs/001-todo-intelligent-features/spec.md`
**Status**: Complete
**Created**: 2025-12-31

## Overview

This document defines the API contracts for the intelligent features of the task service, including recurring tasks, due dates, and overdue functionality.

## Service: TaskService

### Methods

#### `create_recurring_task(title: str, description: str = "", status: str = "Incomplete", priority: str = None, tags: List[str] = None, due_date: str = None, recurrence_config: RecurringTaskConfig = None, reminder_time: int = None) -> Task`

**Purpose**: Create a new recurring task with specified configuration.

**Parameters**:
- `title`: Task title (required, max 100 chars)
- `description`: Task description (optional, max 500 chars)
- `status`: Initial status ("Complete" or "Incomplete", default "Incomplete")
- `priority`: Priority level ("high", "medium", "low", optional)
- `tags`: List of tags for categorization (optional)
- `due_date`: Due date in ISO format (YYYY-MM-DD, optional)
- `recurrence_config`: Configuration for recurrence pattern (required)
- `reminder_time`: Minutes before due date for reminders (optional)

**Returns**: Task object with assigned ID and recurrence configuration

**Errors**:
- `TaskValidationError` if validation fails
- `ValueError` if recurrence_config is None

#### `process_completed_recurring_task(task_id: int) -> Optional[Task]`

**Purpose**: Process a completed recurring task and create the next occurrence if applicable.

**Parameters**:
- `task_id`: ID of the completed recurring task (required)

**Returns**: New Task instance if created, None otherwise

**Errors**:
- `TaskNotFoundError` if task_id does not exist

#### `get_overdue_tasks() -> List[Task]`

**Purpose**: Retrieve all tasks that are past their due date.

**Parameters**: None

**Returns**: List of overdue Task objects

#### `get_due_soon_tasks(minutes_before: int = 30) -> List[Task]`

**Purpose**: Retrieve tasks that are approaching their due date within the specified time window.

**Parameters**:
- `minutes_before`: Time window in minutes (default 30)

**Returns**: List of Task objects due soon

#### `update_task_due_date(task_id: int, due_date: str) -> bool`

**Purpose**: Update the due date of an existing task.

**Parameters**:
- `task_id`: ID of the task to update (required)
- `due_date`: New due date in ISO format (YYYY-MM-DD, required)

**Returns**: True if successful, False if task not found

**Errors**:
- `TaskValidationError` if due_date format is invalid
- `TaskNotFoundError` if task_id does not exist

## Service: TaskList

### Methods

#### `create_recurring_task(title: str, description: str = "", status: str = "Incomplete", priority: str = None, tags: List[str] = None, due_date: str = None, recurrence_config: RecurringTaskConfig = None, reminder_time: int = None) -> Task`

**Purpose**: Create a new recurring task in the task list.

**Parameters**: Same as TaskService.create_recurring_task

**Returns**: Task object with recurrence configuration

#### `process_completed_recurring_task(task_id: int) -> Optional[Task]`

**Purpose**: Process completion of a recurring task and create next occurrence.

**Parameters**: task_id of the completed task

**Returns**: New Task instance if created, None otherwise

#### `get_overdue_tasks() -> List[Task]`

**Purpose**: Get all overdue tasks from the list.

**Returns**: List of overdue Task objects

#### `get_due_soon_tasks(minutes_before: int = 30) -> List[Task]`

**Purpose**: Get tasks due soon from the list.

**Parameters**: minutes_before time window

**Returns**: List of Task objects due soon

## Data Models

### Task (Extended)

**Attributes**:
- `id`: int (required) - Unique identifier
- `title`: str (required) - Task title
- `description`: str (optional) - Task description
- `status`: str (required) - "Complete" or "Incomplete"
- `priority`: str (optional) - "high", "medium", or "low"
- `tags`: List[str] (optional) - List of tags
- `due_date`: str (optional) - Due date in ISO format
- `is_recurring`: bool (optional) - Whether task is recurring
- `recurrence_config`: RecurringTaskConfig (optional) - Recurrence configuration
- `original_task_id`: int (optional) - ID of original task if this is an instance
- `reminder_time`: int (optional) - Minutes before due date for reminders

### RecurringTaskConfig

**Attributes**:
- `pattern_type`: RecurrencePattern (required) - Daily, weekly, or custom
- `interval_days`: int (optional) - Days between occurrences
- `end_date`: datetime (optional) - End date for recurrence
- `week_days`: List[int] (optional) - Days of week for weekly patterns
- `enabled`: bool (optional) - Whether recurrence is active

## Validation Rules

### Task Validation
- `id`: Must be positive integer
- `title`: Required, non-empty, max 100 chars
- `description`: Max 500 chars
- `status`: Must be "Complete" or "Incomplete"
- `priority`: If present, must be "high", "medium", or "low"
- `due_date`: If present, must be in ISO format
- `is_recurring`: Must be boolean
- `original_task_id`: If present, must be positive integer
- `reminder_time`: If present, must be non-negative integer

### RecurringTaskConfig Validation
- `pattern_type`: Must be valid RecurrencePattern enum
- `interval_days`: Must be positive integer
- `week_days`: If present, all values 0-6
- `end_date`: If present, not in past
- `enabled`: Must be boolean