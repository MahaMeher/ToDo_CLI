"""
TaskService for the Todo In-Memory Python Console Application.

This module provides business logic for task operations.
"""
from typing import List, Optional
from datetime import datetime
from src.todo_app.models.task_list import TaskList
from src.todo_app.models.task import Task
from src.todo_app.models.recurring_task import RecurringTaskConfig
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

    def add_task(self, title: str, description: str = "", status: str = "Incomplete", priority: str = None, tags: List[str] = None, due_date: str = None, is_recurring: bool = False, recurrence_config: RecurringTaskConfig = None, original_task_id: int = None, reminder_time: int = None) -> Task:
        """
        Add a new task with validation.

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
            Task: The newly created task

        Raises:
            TaskValidationError: If the task data is invalid
        """
        try:
            # Validate inputs
            Task.validate_title(title)
            Task.validate_description(description)
            Task.validate_status(status)

            if priority is not None:
                Task.validate_priority(priority)

            if tags is not None:
                Task.validate_tags(tags)

            if due_date is not None:
                Task.validate_due_date(due_date)

            if reminder_time is not None and reminder_time < 0:
                raise ValueError("Reminder time must be a non-negative integer")
        except ValueError as e:
            raise TaskValidationError(str(e))

        # Add to task list
        return self.task_list.add_task(title, description, status, priority, tags, due_date, is_recurring, recurrence_config, original_task_id, reminder_time)

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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task
            priority (str, optional): New priority for the task
            tags (List[str], optional): New list of tags for the task
            due_date (str, optional): New due date for the task

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
            if priority is not None:
                Task.validate_priority(priority)
            if tags is not None:
                Task.validate_tags(tags)
            if due_date is not None:
                Task.validate_due_date(due_date)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.update_task(task_id, title, description, priority, tags, due_date)

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

    def set_task_priority(self, task_id: int, priority: str) -> bool:
        """
        Set the priority of a task.

        Args:
            task_id (int): The ID of the task to update
            priority (str): The new priority ("high", "medium", or "low")

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskValidationError: If the priority is invalid
            TaskNotFoundError: If the task with the specified ID is not found
        """
        try:
            Task.validate_priority(priority)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.update_task_priority(task_id, priority)

    def get_task_priority(self, task_id: int) -> Optional[str]:
        """
        Get the priority of a task.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            str: The priority of the task, or None if task not found
        """
        task = self.task_list.get_task(task_id)
        if task is None:
            return None
        return task.priority

    def add_task_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Add tags to a task.

        Args:
            task_id (int): The ID of the task to update
            tags (List[str]): List of tags to add

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskValidationError: If the tags are invalid
            TaskNotFoundError: If the task with the specified ID is not found
        """
        try:
            Task.validate_tags(tags)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.add_task_tags(task_id, tags)

    def remove_task_tags(self, task_id: int, tags: List[str]) -> bool:
        """
        Remove tags from a task.

        Args:
            task_id (int): The ID of the task to update
            tags (List[str]): List of tags to remove

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskNotFoundError: If the task with the specified ID is not found
        """
        return self.task_list.remove_task_tags(task_id, tags)

    def get_task_tags(self, task_id: int) -> Optional[List[str]]:
        """
        Get the tags of a task.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            List[str]: The tags of the task, or None if task not found
        """
        task = self.task_list.get_task(task_id)
        if task is None:
            return None
        return task.tags if task.tags is not None else []

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            query (str): The search keyword

        Returns:
            List[Task]: List of tasks that match the search query
        """
        query_lower = query.lower()
        matching_tasks = []

        for task in self.task_list:
            # Check if query matches in title or description (case-insensitive)
            if (query_lower in task.title.lower() or
                (task.description and query_lower in task.description.lower())):
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                     tags: Optional[List[str]] = None, due_date: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by various criteria.

        Args:
            status (str, optional): Filter by status ("Complete" or "Incomplete")
            priority (str, optional): Filter by priority ("high", "medium", "low")
            tags (List[str], optional): Filter by tags (tasks must contain all specified tags)
            due_date (str, optional): Filter by due date (exact match)

        Returns:
            List[Task]: List of tasks that match the filter criteria
        """
        filtered_tasks = []

        for task in self.task_list:
            # Check status filter
            if status is not None and task.status != status:
                continue

            # Check priority filter
            if priority is not None and task.priority != priority:
                continue

            # Check tags filter
            if tags is not None and task.tags is not None:
                # Check if task has all the required tags
                missing_tags = [tag for tag in tags if tag not in task.tags]
                if missing_tags:
                    continue

            # Check due date filter
            if due_date is not None and task.due_date != due_date:
                continue

            filtered_tasks.append(task)

        return filtered_tasks

    def sort_tasks(self, by: str = "id", order: str = "asc") -> List[Task]:
        """
        Sort tasks by various criteria.

        Args:
            by (str): Field to sort by ("id", "title", "status", "priority", "due_date")
            order (str): Sort order ("asc" for ascending, "desc" for descending)

        Returns:
            List[Task]: List of tasks sorted according to the specified criteria
        """
        def sort_key(task):
            if by == "priority":
                # Define priority order: high > medium > low
                priority_order = {"high": 0, "medium": 1, "low": 2}
                return priority_order.get(task.priority, 3)  # None gets lowest priority
            elif by == "due_date":
                # For due_date, None should come last, then sort chronologically
                if task.due_date is None:
                    return "9999-12-31"  # Far future date for None values
                return task.due_date
            elif by == "title":
                return task.title.lower()  # Case-insensitive sort
            elif by == "status":
                # Complete tasks last
                return 1 if task.status == "Complete" else 0
            else:  # Default to id
                return task.id

        reverse = (order == "desc")
        return sorted(self.task_list.get_all_tasks(), key=sort_key, reverse=reverse)

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
            Task: The newly created recurring task

        Raises:
            TaskValidationError: If the task data is invalid
        """
        try:
            # Validate inputs
            Task.validate_title(title)
            Task.validate_description(description)
            Task.validate_status(status)

            if priority is not None:
                Task.validate_priority(priority)

            if tags is not None:
                Task.validate_tags(tags)

            if due_date is not None:
                Task.validate_due_date(due_date)

            if recurrence_config is None:
                raise ValueError("Recurrence configuration is required for recurring tasks")

            if reminder_time is not None and reminder_time < 0:
                raise ValueError("Reminder time must be a non-negative integer")
        except ValueError as e:
            raise TaskValidationError(str(e))

        # Create recurring task
        return self.task_list.create_recurring_task(
            title, description, status, priority, tags, due_date, recurrence_config, reminder_time
        )

    def process_completed_recurring_task(self, task_id: int) -> Optional[Task]:
        """
        Process a completed recurring task and create the next occurrence if applicable.

        Args:
            task_id (int): The ID of the completed recurring task

        Returns:
            Task: The new task instance if created, None otherwise

        Raises:
            TaskNotFoundError: If the task with the specified ID is not found
        """
        return self.task_list.process_completed_recurring_task(task_id)

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are overdue.

        Returns:
            List[Task]: List of overdue tasks
        """
        return self.task_list.get_overdue_tasks()

    def get_due_soon_tasks(self, minutes_before: int = 30) -> List[Task]:
        """
        Get all tasks that are due soon.

        Args:
            minutes_before (int): Number of minutes before due time to consider "due soon"

        Returns:
            List[Task]: List of tasks due soon
        """
        return self.task_list.get_due_soon_tasks(minutes_before)

    def update_task_due_date(self, task_id: int, due_date: str) -> bool:
        """
        Update the due date of a task.

        Args:
            task_id (int): The ID of the task to update
            due_date (str): The new due date in ISO format (YYYY-MM-DD)

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskValidationError: If the due date is invalid
            TaskNotFoundError: If the task with the specified ID is not found
        """
        try:
            Task.validate_due_date(due_date)
        except ValueError as e:
            raise TaskValidationError(str(e))

        return self.task_list.update_task_due_date(task_id, due_date)

    def update_task_recurrence(self, task_id: int, recurrence_config: RecurringTaskConfig) -> bool:
        """
        Update an existing task to be recurring with the specified configuration.

        Args:
            task_id (int): The ID of the task to update
            recurrence_config (RecurringTaskConfig): The recurrence configuration to apply

        Returns:
            bool: True if update successful, False if task not found

        Raises:
            TaskNotFoundError: If the task with the specified ID is not found
        """
        task = self.task_list.get_task(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        # Update task properties to make it recurring
        task.is_recurring = True
        task.recurrence_config = recurrence_config

        return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            int: The number of tasks in the system
        """
        return len(self.task_list)