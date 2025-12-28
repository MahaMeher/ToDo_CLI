"""
Unit tests for the TaskService in the Todo In-Memory Python Console Application.
"""
import pytest
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.exceptions import TaskNotFoundError, TaskValidationError


class TestTaskService:
    """Test cases for the TaskService."""

    def test_task_service_initialization(self):
        """Test that TaskService initializes correctly."""
        service = TaskService()
        assert service.task_list is not None
        assert len(service.get_all_tasks()) == 0

    def test_add_task_success(self):
        """Test adding a task successfully."""
        service = TaskService()
        task = service.add_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status == "Incomplete"
        assert len(service.get_all_tasks()) == 1

    def test_add_task_default_description(self):
        """Test adding a task with default description."""
        service = TaskService()
        task = service.add_task("Test Title")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.status == "Incomplete"

    def test_add_task_title_validation(self):
        """Test that add_task validates title."""
        service = TaskService()

        # Empty title
        with pytest.raises(TaskValidationError):
            service.add_task("")

        # Whitespace-only title
        with pytest.raises(TaskValidationError):
            service.add_task("   ")

        # Too long title
        with pytest.raises(TaskValidationError):
            service.add_task("A" * 101)

    def test_add_task_description_validation(self):
        """Test that add_task validates description."""
        service = TaskService()

        # Too long description
        with pytest.raises(TaskValidationError):
            service.add_task("Valid Title", "A" * 501)

    def test_get_task(self):
        """Test retrieving a task by ID."""
        service = TaskService()
        added_task = service.add_task("Test Task")

        retrieved_task = service.get_task(added_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_not_found(self):
        """Test retrieving a non-existent task."""
        service = TaskService()
        service.add_task("Test Task")

        retrieved_task = service.get_task(999)
        assert retrieved_task is None

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        all_tasks = service.get_all_tasks()

        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_update_task_success(self):
        """Test updating a task successfully."""
        service = TaskService()
        original_task = service.add_task("Original Title", "Original Description")

        result = service.update_task(original_task.id, "New Title", "New Description")

        assert result is True
        updated_task = service.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        service = TaskService()
        original_task = service.add_task("Original Title", "Original Description")

        # Update only title
        result = service.update_task(original_task.id, title="New Title")
        assert result is True
        updated_task = service.get_task(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"

        # Update only description
        task2 = service.add_task("Another Task", "Another Description")
        result = service.update_task(task2.id, description="Updated Description")
        assert result is True
        updated_task2 = service.get_task(task2.id)
        assert updated_task2.description == "Updated Description"
        assert updated_task2.title == "Another Task"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        service = TaskService()
        service.add_task("Test Task")

        with pytest.raises(TaskNotFoundError):
            service.update_task(999, "New Title")

    def test_update_task_validation(self):
        """Test validation during task update."""
        service = TaskService()
        original_task = service.add_task("Original Title")

        # Update with invalid title
        with pytest.raises(TaskValidationError):
            service.update_task(original_task.id, title="")

        # Update with too long title
        with pytest.raises(TaskValidationError):
            service.update_task(original_task.id, title="A" * 101)

        # Update with too long description
        with pytest.raises(TaskValidationError):
            service.update_task(original_task.id, description="A" * 501)

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        service = TaskService()
        task = service.add_task("Test Task")

        result = service.delete_task(task.id)

        assert result is True
        assert service.get_task(task.id) is None
        assert len(service.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        service = TaskService()
        service.add_task("Test Task")

        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)

    def test_update_task_status_success(self):
        """Test updating task status successfully."""
        service = TaskService()
        task = service.add_task("Test Task", status="Incomplete")

        result = service.update_task_status(task.id, "Complete")
        assert result is True
        updated_task = service.get_task(task.id)
        assert updated_task.status == "Complete"

        result = service.update_task_status(task.id, "Incomplete")
        assert result is True
        updated_task = service.get_task(task.id)
        assert updated_task.status == "Incomplete"

    def test_update_task_status_invalid(self):
        """Test updating task status with invalid status."""
        service = TaskService()
        task = service.add_task("Test Task")

        with pytest.raises(TaskValidationError):
            service.update_task_status(task.id, "Invalid Status")

    def test_update_task_status_not_found(self):
        """Test updating status of non-existent task."""
        service = TaskService()
        service.add_task("Test Task")

        result = service.update_task_status(999, "Complete")
        assert result is False

    def test_get_next_task_id(self):
        """Test getting the next task ID."""
        service = TaskService()
        assert service.get_next_task_id() == 1

        service.add_task("Task 1")
        assert service.get_next_task_id() == 2

        service.add_task("Task 2")
        assert service.get_next_task_id() == 3

    def test_get_task_count(self):
        """Test getting the task count."""
        service = TaskService()
        assert service.get_task_count() == 0

        service.add_task("Task 1")
        assert service.get_task_count() == 1

        service.add_task("Task 2")
        assert service.get_task_count() == 2