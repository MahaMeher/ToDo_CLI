"""
Datetime utility functions for the todo application.
Handles date/time operations, comparisons, and calculations for due dates and recurring tasks.
"""
from datetime import datetime, timedelta
from typing import Optional
import re


def parse_datetime(date_str: str) -> Optional[datetime]:
    """
    Parse a datetime string in ISO format (YYYY-MM-DD HH:MM) to datetime object.

    Args:
        date_str: String in format 'YYYY-MM-DD HH:MM'

    Returns:
        datetime object or None if parsing fails
    """
    if not date_str:
        return None

    # Try multiple formats
    formats = [
        '%Y-%m-%d %H:%M',  # YYYY-MM-DD HH:MM
        '%Y-%m-%d',        # YYYY-MM-DD (assumes 00:00)
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Try with seconds if available
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pass

    return None


def is_overdue(due_date: Optional[datetime]) -> bool:
    """
    Check if a task is overdue based on its due date.

    Args:
        due_date: The due date of the task

    Returns:
        True if the task is overdue, False otherwise
    """
    if due_date is None:
        return False

    return due_date < datetime.now()


def is_due_soon(due_date: Optional[str], minutes_before: int = 30) -> bool:
    """
    Check if a task is due soon based on its due date.

    Args:
        due_date: The due date of the task as a string in YYYY-MM-DD format
        minutes_before: Number of minutes before due time to consider "due soon"

    Returns:
        True if the task is due soon, False otherwise
    """
    if due_date is None:
        return False

    try:
        # Parse the due date string to a datetime object
        # For this function, we'll compare with the start of the due date
        due_datetime = datetime.strptime(due_date, "%Y-%m-%d")
        current_time = datetime.now()

        # Calculate the time difference
        time_until_due = due_datetime - current_time

        # Check if the due date is within the specified minutes from now
        return timedelta(0) <= time_until_due <= timedelta(minutes=minutes_before)
    except ValueError:
        # If due_date is not in valid format, it's not due soon
        return False


def calculate_next_occurrence(
    current_due_date: datetime,
    pattern_type: str,
    interval_days: int = 1,
    week_days: Optional[list] = None
) -> datetime:
    """
    Calculate the next occurrence date based on recurrence pattern.

    Args:
        current_due_date: The current due date
        pattern_type: 'daily', 'weekly', 'custom', or 'interval'
        interval_days: Number of days between occurrences (for daily/custom patterns)
        week_days: List of weekdays (0=Monday, 6=Sunday) for weekly patterns

    Returns:
        datetime object for the next occurrence
    """
    if pattern_type == 'daily':
        return current_due_date + timedelta(days=1)
    elif pattern_type == 'weekly':
        if week_days and len(week_days) > 0:
            # For weekly with specific days, find next occurrence
            # For now, just add 7 days
            return current_due_date + timedelta(days=7)
        else:
            return current_due_date + timedelta(days=7)
    elif pattern_type == 'custom':
        return current_due_date + timedelta(days=interval_days)
    else:
        # Default to daily
        return current_due_date + timedelta(days=1)


def validate_datetime_format(date_str: str) -> bool:
    """
    Validate if a string is in a valid datetime format.

    Args:
        date_str: String to validate

    Returns:
        True if valid format, False otherwise
    """
    return parse_datetime(date_str) is not None


def format_datetime_for_display(dt: Optional[datetime]) -> str:
    """
    Format a datetime object for display in the CLI.

    Args:
        dt: datetime object to format

    Returns:
        Formatted string or 'No due date' if None
    """
    if dt is None:
        return 'No due date'
    return dt.strftime('%Y-%m-%d %H:%M')


def get_time_until_due(due_date: Optional[datetime]) -> str:
    """
    Get a human-readable string showing time until due.

    Args:
        due_date: The due date to calculate from

    Returns:
        Human-readable time string
    """
    if due_date is None:
        return 'No due date'

    current_time = datetime.now()
    time_diff = due_date - current_time

    if time_diff.total_seconds() < 0:
        # Overdue
        days_overdue = abs(time_diff.days)
        if days_overdue == 0:
            hours_overdue = abs(int(time_diff.total_seconds() // 3600))
            return f'Overdue by {hours_overdue} hour(s)'
        else:
            return f'Overdue by {days_overdue} day(s)'
    else:
        # Not overdue
        days_until = time_diff.days
        hours_until = int(time_diff.seconds // 3600)

        if days_until == 0:
            if hours_until == 0:
                minutes = int(time_diff.seconds // 60)
                return f'Due in {minutes} minute(s)'
            else:
                return f'Due in {hours_until} hour(s)'
        else:
            return f'Due in {days_until} day(s)'