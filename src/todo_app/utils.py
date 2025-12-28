"""
Utility functions for the Todo In-Memory Python Console Application.

This module contains utility functions for consistent error messaging and other common operations.
"""


class ErrorMessage:
    """Utility class for consistent error messaging."""

    @staticmethod
    def invalid_task_id(task_id: int) -> str:
        """Generate error message for invalid task ID."""
        return f"Error: Task with ID {task_id} not found."

    @staticmethod
    def invalid_title_length(title: str, max_length: int = 100) -> str:
        """Generate error message for invalid title length."""
        return f"Error: Task title exceeds maximum length of {max_length} characters. Current length: {len(title)}"

    @staticmethod
    def invalid_description_length(description: str, max_length: int = 500) -> str:
        """Generate error message for invalid description length."""
        return f"Error: Task description exceeds maximum length of {max_length} characters. Current length: {len(description)}"

    @staticmethod
    def invalid_status(status: str) -> str:
        """Generate error message for invalid status."""
        return f"Error: Status must be 'Complete' or 'Incomplete', got '{status}'"

    @staticmethod
    def empty_title() -> str:
        """Generate error message for empty title."""
        return "Error: Task title cannot be empty or only whitespace."

    @staticmethod
    def invalid_numeric_input(input_str: str) -> str:
        """Generate error message for invalid numeric input."""
        return f"Error: '{input_str}' is not a valid number."

    @staticmethod
    def task_not_found(task_id: int) -> str:
        """Generate error message for task not found."""
        return f"Error: Task with ID {task_id} does not exist."


def format_task_display(task) -> str:
    """Format a task for display in the console."""
    status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
    return f"{task.id:<4} {status:<12} {task.title[:29]:<30} {task.description[:30]}"