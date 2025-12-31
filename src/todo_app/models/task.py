"""
Task model for the Todo In-Memory Python Console Application.

This module defines the Task data model with validation rules and status management.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from .recurring_task import RecurringTaskConfig


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, and status.

    Attributes:
        id (int): Unique identifier for the task, auto-generated, positive integer
        title (str): Short description of the task, required, max 100 characters
        description (str): Detailed information about the task, optional, max 500 characters
        status (str): Completion status, either "Complete" or "Incomplete", default "Incomplete"
        priority (str): Priority level, one of "high", "medium", "low", optional
        tags (List[str]): List of tags/categories for the task, optional
        due_date (str): Due date in ISO format (YYYY-MM-DD), optional
        is_recurring (bool): Whether the task is recurring, optional
        recurrence_config (RecurringTaskConfig): Configuration for recurring tasks, optional
        original_task_id (int): ID of the original task this is an instance of, optional
        reminder_time (int): Minutes before due date to show reminder, optional
    """

    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None
    is_recurring: bool = False
    recurrence_config: Optional[RecurringTaskConfig] = None
    original_task_id: Optional[int] = None
    reminder_time: Optional[int] = None

    def __post_init__(self):
        """Validate the task after initialization."""
        self.validate()

    def validate(self):
        """Validate the task fields according to the specification."""
        # Validate ID
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {self.id}")

        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or only whitespace")

        if len(self.title) > 100:
            raise ValueError(f"Task title exceeds maximum length of 100 characters: {len(self.title)}")

        # Validate description
        if len(self.description) > 500:
            raise ValueError(f"Task description exceeds maximum length of 500 characters: {len(self.description)}")

        # Validate status
        if self.status not in ["Complete", "Incomplete"]:
            raise ValueError(f"Task status must be 'Complete' or 'Incomplete', got '{self.status}'")

        # Validate priority if provided
        if self.priority is not None:
            if self.priority not in ["high", "medium", "low"]:
                raise ValueError(f"Task priority must be 'high', 'medium', or 'low', got '{self.priority}'")

        # Validate tags if provided
        if self.tags is not None:
            if not isinstance(self.tags, list):
                raise ValueError("Task tags must be a list")
            for tag in self.tags:
                if not isinstance(tag, str):
                    raise ValueError(f"Each tag must be a string, got {type(tag)} for '{tag}'")

        # Validate due_date if provided
        if self.due_date is not None:
            try:
                # Parse the date string to ensure it's in a valid format
                datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Due date must be in ISO format (YYYY-MM-DD), got '{self.due_date}'")

        # Validate is_recurring
        if not isinstance(self.is_recurring, bool):
            raise ValueError(f"is_recurring must be a boolean, got {type(self.is_recurring)}")

        # Validate recurrence_config if provided
        if self.recurrence_config is not None and not isinstance(self.recurrence_config, RecurringTaskConfig):
            raise ValueError(f"recurrence_config must be a RecurringTaskConfig instance, got {type(self.recurrence_config)}")

        # Validate original_task_id if provided
        if self.original_task_id is not None:
            if not isinstance(self.original_task_id, int) or self.original_task_id <= 0:
                raise ValueError(f"original_task_id must be a positive integer, got {self.original_task_id}")

        # Validate reminder_time if provided
        if self.reminder_time is not None:
            if not isinstance(self.reminder_time, int) or self.reminder_time < 0:
                raise ValueError(f"reminder_time must be a non-negative integer, got {self.reminder_time}")

    @staticmethod
    def validate_title(title: str) -> bool:
        """
        Validate task title.

        Args:
            title: The title to validate

        Returns:
            bool: True if title is valid, raises ValueError if invalid
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or only whitespace")

        if len(title) > 100:
            raise ValueError(f"Task title exceeds maximum length of 100 characters: {len(title)}")

        return True

    @staticmethod
    def validate_description(description: str) -> bool:
        """
        Validate task description.

        Args:
            description: The description to validate

        Returns:
            bool: True if description is valid, raises ValueError if invalid
        """
        if len(description) > 500:
            raise ValueError(f"Task description exceeds maximum length of 500 characters: {len(description)}")

        return True

    @staticmethod
    def validate_status(status: str) -> bool:
        """
        Validate task status.

        Args:
            status: The status to validate

        Returns:
            bool: True if status is valid, raises ValueError if invalid
        """
        if status not in ["Complete", "Incomplete"]:
            raise ValueError(f"Task status must be 'Complete' or 'Incomplete', got '{status}'")

        return True

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """
        Validate task priority.

        Args:
            priority: The priority to validate (high, medium, low)

        Returns:
            bool: True if priority is valid, raises ValueError if invalid
        """
        if priority not in ["high", "medium", "low"]:
            raise ValueError(f"Task priority must be 'high', 'medium', or 'low', got '{priority}'")

        return True

    @staticmethod
    def validate_tags(tags: List[str]) -> bool:
        """
        Validate task tags.

        Args:
            tags: The tags list to validate

        Returns:
            bool: True if tags are valid, raises ValueError if invalid
        """
        if not isinstance(tags, list):
            raise ValueError("Task tags must be a list")

        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError(f"Each tag must be a string, got {type(tag)} for '{tag}'")
            if not tag.strip():
                raise ValueError("Tags cannot be empty or only whitespace")

        return True

    @staticmethod
    def validate_due_date(due_date: str) -> bool:
        """
        Validate task due date.

        Args:
            due_date: The due date to validate in ISO format (YYYY-MM-DD)

        Returns:
            bool: True if due date is valid, raises ValueError if invalid
        """
        if due_date is not None:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Due date must be in ISO format (YYYY-MM-DD), got '{due_date}'")

        return True

    def mark_complete(self):
        """Mark the task as complete."""
        self.status = "Complete"

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.status = "Incomplete"

    def update_title(self, new_title: str):
        """Update the task title with validation."""
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty or only whitespace")

        if len(new_title) > 100:
            raise ValueError(f"Task title exceeds maximum length of 100 characters: {len(new_title)}")

        self.title = new_title
        self.validate()

    def update_description(self, new_description: str):
        """Update the task description with validation."""
        if len(new_description) > 500:
            raise ValueError(f"Task description exceeds maximum length of 500 characters: {len(new_description)}")

        self.description = new_description
        self.validate()

    def update_priority(self, new_priority: str):
        """Update the task priority with validation."""
        self.validate_priority(new_priority)
        self.priority = new_priority
        self.validate()

    def update_tags(self, new_tags: List[str]):
        """Update the task tags with validation."""
        self.validate_tags(new_tags)
        self.tags = new_tags if new_tags else []
        self.validate()

    def add_tags(self, tags_to_add: List[str]):
        """Add tags to the task."""
        if not tags_to_add:
            return

        self.validate_tags(tags_to_add)

        if self.tags is None:
            self.tags = []

        # Add only unique tags that aren't already present
        for tag in tags_to_add:
            if tag not in self.tags:
                self.tags.append(tag)

        self.validate()

    def remove_tags(self, tags_to_remove: List[str]):
        """Remove tags from the task."""
        if not tags_to_remove or self.tags is None:
            return

        for tag in tags_to_remove:
            if tag in self.tags:
                self.tags.remove(tag)

        self.validate()

    def update_due_date(self, new_due_date: str):
        """Update the task due date with validation."""
        self.validate_due_date(new_due_date)
        self.due_date = new_due_date
        self.validate()

    def __str__(self):
        """Return a string representation of the task."""
        result = f"[{self.id}] {self.title} - {self.status}"
        if self.priority:
            result += f" (Priority: {self.priority})"
        if self.due_date:
            result += f" (Due: {self.due_date})"
        if self.is_recurring and self.recurrence_config:
            result += f" (Recurring: {self.recurrence_config})"
        elif self.is_recurring:
            result += " (Recurring)"
        return result

    def to_dict(self):
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "tags": self.tags if self.tags is not None else [],
            "due_date": self.due_date,
            "is_recurring": self.is_recurring,
            "recurrence_config": self.recurrence_config.to_dict() if self.recurrence_config else None,
            "original_task_id": self.original_task_id,
            "reminder_time": self.reminder_time
        }

    def is_overdue(self) -> bool:
        """Check if the task is overdue based on its due date."""
        if self.due_date is None:
            return False

        try:
            due_datetime = datetime.strptime(self.due_date, "%Y-%m-%d")
            current_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return due_datetime < current_datetime
        except ValueError:
            # If due_date is not in valid format, it's not overdue
            return False

    def mark_complete(self):
        """Mark the task as complete."""
        self.status = "Complete"

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.status = "Incomplete"