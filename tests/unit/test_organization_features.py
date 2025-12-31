"""
Unit tests for the organization features (priority, tags, search, filter, sort).
"""
import pytest
from src.todo_app.models.task import Task
from src.todo_app.models.task_list import TaskList
from src.todo_app.services.task_service import TaskService


class TestPriorityFeatures:
    """Test priority-related functionality."""

    def test_task_priority_assignment(self):
        """Test that tasks can be created with priority."""
        task = Task(id=1, title="Test Task", priority="high")
        assert task.priority == "high"

    def test_task_priority_validation(self):
        """Test that priority values are validated."""
        with pytest.raises(ValueError):
            Task(id=1, title="Test Task", priority="invalid_priority")

    def test_task_priority_update(self):
        """Test updating task priority."""
        task = Task(id=1, title="Test Task", priority="low")
        task.update_priority("high")
        assert task.priority == "high"


class TestTagFeatures:
    """Test tag-related functionality."""

    def test_task_tags_assignment(self):
        """Test that tasks can be created with tags."""
        task = Task(id=1, title="Test Task", tags=["work", "important"])
        assert "work" in task.tags
        assert "important" in task.tags

    def test_task_tags_validation(self):
        """Test that tag values are validated."""
        with pytest.raises(ValueError):
            Task(id=1, title="Test Task", tags=["valid", 123])  # tags should be strings

    def test_task_tags_update(self):
        """Test updating task tags."""
        task = Task(id=1, title="Test Task", tags=["work"])
        task.update_tags(["personal", "urgent"])
        assert "personal" in task.tags
        assert "urgent" in task.tags
        assert "work" not in task.tags

    def test_task_add_tags(self):
        """Test adding tags to existing tags."""
        task = Task(id=1, title="Test Task", tags=["work"])
        task.add_tags(["urgent", "review"])
        assert "work" in task.tags
        assert "urgent" in task.tags
        assert "review" in task.tags


class TestTaskServiceIntegration:
    """Test TaskService integration with new features."""

    def test_add_task_with_priority_and_tags(self):
        """Test adding a task with priority and tags."""
        service = TaskService()
        task = service.add_task(
            title="Test Task",
            description="A test task",
            priority="high",
            tags=["work", "important"],
            due_date="2025-12-31"
        )

        assert task.priority == "high"
        assert "work" in task.tags
        assert "important" in task.tags
        assert task.due_date == "2025-12-31"

    def test_set_task_priority(self):
        """Test setting task priority through service."""
        service = TaskService()
        task = service.add_task(title="Test Task")

        result = service.set_task_priority(task.id, "high")
        assert result is True

        updated_task = service.get_task(task.id)
        assert updated_task.priority == "high"

    def test_add_task_tags(self):
        """Test adding tags to task through service."""
        service = TaskService()
        task = service.add_task(title="Test Task", tags=["initial"])

        result = service.add_task_tags(task.id, ["new", "tag"])
        assert result is True

        updated_task = service.get_task(task.id)
        assert "initial" in updated_task.tags
        assert "new" in updated_task.tags
        assert "tag" in updated_task.tags


class TestSearchFunctionality:
    """Test search functionality."""

    def test_search_by_title(self):
        """Test searching tasks by title."""
        service = TaskService()
        service.add_task(title="Meeting with team", description="Discuss project")
        service.add_task(title="Buy groceries", description="Milk and bread")

        results = service.search_tasks("team")
        assert len(results) == 1
        assert results[0].title == "Meeting with team"

    def test_search_by_description(self):
        """Test searching tasks by description."""
        service = TaskService()
        service.add_task(title="Task 1", description="Important project work")
        service.add_task(title="Task 2", description="Less important work")

        results = service.search_tasks("project")
        assert len(results) == 1
        assert results[0].title == "Task 1"

    def test_case_insensitive_search(self):
        """Test that search is case insensitive."""
        service = TaskService()
        service.add_task(title="MEETING with team", description="discuss project")

        results = service.search_tasks("meeting")
        assert len(results) == 1
        assert results[0].title == "MEETING with team"

        results = service.search_tasks("PROJECT")
        assert len(results) == 1
        assert results[0].description == "discuss project"


class TestFilterFunctionality:
    """Test filter functionality."""

    def test_filter_by_status(self):
        """Test filtering tasks by status."""
        service = TaskService()
        service.add_task(title="Task 1", status="Complete")
        service.add_task(title="Task 2", status="Incomplete")

        completed = service.filter_tasks(status="Complete")
        assert len(completed) == 1
        assert completed[0].status == "Complete"

    def test_filter_by_priority(self):
        """Test filtering tasks by priority."""
        service = TaskService()
        service.add_task(title="Task 1", priority="high")
        service.add_task(title="Task 2", priority="low")

        high_priority = service.filter_tasks(priority="high")
        assert len(high_priority) == 1
        assert high_priority[0].priority == "high"

    def test_filter_by_tags(self):
        """Test filtering tasks by tags."""
        service = TaskService()
        service.add_task(title="Task 1", tags=["work", "urgent"])
        service.add_task(title="Task 2", tags=["personal"])

        work_tasks = service.filter_tasks(tags=["work"])
        assert len(work_tasks) == 1
        assert "work" in work_tasks[0].tags


class TestSortFunctionality:
    """Test sort functionality."""

    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        service = TaskService()
        service.add_task(title="Low Priority", priority="low")
        service.add_task(title="High Priority", priority="high")
        service.add_task(title="Medium Priority", priority="medium")

        sorted_tasks = service.sort_tasks(by="priority", order="asc")
        priorities = [task.priority for task in sorted_tasks]
        assert priorities == ["high", "medium", "low"]  # high is highest priority

    def test_sort_by_title(self):
        """Test sorting tasks by title."""
        service = TaskService()
        service.add_task(title="Zebra Task")
        service.add_task(title="Apple Task")
        service.add_task(title="Mango Task")

        sorted_tasks = service.sort_tasks(by="title", order="asc")
        titles = [task.title for task in sorted_tasks]
        assert titles == ["Apple Task", "Mango Task", "Zebra Task"]