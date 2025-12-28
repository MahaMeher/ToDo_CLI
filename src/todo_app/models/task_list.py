"""
TaskList collection for the Todo In-Memory Python Console Application.

This module defines the TaskList collection that stores Task objects in memory
and provides operations for managing tasks.
"""
from typing import Dict, List, Optional
from .task import Task
from .exceptions import TaskNotFoundError, TaskValidationError


class TaskList:
    """
    Collection of Task entities stored in memory.

    Attributes:
        tasks (list): List of Task objects
        next_id (int): Counter for generating next unique ID, starts at 1
        _id_map (dict): Dictionary mapping ID to Task object for O(1) lookup by ID
    """

    def __init__(self):
        """Initialize an empty TaskList with starting ID counter."""
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self._id_map: Dict[int, Task] = {}

    def add_task(self, title: str, description: str = "", status: str = "Incomplete") -> Task:
        """
        Add a new task with unique ID and add to collection.

        Args:
            title (str): The task title (required)
            description (str): The task description (optional)
            status (str): The task status (optional, defaults to "Incomplete")

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            ValueError: If title validation fails
        """
        # Create task with next available ID
        task = Task(id=self.next_id, title=title, description=description, status=status)

        # Add to collections
        self.tasks.append(task)
        self._id_map[task.id] = task

        # Increment ID counter for next task
        self.next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get task by ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task with the specified ID, or None if not found
        """
        return self._id_map.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List[Task]: All tasks in the collection
        """
        return self.tasks.copy()  # Return a copy to prevent external modification

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update existing task fields.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        # Update fields if provided
        if title is not None:
            task.update_title(title)
        if description is not None:
            task.update_description(description)

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task from collection.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if deletion successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        # Remove from both collections
        self.tasks.remove(task)
        del self._id_map[task_id]

        return True

    def update_task_status(self, task_id: int, status: str) -> bool:
        """
        Update status of specified task.

        Args:
            task_id (int): The ID of the task to update
            status (str): The new status ("Complete" or "Incomplete")

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        if status == "Complete":
            task.mark_complete()
        elif status == "Incomplete":
            task.mark_incomplete()
        else:
            raise ValueError(f"Status must be 'Complete' or 'Incomplete', got '{status}'")

        return True

    def get_next_id(self) -> int:
        """
        Get the next available ID without incrementing.

        Returns:
            int: The next available ID
        """
        return self.next_id

    def __len__(self) -> int:
        """Return the number of tasks in the collection."""
        return len(self.tasks)

    def __iter__(self):
        """Allow iteration over tasks."""
        return iter(self.tasks)