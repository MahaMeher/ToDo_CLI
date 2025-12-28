"""
Custom exceptions for task operations in the Todo In-Memory Python Console Application.

This module defines custom exception classes for handling task-related errors.
"""


class TaskError(Exception):
    """Base exception class for task-related errors."""
    pass


class TaskNotFoundError(TaskError):
    """Raised when a task with a specified ID is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class TaskValidationError(TaskError):
    """Raised when a task fails validation."""
    def __init__(self, message: str):
        super().__init__(message)


class TaskTitleError(TaskValidationError):
    """Raised when a task title fails validation."""
    def __init__(self, message: str):
        super().__init__(f"Task title error: {message}")


class TaskDescriptionError(TaskValidationError):
    """Raised when a task description fails validation."""
    def __init__(self, message: str):
        super().__init__(f"Task description error: {message}")


class TaskStatusError(TaskValidationError):
    """Raised when a task status fails validation."""
    def __init__(self, message: str):
        super().__init__(f"Task status error: {message}")


class DuplicateTaskIdError(TaskError):
    """Raised when attempting to create a task with a duplicate ID."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} already exists")