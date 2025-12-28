"""
Task model for the Todo In-Memory Python Console Application.

This module defines the Task data model with validation rules and status management.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, and status.

    Attributes:
        id (int): Unique identifier for the task, auto-generated, positive integer
        title (str): Short description of the task, required, max 100 characters
        description (str): Detailed information about the task, optional, max 500 characters
        status (str): Completion status, either "Incomplete" or "Complete", default "Incomplete"
    """

    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"

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

    def __str__(self):
        """Return a string representation of the task."""
        return f"[{self.id}] {self.title} - {self.status}"

    def to_dict(self):
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }