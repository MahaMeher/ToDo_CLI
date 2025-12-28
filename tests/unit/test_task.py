"""
Unit tests for the Task model in the Todo In-Memory Python Console Application.
"""
import pytest
from src.todo_app.models.task import Task
from src.todo_app.models.exceptions import TaskValidationError


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(id=1, title="Test Task", description="Test Description", status="Incomplete")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "Incomplete"

    def test_task_creation_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.status == "Incomplete"

    def test_task_id_validation_positive(self):
        """Test that task ID must be positive."""
        with pytest.raises(ValueError):
            Task(id=0, title="Test Task")

        with pytest.raises(ValueError):
            Task(id=-1, title="Test Task")

    def test_task_title_required(self):
        """Test that task title is required."""
        with pytest.raises(ValueError):
            Task(id=1, title="")

        with pytest.raises(ValueError):
            Task(id=1, title="   ")  # Only whitespace

    def test_task_title_length_limit(self):
        """Test that task title has length limit."""
        # Valid length
        Task(id=1, title="A" * 100)

        # Too long
        with pytest.raises(ValueError):
            Task(id=1, title="A" * 101)

    def test_task_description_length_limit(self):
        """Test that task description has length limit."""
        # Valid length
        Task(id=1, title="Test", description="A" * 500)

        # Too long
        with pytest.raises(ValueError):
            Task(id=1, title="Test", description="A" * 501)

    def test_task_status_validation(self):
        """Test that task status must be valid."""
        # Valid statuses
        Task(id=1, title="Test", status="Complete")
        Task(id=1, title="Test", status="Incomplete")

        # Invalid status
        with pytest.raises(ValueError):
            Task(id=1, title="Test", status="Invalid")

    def test_mark_complete(self):
        """Test marking task as complete."""
        task = Task(id=1, title="Test Task", status="Incomplete")
        task.mark_complete()
        assert task.status == "Complete"

    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task(id=1, title="Test Task", status="Complete")
        task.mark_incomplete()
        assert task.status == "Incomplete"

    def test_update_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Old Title")
        task.update_title("New Title")
        assert task.title == "New Title"

    def test_update_title_validation(self):
        """Test validation when updating title."""
        task = Task(id=1, title="Valid Title")

        # Empty title
        with pytest.raises(ValueError):
            task.update_title("")

        # Too long title
        with pytest.raises(ValueError):
            task.update_title("A" * 101)

    def test_update_description(self):
        """Test updating task description."""
        task = Task(id=1, title="Test", description="Old Description")
        task.update_description("New Description")
        assert task.description == "New Description"

    def test_update_description_validation(self):
        """Test validation when updating description."""
        task = Task(id=1, title="Test", description="Valid Description")

        # Too long description
        with pytest.raises(ValueError):
            task.update_description("A" * 501)

    def test_static_validate_title(self):
        """Test static title validation method."""
        # Valid title
        assert Task.validate_title("Valid Title") == True

        # Invalid titles
        with pytest.raises(ValueError):
            Task.validate_title("")

        with pytest.raises(ValueError):
            Task.validate_title("A" * 101)

    def test_static_validate_description(self):
        """Test static description validation method."""
        # Valid description
        assert Task.validate_description("Valid Description") == True

        # Invalid description
        with pytest.raises(ValueError):
            Task.validate_description("A" * 501)

    def test_static_validate_status(self):
        """Test static status validation method."""
        # Valid statuses
        assert Task.validate_status("Complete") == True
        assert Task.validate_status("Incomplete") == True

        # Invalid status
        with pytest.raises(ValueError):
            Task.validate_status("Invalid")