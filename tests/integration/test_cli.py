"""
Integration tests for the CLI interface in the Todo In-Memory Python Console Application.
"""
import io
import sys
from unittest.mock import patch, MagicMock
import pytest
from src.todo_app.cli.interface import CLIInterface
from src.todo_app.services.task_service import TaskService


class TestCLIIntegration:
    """Integration tests for the CLI interface."""

    def test_add_task_via_cli_success(self):
        """Test adding a task through the CLI interface successfully."""
        cli = CLIInterface()

        # Mock user inputs: title, description, priority (skip), tags (skip), due date (skip)
        inputs = iter(["Test Task Title", "Test Task Description", "", "", ""])  # Empty strings to skip priority, tags, due date

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.add_task()

                # Verify the task was added successfully
                assert result is True
                assert len(cli.task_service.get_all_tasks()) == 1

                # Get the added task and verify its properties
                task = cli.task_service.get_all_tasks()[0]
                assert task.title == "Test Task Title"
                assert task.description == "Test Task Description"
                assert task.status == "Incomplete"

    def test_add_task_via_cli_empty_title_retry(self):
        """Test CLI handles empty title input by asking again."""
        cli = CLIInterface()

        # Mock user inputs: empty title, then valid title, then description, then priority (skip), tags (skip), due date (skip)
        inputs = iter(["", "Valid Task Title", "Task Description", "", "", ""])  # Empty strings to skip priority, tags, due date

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.add_task()

                # Verify the task was added successfully after retrying with valid title
                assert result is True
                assert len(cli.task_service.get_all_tasks()) == 1

                task = cli.task_service.get_all_tasks()[0]
                assert task.title == "Valid Task Title"

    def test_add_task_via_cli_long_title_validation(self):
        """Test CLI validates long title."""
        cli = CLIInterface()

        # Mock user inputs: long title, then description, then priority (skip), tags (skip), due date (skip)
        long_title = "A" * 101  # Too long
        inputs = iter([long_title, "Task Description", "", "", ""])  # Empty strings to skip priority, tags, due date

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.add_task()

                # Verify the task was not added due to validation error
                assert result is False
                assert len(cli.task_service.get_all_tasks()) == 0

                # Verify error message was printed
                output = mock_stdout.getvalue()
                assert "exceeds maximum length" in output

    def test_view_all_tasks_empty(self):
        """Test viewing all tasks when there are no tasks."""
        cli = CLIInterface()

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = cli.view_all_tasks()

            # Verify the method completed successfully
            assert result is True

            # Verify appropriate message was displayed
            output = mock_stdout.getvalue()
            assert "No tasks found" in output

    def test_view_all_tasks_with_tasks(self):
        """Test viewing all tasks when there are tasks."""
        cli = CLIInterface()

        # Add some tasks first
        cli.task_service.add_task("Task 1", "Description 1")
        cli.task_service.add_task("Task 2", "Description 2")

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = cli.view_all_tasks()

            # Verify the method completed successfully
            assert result is True

            # Verify tasks were displayed
            output = mock_stdout.getvalue()
            assert "Task 1" in output
            assert "Task 2" in output
            assert "ID" in output  # Header should be present

    def test_update_task_via_cli(self):
        """Test updating a task through the CLI interface."""
        cli = CLIInterface()

        # Add a task first
        original_task = cli.task_service.add_task("Original Title", "Original Description")

        # Mock user inputs: task ID, new title, new description, new priority (keep current), new tags (keep current), new due date (keep current)
        inputs = iter([str(original_task.id), "Updated Title", "Updated Description", "", "", ""])  # Empty strings to keep current priority, tags, due date

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.update_task()

                # Verify the update was successful
                assert result is True

                # Get the updated task and verify its properties
                updated_task = cli.task_service.get_task(original_task.id)
                assert updated_task is not None
                assert updated_task.title == "Updated Title"
                assert updated_task.description == "Updated Description"

    def test_delete_task_via_cli(self):
        """Test deleting a task through the CLI interface."""
        cli = CLIInterface()

        # Add a task first
        task_to_delete = cli.task_service.add_task("Task to Delete", "Description")

        # Mock user inputs: task ID, confirmation (y)
        inputs = iter([str(task_to_delete.id), "y"])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.delete_task()

                # Verify the deletion was successful
                assert result is True

                # Verify the task no longer exists
                assert cli.task_service.get_task(task_to_delete.id) is None
                assert len(cli.task_service.get_all_tasks()) == 0

    def test_mark_task_complete_via_cli(self):
        """Test marking a task as complete through the CLI interface."""
        cli = CLIInterface()

        # Add a task first
        task = cli.task_service.add_task("Test Task", "Description")

        # Mock user inputs: task ID
        inputs = iter([str(task.id)])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.mark_task_complete()

                # Verify the status update was successful
                assert result is True

                # Get the updated task and verify its status
                updated_task = cli.task_service.get_task(task.id)
                assert updated_task is not None
                assert updated_task.status == "Complete"

    def test_mark_task_incomplete_via_cli(self):
        """Test marking a task as incomplete through the CLI interface."""
        cli = CLIInterface()

        # Add a task first and mark it as complete
        task = cli.task_service.add_task("Test Task", "Description")
        cli.task_service.update_task_status(task.id, "Complete")

        # Mock user inputs: task ID
        inputs = iter([str(task.id)])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                result = cli.mark_task_incomplete()

                # Verify the status update was successful
                assert result is True

                # Get the updated task and verify its status
                updated_task = cli.task_service.get_task(task.id)
                assert updated_task is not None
                assert updated_task.status == "Incomplete"

    def test_menu_display(self):
        """Test that the main menu displays correctly."""
        cli = CLIInterface()

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            cli.show_menu()

            output = mock_stdout.getvalue()

            # Verify menu options are present
            assert "Add new task" in output
            assert "View all tasks" in output
            assert "Update task" in output
            assert "Delete task" in output
            assert "Mark task as complete" in output
            assert "Mark task as incomplete" in output
            assert "Exit" in output

    def test_cli_run_loop_exit(self):
        """Test that CLI run loop can exit properly."""
        cli = CLIInterface()

        # Mock user input to select exit option immediately
        # Option 16 is exit, option 7 is "Set task priority" which requires additional input
        inputs = iter(["16"])  # Exit option

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                # This should exit after the first menu selection
                cli.run()

                output = mock_stdout.getvalue()
                assert "Goodbye!" in output