"""
TaskList collection for the Todo In-Memory Python Console Application.

This module defines the TaskList collection that stores Task objects in memory
and provides operations for managing tasks.
"""
from typing import Dict, List, Optional
from datetime import datetime
from .task import Task
from .recurring_task import RecurringTaskConfig
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

    def add_task(self, title: str, description: str = "", status: str = "Incomplete", priority: str = None, tags: List[str] = None, due_date: str = None, is_recurring: bool = False, recurrence_config: RecurringTaskConfig = None, original_task_id: int = None, reminder_time: int = None) -> Task:
        """
        Add a new task with unique ID and add to collection.

        Args:
            title (str): The task title (required)
            description (str): The task description (optional)
            status (str): The task status (optional, defaults to "Incomplete")
            priority (str): The task priority (optional, high/medium/low)
            tags (List[str]): List of tags for the task (optional)
            due_date (str): Due date in ISO format (optional)
            is_recurring (bool): Whether the task is recurring (optional)
            recurrence_config (RecurringTaskConfig): Configuration for recurring tasks (optional)
            original_task_id (int): ID of the original task this is an instance of (optional)
            reminder_time (int): Minutes before due date to show reminder (optional)

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            ValueError: If title validation fails
        """
        # Create task with next available ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            tags=tags if tags is not None else [],
            due_date=due_date,
            is_recurring=is_recurring,
            recurrence_config=recurrence_config,
            original_task_id=original_task_id,
            reminder_time=reminder_time
        )

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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[str] = None) -> bool:
        """
        Update existing task fields.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            priority (str, optional): New priority for the task
            tags (List[str], optional): New list of tags for the task
            due_date (str, optional): New due date for the task

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
        if priority is not None:
            task.update_priority(priority)
        if tags is not None:
            task.update_tags(tags)
        if due_date is not None:
            task.update_due_date(due_date)

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

    def update_task_priority(self, task_id: int, priority: str) -> bool:
        """
        Update priority of specified task.

        Args:
            task_id (int): The ID of the task to update
            priority (str): The new priority ("high", "medium", or "low")

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.update_priority(priority)
        return True

    def update_task_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Update tags of specified task.

        Args:
            task_id (int): The ID of the task to update
            tags (List[str]): The new list of tags

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.update_tags(tags)
        return True

    def add_task_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Add tags to specified task.

        Args:
            task_id (int): The ID of the task to update
            tags (List[str]): List of tags to add

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.add_tags(tags)
        return True

    def remove_task_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Remove tags from specified task.

        Args:
            task_id (int): The ID of the task to update
            tags (List[str]): List of tags to remove

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.remove_tags(tags)
        return True

    def update_task_due_date(self, task_id: int, due_date: str) -> bool:
        """
        Update due date of specified task.

        Args:
            task_id (int): The ID of the task to update
            due_date (str): The new due date in ISO format (YYYY-MM-DD)

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.update_due_date(due_date)
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

    def create_recurring_task(self, title: str, description: str = "", status: str = "Incomplete", priority: str = None, tags: List[str] = None, due_date: str = None, recurrence_config: RecurringTaskConfig = None, reminder_time: int = None) -> Task:
        """
        Create a new recurring task.

        Args:
            title (str): The task title (required)
            description (str): The task description (optional)
            status (str): The task status (optional, defaults to "Incomplete")
            priority (str): The task priority (optional, high/medium/low)
            tags (List[str]): List of tags for the task (optional)
            due_date (str): Due date in ISO format (optional)
            recurrence_config (RecurringTaskConfig): Configuration for recurring tasks (required)
            reminder_time (int): Minutes before due date to show reminder (optional)

        Returns:
            Task: The newly created recurring task with assigned ID
        """
        if recurrence_config is None:
            raise ValueError("Recurrence configuration is required for recurring tasks")

        return self.add_task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            tags=tags,
            due_date=due_date,
            is_recurring=True,
            recurrence_config=recurrence_config,
            original_task_id=None,  # This is the original task
            reminder_time=reminder_time
        )

    def process_completed_recurring_task(self, task_id: int) -> Optional[Task]:
        """
        Process a completed recurring task and create the next occurrence if applicable.

        Args:
            task_id (int): The ID of the completed recurring task

        Returns:
            Task: The new task instance if created, None otherwise
        """
        completed_task = self.get_task(task_id)
        if completed_task is None:
            raise TaskNotFoundError(task_id)

        if not completed_task.is_recurring or completed_task.recurrence_config is None:
            return None

        # Check if we should create a new occurrence
        if completed_task.recurrence_config.should_create_next_occurrence(datetime.now()):
            # Calculate next occurrence date
            if completed_task.due_date:
                try:
                    current_due_date = datetime.strptime(completed_task.due_date, "%Y-%m-%d")
                    next_due_date = completed_task.recurrence_config.get_next_occurrence_date(current_due_date)
                    next_due_date_str = next_due_date.strftime("%Y-%m-%d")
                except ValueError:
                    next_due_date_str = completed_task.due_date  # Keep the same date if parsing fails
            else:
                next_due_date_str = None

            # Create a new task instance based on the original
            new_task = self.add_task(
                title=completed_task.title,
                description=completed_task.description,
                status="Incomplete",  # New tasks start as incomplete
                priority=completed_task.priority,
                tags=completed_task.tags,
                due_date=next_due_date_str,
                is_recurring=completed_task.is_recurring,
                recurrence_config=completed_task.recurrence_config,
                original_task_id=completed_task.original_task_id or completed_task.id,  # Use original ID if available, otherwise this task is the original
                reminder_time=completed_task.reminder_time
            )

            return new_task

        return None

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are overdue.

        Returns:
            List[Task]: List of overdue tasks
        """
        overdue_tasks = []
        for task in self.tasks:
            if task.is_overdue():
                overdue_tasks.append(task)
        return overdue_tasks

    def get_due_soon_tasks(self, minutes_before: int = 30) -> List[Task]:
        """
        Get all tasks that are due soon.

        Args:
            minutes_before (int): Number of minutes before due time to consider "due soon"

        Returns:
            List[Task]: List of tasks due soon
        """
        from src.todo_app.utils.datetime_utils import is_due_soon
        due_soon_tasks = []
        for task in self.tasks:
            if task.due_date and is_due_soon(task.due_date, minutes_before):
                due_soon_tasks.append(task)
        return due_soon_tasks

    def update_task_recurrence(self, task_id: int, recurrence_config) -> bool:
        """
        Update an existing task to be recurring with the specified configuration.

        Args:
            task_id (int): The ID of the task to update
            recurrence_config: The recurrence configuration to apply

        Returns:
            bool: True if update successful, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        # Update task properties to make it recurring
        task.is_recurring = True
        task.recurrence_config = recurrence_config

        return True

    def __iter__(self):
        """Allow iteration over tasks."""
        return iter(self.tasks)