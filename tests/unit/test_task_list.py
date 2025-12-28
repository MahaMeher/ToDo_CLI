"""
Unit tests for the TaskList collection in the Todo In-Memory Python Console Application.
"""
import pytest
from src.todo_app.models.task_list import TaskList
from src.todo_app.models.task import Task
from src.todo_app.models.exceptions import TaskNotFoundError


class TestTaskList:
    """Test cases for the TaskList collection."""

    def test_task_list_initialization(self):
        """Test that TaskList initializes correctly."""
        task_list = TaskList()
        assert len(task_list) == 0
        assert task_list.next_id == 1
        assert task_list.get_all_tasks() == []

    def test_add_task(self):
        """Test adding a task to the list."""
        task_list = TaskList()
        task = task_list.add_task("Test Task", "Test Description")

        assert len(task_list) == 1
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "Incomplete"
        assert task_list.get_task(1) == task

    def test_add_task_default_description(self):
        """Test adding a task with default description."""
        task_list = TaskList()
        task = task_list.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.status == "Incomplete"

    def test_get_task(self):
        """Test retrieving a task by ID."""
        task_list = TaskList()
        task = task_list.add_task("Test Task")

        retrieved_task = task_list.get_task(1)
        assert retrieved_task == task
        assert retrieved_task.id == 1
        assert retrieved_task.title == "Test Task"

    def test_get_task_not_found(self):
        """Test retrieving a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        assert task_list.get_task(999) is None

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")

        all_tasks = task_list.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_get_all_tasks_returns_copy(self):
        """Test that get_all_tasks returns a copy of the internal list."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        original_length = len(task_list.get_all_tasks())
        all_tasks = task_list.get_all_tasks()
        all_tasks.append("fake_task")  # This shouldn't affect the internal list

        assert len(task_list.get_all_tasks()) == original_length

    def test_update_task(self):
        """Test updating a task."""
        task_list = TaskList()
        task = task_list.add_task("Old Title", "Old Description")

        result = task_list.update_task(1, title="New Title", description="New Description")

        assert result is True
        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task_list = TaskList()
        task = task_list.add_task("Old Title", "Old Description")

        # Update only title
        result = task_list.update_task(1, title="New Title")
        assert result is True
        assert task.title == "New Title"
        assert task.description == "Old Description"

        # Update only description
        task2 = task_list.add_task("Another Task", "Another Description")
        result = task_list.update_task(2, description="Updated Description")
        assert result is True
        assert task2.description == "Updated Description"
        assert task2.title == "Another Task"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        with pytest.raises(TaskNotFoundError):
            task_list.update_task(999, title="New Title")

    def test_delete_task(self):
        """Test deleting a task."""
        task_list = TaskList()
        task = task_list.add_task("Test Task")

        result = task_list.delete_task(1)

        assert result is True
        assert len(task_list) == 0
        assert task_list.get_task(1) is None

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        with pytest.raises(TaskNotFoundError):
            task_list.delete_task(999)

    def test_update_task_status(self):
        """Test updating task status."""
        task_list = TaskList()
        task = task_list.add_task("Test Task", status="Incomplete")

        result = task_list.update_task_status(1, "Complete")

        assert result is True
        assert task.status == "Complete"

    def test_update_task_status_to_incomplete(self):
        """Test updating task status back to incomplete."""
        task_list = TaskList()
        task = task_list.add_task("Test Task", status="Complete")

        result = task_list.update_task_status(1, "Incomplete")

        assert result is True
        assert task.status == "Incomplete"

    def test_update_task_status_invalid(self):
        """Test updating task status with invalid status."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        with pytest.raises(ValueError):
            task_list.update_task_status(1, "Invalid Status")

    def test_update_task_status_not_found(self):
        """Test updating status of non-existent task."""
        task_list = TaskList()
        task_list.add_task("Test Task")

        result = task_list.update_task_status(999, "Complete")
        assert result is False

    def test_unique_ids(self):
        """Test that tasks get unique IDs."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        task3 = task_list.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_next_id_method(self):
        """Test the get_next_id method."""
        task_list = TaskList()
        assert task_list.get_next_id() == 1

        task_list.add_task("Task 1")
        assert task_list.get_next_id() == 2

        task_list.add_task("Task 2")
        assert task_list.get_next_id() == 3