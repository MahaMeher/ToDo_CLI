"""
Test script for the intelligent features of the todo application.
Tests recurring tasks, due dates, and overdue functionality.
"""
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.recurring_task import RecurrencePattern, RecurringTaskConfig
from datetime import datetime, timedelta

def test_basic_functionality():
    """Test basic task functionality with new intelligent features."""
    print("Testing basic functionality with intelligent features...")
    service = TaskService()

    # Test adding a task with due date
    task = service.add_task(
        title="Test task with due date",
        description="This is a test task",
        due_date="2024-12-31"
    )
    print(f"Created task: {task}")
    print(f"Task is overdue: {task.is_overdue()}")

    # Test adding a task that is already overdue
    overdue_task = service.add_task(
        title="Overdue task",
        description="This task is already overdue",
        due_date="2020-01-01"  # Past date
    )
    print(f"Created overdue task: {overdue_task}")
    print(f"Overdue task is overdue: {overdue_task.is_overdue()}")

    # Test getting overdue tasks
    overdue_tasks = service.get_overdue_tasks()
    print(f"Number of overdue tasks: {len(overdue_tasks)}")
    for task in overdue_tasks:
        print(f"  - {task}")

    print("Basic functionality test completed.\n")


def test_recurring_tasks():
    """Test recurring task functionality."""
    print("Testing recurring task functionality...")
    service = TaskService()

    # Create a recurring task configuration
    recurrence_config = RecurringTaskConfig(
        pattern_type=RecurrencePattern.DAILY,
        interval_days=1
    )

    # Create a recurring task
    recurring_task = service.create_recurring_task(
        title="Daily recurring task",
        description="This task repeats daily",
        due_date="2025-01-01",
        recurrence_config=recurrence_config
    )
    print(f"Created recurring task: {recurring_task}")
    print(f"Task is recurring: {recurring_task.is_recurring}")

    # Complete the recurring task and check if a new one is created
    service.update_task_status(recurring_task.id, "Complete")
    print(f"Completed recurring task: {recurring_task.id}")

    # Process the completed recurring task to create next occurrence
    new_task = service.process_completed_recurring_task(recurring_task.id)
    if new_task:
        print(f"Created new occurrence: {new_task}")
    else:
        print("No new occurrence created (this may be expected behavior)")

    print("Recurring task test completed.\n")


def test_due_soon_functionality():
    """Test due soon functionality."""
    print("Testing due soon functionality...")
    service = TaskService()

    # Add a task due tomorrow (should be due soon with default 30 min threshold)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    task = service.add_task(
        title="Task due tomorrow",
        due_date=tomorrow
    )
    print(f"Created task due tomorrow: {task}")

    # Add a task due in 10 days (should not be due soon)
    future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    future_task = service.add_task(
        title="Task due in 10 days",
        due_date=future_date
    )
    print(f"Created task due in 10 days: {future_task}")

    # Get tasks due soon (default is 30 minutes before due time)
    due_soon_tasks = service.get_due_soon_tasks()
    print(f"Number of tasks due soon: {len(due_soon_tasks)}")

    print("Due soon functionality test completed.\n")


def run_all_tests():
    """Run all tests for intelligent features."""
    print("="*50)
    print("Testing Intelligent Features")
    print("="*50)

    try:
        test_basic_functionality()
        test_recurring_tasks()
        test_due_soon_functionality()

        print("="*50)
        print("All tests completed!")
        print("="*50)
    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()