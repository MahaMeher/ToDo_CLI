"""
TaskService for the Todo In-Memory Python Console Application.

This module provides business logic for task operations.
"""
from typing import List, Optional
from src.todo_app.models.task_list import TaskList
from src.todo_app.models.task import Task
from src.todo_app.models.exceptions import TaskNotFoundError, TaskValidationError


class TaskService:
    """
    Business logic for task operations.

    This service layer manages task operations and provides an interface
    between the CLI layer and the model layer.
    """

    def __init__(self):
        """Initialize the TaskService with a TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = "", status: str = "Incomplete") -> Task:
        """
        Add a new task with validation.

        Args:
            title (str): The task title (required)
            description (str): The task description (optional)
            status (str): The task status (optional, defaults to "Incomplete")

        Returns:
            Task: The newly created task

        Raises:
            TaskValidationError: If the task data is invalid
        """
        try:
            # Validate inputs
            Task.validate_title(title)
            Task.validate_description(description)
            Task.validate_status(status)
        except ValueError as e:
            raise TaskValidationError(str(e))

        # Add to task list
        return self.task_list.add_task(title, description, status)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task with the specified ID, or None if not found
        """
        return self.task_list.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: All tasks in the system
        """
        return self.task_list.get_all_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskNotFoundError: If the task with the specified ID is not found
        """
        try:
            if title is not None:
                Task.validate_title(title)
            if description is not None:
                Task.validate_description(description)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if deletion successful, False if task not found

        Raises:
            TaskNotFoundError: If the task with the specified ID is not found
        """
        return self.task_list.delete_task(task_id)

    def update_task_status(self, task_id: int, status: str) -> bool:
        """
        Update the status of a task.

        Args:
            task_id (int): The ID of the task to update
            status (str): The new status ("Complete" or "Incomplete")

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskValidationError: If the status is invalid
        """
        try:
            Task.validate_status(status)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.update_task_status(task_id, status)

    def get_next_task_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        return self.task_list.get_next_id()

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            int: The number of tasks in the system
        """
        return len(self.task_list)