"""
Recurring task configuration for the todo application.
Defines the pattern and settings for recurring tasks.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum


class RecurrencePattern(Enum):
    """Enumeration of recurrence pattern types."""
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


class RecurringTaskConfig:
    """
    Configuration class for recurring tasks.
    Defines how and when a task should repeat.
    """

    def __init__(
        self,
        pattern_type: RecurrencePattern,
        interval_days: int = 1,
        end_date: Optional[datetime] = None,
        week_days: Optional[List[int]] = None,
        enabled: bool = True
    ):
        """
        Initialize recurring task configuration.

        Args:
            pattern_type: Type of recurrence pattern (daily, weekly, custom)
            interval_days: Number of days between occurrences for custom patterns
            end_date: Optional end date for the recurrence
            week_days: List of weekdays (0=Monday, 6=Sunday) for weekly patterns
            enabled: Whether the recurrence is currently enabled
        """
        self.pattern_type = pattern_type
        self.interval_days = interval_days
        self.end_date = end_date
        self.week_days = week_days or []
        self.enabled = enabled
        self.validate()

    def validate(self) -> None:
        """
        Validate the recurrence configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        if not isinstance(self.pattern_type, RecurrencePattern):
            raise ValueError("pattern_type must be a RecurrencePattern enum value")

        if self.interval_days <= 0:
            raise ValueError("interval_days must be a positive integer")

        if self.pattern_type == RecurrencePattern.WEEKLY and self.week_days:
            for day in self.week_days:
                if not 0 <= day <= 6:
                    raise ValueError("week_days must be integers between 0 (Monday) and 6 (Sunday)")

        if self.end_date and self.end_date < datetime.now():
            raise ValueError("end_date cannot be in the past")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.

        Returns:
            Dictionary representation of the configuration
        """
        return {
            'pattern_type': self.pattern_type.value,
            'interval_days': self.interval_days,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'week_days': self.week_days,
            'enabled': self.enabled
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecurringTaskConfig':
        """
        Create a RecurringTaskConfig from a dictionary.

        Args:
            data: Dictionary containing configuration data

        Returns:
            RecurringTaskConfig instance
        """
        pattern_type = RecurrencePattern(data['pattern_type'])
        end_date = datetime.fromisoformat(data['end_date']) if data['end_date'] else None

        return cls(
            pattern_type=pattern_type,
            interval_days=data.get('interval_days', 1),
            end_date=end_date,
            week_days=data.get('week_days', []),
            enabled=data.get('enabled', True)
        )

    def should_create_next_occurrence(self, last_completion_date: datetime) -> bool:
        """
        Determine if a new occurrence should be created based on the last completion date.

        Args:
            last_completion_date: When the previous occurrence was completed

        Returns:
            True if a new occurrence should be created, False otherwise
        """
        if not self.enabled:
            return False

        if self.end_date and datetime.now() > self.end_date:
            return False

        return True

    def get_next_occurrence_date(self, current_date: datetime) -> datetime:
        """
        Calculate the next occurrence date based on the current date.

        Args:
            current_date: The current occurrence date

        Returns:
            datetime for the next occurrence
        """
        if self.pattern_type == RecurrencePattern.DAILY:
            return current_date + timedelta(days=1)
        elif self.pattern_type == RecurrencePattern.WEEKLY:
            if self.week_days:
                # Find the next occurrence based on specific week days
                # For now, just add 7 days
                return current_date + timedelta(days=7)
            else:
                return current_date + timedelta(days=7)
        elif self.pattern_type == RecurrencePattern.CUSTOM:
            return current_date + timedelta(days=self.interval_days)
        else:
            # Default to daily
            return current_date + timedelta(days=1)

    def __str__(self) -> str:
        """String representation of the configuration."""
        pattern_str = self.pattern_type.value
        if self.pattern_type == RecurrencePattern.CUSTOM:
            return f"Repeats every {self.interval_days} day(s)"
        elif self.pattern_type == RecurrencePattern.WEEKLY and self.week_days:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            day_names = [days[i] for i in self.week_days]
            return f"Repeats weekly on {', '.join(day_names)}"
        else:
            return f"Repeats {pattern_str}"