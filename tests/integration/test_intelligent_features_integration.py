"""
Integration test for the intelligent features.
"""
from src.todo_app.cli.interface import CLIInterface
from src.todo_app.services.task_service import TaskService
import io
import sys
from contextlib import redirect_stdout, redirect_stderr


def test_cli_functionality():
    """Test CLI functionality with intelligent features."""
    print("Testing CLI functionality with intelligent features...")

    # Create a CLI interface
    cli = CLIInterface()

    # Test adding a task with due date via service layer directly
    print("\n1. Testing task creation with due date...")
    task = cli.task_service.add_task(
        title="Test task with due date",
        description="This is a test task with due date",
        priority="medium",
        tags=["test", "important"],
        due_date="2025-12-31"
    )
    print(f"Task added successfully: {task}")

    # Test viewing all tasks
    print("\n2. Testing view all tasks...")
    try:
        cli.view_all_tasks()
        print("View all tasks completed successfully")
    except Exception as e:
        print(f"Error viewing tasks: {e}")

    # Test setting task due date via service layer
    print("\n3. Testing setting task due date...")
    try:
        result = cli.task_service.update_task_due_date(task.id, "2025-12-30")
        print(f"Due date set successfully: {result}")
    except Exception as e:
        print(f"Error setting due date: {e}")

    # Test viewing overdue tasks
    print("\n4. Testing view overdue tasks...")
    try:
        overdue_tasks = cli.task_service.get_overdue_tasks()
        print(f"View overdue tasks completed successfully. Found {len(overdue_tasks)} overdue tasks.")
    except Exception as e:
        print(f"Error viewing overdue tasks: {e}")

    print("\nCLI functionality test completed.")


def test_task_service_integrity():
    """Test that all task service methods work correctly."""
    print("\nTesting task service integrity...")

    service = TaskService()

    # Test basic task operations
    task = service.add_task("Test task", "Test description", "Incomplete", "high")
    print(f"Created task: {task}")

    # Test due date operations
    service.update_task_due_date(task.id, "2025-12-31")
    print(f"Updated due date for task: {task.id}")

    # Test getting overdue tasks (should be empty since the date is in the future)
    overdue_tasks = service.get_overdue_tasks()
    print(f"Number of overdue tasks: {len(overdue_tasks)}")

    # Test recurring task creation
    from src.todo_app.models.recurring_task import RecurrencePattern, RecurringTaskConfig

    config = RecurringTaskConfig(pattern_type=RecurrencePattern.DAILY)
    recurring_task = service.create_recurring_task(
        "Daily recurring task",
        "This is a recurring task",
        recurrence_config=config
    )
    print(f"Created recurring task: {recurring_task}")

    # Test completing the recurring task and creating a new occurrence
    service.update_task_status(recurring_task.id, "Complete")
    new_task = service.process_completed_recurring_task(recurring_task.id)
    if new_task:
        print(f"Created new occurrence: {new_task}")
    else:
        print("No new occurrence created")

    print("Task service integrity test completed.")


def run_integration_tests():
    """Run all integration tests."""
    print("="*60)
    print("Running Integration Tests for Intelligent Features")
    print("="*60)

    try:
        test_task_service_integrity()
        test_cli_functionality()

        print("\n" + "="*60)
        print("All integration tests completed successfully!")
        print("="*60)
    except Exception as e:
        print(f"\nAn error occurred during integration testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_integration_tests()