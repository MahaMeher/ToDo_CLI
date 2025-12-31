"""
CLI Interface for the Todo In-Memory Python Console Application.

This module provides the console interface and command handlers for the todo app.
"""
from typing import Optional
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.exceptions import TaskValidationError


class CLIInterface:
    """
    Console interface and command handlers for the todo application.

    This class manages the user interface and connects user input to the
    appropriate service methods.
    """

    def __init__(self):
        """Initialize the CLI interface with a task service."""
        self.task_service = TaskService()

    def add_task(self) -> bool:
        """
        Add a new task through the CLI.

        Returns:
            bool: True if task was added successfully, False otherwise
        """
        print("\n--- Add New Task ---")

        # Get task title
        while True:
            title = input("Enter task title: ").strip()
            if title:
                break
            print("Error: Task title cannot be empty. Please enter a valid title.")

        # Get task description (optional)
        description = input("Enter task description (optional, press Enter to skip): ")

        # Get task priority (optional)
        priority_input = input("Enter priority (high/medium/low, press Enter to skip): ").strip().lower()
        priority = priority_input if priority_input in ["high", "medium", "low"] else None

        # Get task tags (optional)
        tags_input = input("Enter tags (comma-separated, press Enter to skip): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else None

        # Get due date (optional)
        due_date = input("Enter due date (YYYY-MM-DD, press Enter to skip): ").strip()
        due_date = due_date if due_date else None

        try:
            # Validate title length
            if len(title) > 100:
                print(f"Error: Task title exceeds maximum length of 100 characters. Current length: {len(title)}")
                return False

            # Validate description length
            if len(description) > 500:
                print(f"Error: Task description exceeds maximum length of 500 characters. Current length: {len(description)}")
                return False

            # Add the task
            task = self.task_service.add_task(title, description, priority=priority, tags=tags, due_date=due_date)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
            if task.priority:
                print(f"Priority: {task.priority}")
            if task.tags:
                print(f"Tags: {', '.join(task.tags)}")
            if task.due_date:
                print(f"Due Date: {task.due_date}")
            return True

        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def view_all_tasks(self) -> bool:
        """
        Display all tasks through the CLI.

        Returns:
            bool: True if tasks were displayed successfully
        """
        print("\n--- All Tasks ---")
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return True

        print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Overdue':<8} {'Recurring':<15} {'Title':<30} {'Tags'}")
        print("-" * 125)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            priority = task.priority if task.priority else "None"
            due_date = task.due_date if task.due_date else "None"
            # Check if task is overdue
            is_overdue = "Yes" if task.is_overdue() else "No"
            # Check if task is recurring and show recurrence info
            if task.is_recurring and task.recurrence_config:
                recurring_info = f"Every {task.recurrence_config.interval_days} day(s)" if task.recurrence_config.pattern_type.value == 'custom' else task.recurrence_config.pattern_type.value.title()
            elif task.is_recurring:
                recurring_info = "Yes"
            else:
                recurring_info = "No"
            tags_str = ", ".join(task.tags) if task.tags else "None"
            print(f"{task.id:<4} {status:<12} {priority:<10} {due_date:<12} {is_overdue:<8} {recurring_info:<15} {task.title[:29]:<30} {tags_str}")

        return True

    def update_task(self) -> bool:
        """
        Update an existing task through the CLI.

        Returns:
            bool: True if task was updated successfully, False otherwise
        """
        print("\n--- Update Task ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to update: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}', Description: '{task.description}', "
              f"Status: '{task.status}', Priority: '{task.priority}', Tags: {task.tags}, Due Date: '{task.due_date}'")

        # Get new title (optional)
        new_title_input = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        new_title = new_title_input if new_title_input else None

        # Get new description (optional)
        new_description_input = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ")
        new_description = new_description_input if new_description_input != task.description else None

        # Get new priority (optional)
        new_priority_input = input(f"Enter new priority (current: '{task.priority}', high/medium/low, press Enter to keep current): ").strip().lower()
        new_priority = new_priority_input if new_priority_input in ["high", "medium", "low"] else None

        # Get new tags (optional)
        new_tags_input = input(f"Enter new tags (comma-separated, current: {task.tags}, press Enter to keep current): ").strip()
        new_tags = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()] if new_tags_input else None

        # Get new due date (optional)
        new_due_date_input = input(f"Enter new due date (current: '{task.due_date}', YYYY-MM-DD, press Enter to keep current): ").strip()
        new_due_date = new_due_date_input if new_due_date_input else None

        try:
            # Update the task
            result = self.task_service.update_task(task_id, new_title, new_description, new_priority, new_tags, new_due_date)
            if result:
                print(f"Task {task_id} updated successfully!")
                return True
            else:
                print(f"Error: Failed to update task {task_id}.")
                return False
        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def delete_task(self) -> bool:
        """
        Delete a task through the CLI.

        Returns:
            bool: True if task was deleted successfully, False otherwise
        """
        print("\n--- Delete Task ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to delete: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete task {task_id}? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Task deletion cancelled.")
            return True

        try:
            # Delete the task
            result = self.task_service.delete_task(task_id)
            if result:
                print(f"Task {task_id} deleted successfully!")
                return True
            else:
                print(f"Error: Task with ID {task_id} not found.")
                return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def mark_task_complete(self) -> bool:
        """
        Mark a task as complete through the CLI.

        Returns:
            bool: True if task status was updated successfully, False otherwise
        """
        print("\n--- Mark Task Complete ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to mark complete: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        try:
            # Update task status
            result = self.task_service.update_task_status(task_id, "Complete")
            if result:
                print(f"Task {task_id} marked as complete!")
                return True
            else:
                print(f"Error: Task with ID {task_id} not found.")
                return False
        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def mark_task_incomplete(self) -> bool:
        """
        Mark a task as incomplete through the CLI.

        Returns:
            bool: True if task status was updated successfully, False otherwise
        """
        print("\n--- Mark Task Incomplete ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to mark incomplete: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        try:
            # Update task status
            result = self.task_service.update_task_status(task_id, "Incomplete")
            if result:
                print(f"Task {task_id} marked as incomplete!")
                return True
            else:
                print(f"Error: Task with ID {task_id} not found.")
                return False
        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def set_task_priority(self) -> bool:
        """
        Set the priority of a task through the CLI.

        Returns:
            bool: True if task priority was updated successfully, False otherwise
        """
        print("\n--- Set Task Priority ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to set priority: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}', Current Priority: '{task.priority}'")

        # Get priority level
        while True:
            priority = input("Enter priority (high/medium/low, press Enter to cancel): ").strip().lower()
            if not priority:
                print("Priority update cancelled.")
                return True
            if priority in ["high", "medium", "low"]:
                break
            print("Error: Priority must be 'high', 'medium', or 'low'.")

        try:
            # Set task priority
            result = self.task_service.set_task_priority(task_id, priority)
            if result:
                print(f"Priority for task {task_id} set to '{priority}' successfully!")
                return True
            else:
                print(f"Error: Failed to set priority for task {task_id}.")
                return False
        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def add_task_tags(self) -> bool:
        """
        Add tags to a task through the CLI.

        Returns:
            bool: True if tags were added successfully, False otherwise
        """
        print("\n--- Add Task Tags ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to add tags: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}'")
        print(f"Current tags: {task.tags if task.tags else 'None'}")

        # Get tags to add
        tags_input = input("Enter tags to add (comma-separated, press Enter to cancel): ").strip()
        if not tags_input:
            print("Tag addition cancelled.")
            return True

        # Parse tags
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        if not tags:
            print("No valid tags provided.")
            return False

        try:
            # Add tags to task
            result = self.task_service.add_task_tags(task_id, tags)
            if result:
                print(f"Tags {tags} added to task {task_id} successfully!")
                return True
            else:
                print(f"Error: Failed to add tags to task {task_id}.")
                return False
        except TaskValidationError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def remove_task_tags(self) -> bool:
        """
        Remove tags from a task through the CLI.

        Returns:
            bool: True if tags were removed successfully, False otherwise
        """
        print("\n--- Remove Task Tags ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to remove tags: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}'")
        print(f"Current tags: {task.tags if task.tags else 'None'}")

        if not task.tags:
            print("Task has no tags to remove.")
            return True

        # Get tags to remove
        tags_input = input("Enter tags to remove (comma-separated, press Enter to cancel): ").strip()
        if not tags_input:
            print("Tag removal cancelled.")
            return True

        # Parse tags
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        if not tags:
            print("No valid tags provided.")
            return False

        try:
            # Remove tags from task
            result = self.task_service.remove_task_tags(task_id, tags)
            if result:
                print(f"Tags {tags} removed from task {task_id} successfully!")
                return True
            else:
                print(f"Error: Failed to remove tags from task {task_id}.")
                return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def search_tasks(self) -> bool:
        """
        Search tasks by keyword through the CLI.

        Returns:
            bool: True if search was performed successfully, False otherwise
        """
        print("\n--- Search Tasks ---")

        # Get search query
        query = input("Enter search keyword: ").strip()
        if not query:
            print("Search cancelled - no query provided.")
            return True

        # Perform search
        tasks = self.task_service.search_tasks(query)

        if not tasks:
            print(f"No tasks found matching '{query}'.")
            return True

        print(f"\nFound {len(tasks)} task(s) matching '{query}':")
        print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Title':<30} {'Tags'}")
        print("-" * 80)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            priority = task.priority if task.priority else "None"
            tags_str = ", ".join(task.tags) if task.tags else "None"
            print(f"{task.id:<4} {status:<12} {priority:<10} {task.title[:29]:<30} {tags_str}")

        return True

    def filter_tasks(self) -> bool:
        """
        Filter tasks by various criteria through the CLI.

        Returns:
            bool: True if filtering was performed successfully, False otherwise
        """
        print("\n--- Filter Tasks ---")

        # Get filter criteria with options like sort
        print("Filter by options:")
        print("1. Status (Complete/Incomplete)")
        print("2. Priority (high/medium/low)")
        print("3. Tags (comma-separated)")
        print("4. Due Date (YYYY-MM-DD)")
        print("5. Multiple filters")
        print("6. Clear all filters (show all tasks)")
        filter_choice = input("Enter filter option (1-6, default is 1): ").strip()

        # Perform filtering based on choice
        if filter_choice == "1":
            status = input("Filter by status (Complete/Incomplete): ").strip()
            status = status if status.lower() in ["complete", "incomplete"] else None
            if status:
                tasks = self.task_service.filter_tasks(status=status)
            else:
                print("No valid status provided.")
                return True
        elif filter_choice == "2":
            priority = input("Filter by priority (high/medium/low): ").strip()
            priority = priority.lower() if priority.lower() in ["high", "medium", "low"] else None
            if priority:
                tasks = self.task_service.filter_tasks(priority=priority)
            else:
                print("No valid priority provided.")
                return True
        elif filter_choice == "3":
            tags_input = input("Filter by tags (comma-separated): ").strip()
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                tasks = self.task_service.filter_tasks(tags=tags)
            else:
                print("No tags provided.")
                return True
        elif filter_choice == "4":
            due_date = input("Filter by due date (YYYY-MM-DD): ").strip()
            if due_date:
                tasks = self.task_service.filter_tasks(due_date=due_date)
            else:
                print("No due date provided.")
                return True
        elif filter_choice == "5":
            # Multiple filters
            print("Enter multiple filter criteria (press Enter to skip each):")
            status = input("Filter by status (Complete/Incomplete): ").strip()
            status = status if status.lower() in ["complete", "incomplete"] else None

            priority = input("Filter by priority (high/medium/low): ").strip()
            priority = priority.lower() if priority.lower() in ["high", "medium", "low"] else None

            tags_input = input("Filter by tags (comma-separated): ").strip()
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else None

            due_date = input("Filter by due date (YYYY-MM-DD): ").strip()
            due_date = due_date if due_date else None

            tasks = self.task_service.filter_tasks(status=status, priority=priority, tags=tags, due_date=due_date)
        elif filter_choice == "6":
            # Show all tasks (no filter)
            tasks = self.task_service.get_all_tasks()
        else:
            # Default to status filter
            status = input("Filter by status (Complete/Incomplete): ").strip()
            status = status if status.lower() in ["complete", "incomplete"] else None
            if status:
                tasks = self.task_service.filter_tasks(status=status)
            else:
                print("No valid status provided.")
                return True

        if not tasks:
            print("No tasks found matching the filter criteria.")
            return True

        print(f"\nFound {len(tasks)} task(s) matching the filter criteria:")
        print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Title':<30} {'Tags'}")
        print("-" * 90)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            priority = task.priority if task.priority else "None"
            due_date = task.due_date if task.due_date else "None"
            tags_str = ", ".join(task.tags) if task.tags else "None"
            print(f"{task.id:<4} {status:<12} {priority:<10} {due_date:<12} {task.title[:29]:<30} {tags_str}")

        return True

    def set_task_recurrence(self) -> bool:
        """
        Set recurrence for a task through the CLI.

        Returns:
            bool: True if recurrence was set successfully, False otherwise
        """
        print("\n--- Set Task Recurrence ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to set recurrence: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}'")

        # Get recurrence type
        print("\nRecurrence options:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Custom (every N days)")
        recurrence_choice = input("Enter recurrence option (1-3): ").strip()

        from src.todo_app.models.recurring_task import RecurrencePattern, RecurringTaskConfig

        try:
            if recurrence_choice == "1":
                recurrence_config = RecurringTaskConfig(pattern_type=RecurrencePattern.DAILY)
            elif recurrence_choice == "2":
                recurrence_config = RecurringTaskConfig(pattern_type=RecurrencePattern.WEEKLY)
            elif recurrence_choice == "3":
                interval_input = input("Enter interval in days: ").strip()
                if not interval_input.isdigit() or int(interval_input) <= 0:
                    print("Error: Interval must be a positive number.")
                    return False
                interval = int(interval_input)
                recurrence_config = RecurringTaskConfig(
                    pattern_type=RecurrencePattern.CUSTOM,
                    interval_days=interval
                )
            else:
                print("Invalid choice. Setting to daily recurrence.")
                recurrence_config = RecurringTaskConfig(pattern_type=RecurrencePattern.DAILY)

            # Update the existing task to be recurring
            result = self.task_service.update_task_recurrence(task_id, recurrence_config)
            if result:
                print(f"Recurrence set for task {task_id}.")
                print(f"Task will now repeat based on: {recurrence_config}")
                return True
            else:
                print(f"Error: Failed to set recurrence for task {task_id}.")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def set_task_due_date(self) -> bool:
        """
        Set due date for a task through the CLI.

        Returns:
            bool: True if due date was set successfully, False otherwise
        """
        print("\n--- Set Task Due Date ---")

        # Get task ID
        try:
            task_id_input = input("Enter task ID to set due date: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return False
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid task ID format.")
            return False

        # Check if task exists
        task = self.task_service.get_task(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: ID {task.id}, Title: '{task.title}', Current Due Date: '{task.due_date}'")

        # Get due date
        due_date = input("Enter due date (YYYY-MM-DD, press Enter to clear): ").strip()
        if not due_date:
            due_date = None
        elif due_date.lower() == 'clear':
            due_date = None

        try:
            if due_date:
                # Validate the date format
                from datetime import datetime
                datetime.strptime(due_date, "%Y-%m-%d")

            # Update the task due date
            result = self.task_service.update_task_due_date(task_id, due_date)
            if result:
                print(f"Due date for task {task_id} set to '{due_date}' successfully!")
                return True
            else:
                print(f"Error: Failed to set due date for task {task_id}.")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def view_overdue_tasks(self) -> bool:
        """
        View all overdue tasks through the CLI.

        Returns:
            bool: True if overdue tasks were displayed successfully
        """
        print("\n--- Overdue Tasks ---")
        tasks = self.task_service.get_overdue_tasks()

        if not tasks:
            print("No overdue tasks found.")
            return True

        print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Recurring':<15} {'Title':<30} {'Tags'}")
        print("-" * 115)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            priority = task.priority if task.priority else "None"
            due_date = task.due_date if task.due_date else "None"
            # Check if task is recurring and show recurrence info
            if task.is_recurring and task.recurrence_config:
                recurring_info = f"Every {task.recurrence_config.interval_days} day(s)" if task.recurrence_config.pattern_type.value == 'custom' else task.recurrence_config.pattern_type.value.title()
            elif task.is_recurring:
                recurring_info = "Yes"
            else:
                recurring_info = "No"
            tags_str = ", ".join(task.tags) if task.tags else "None"
            print(f"{task.id:<4} {status:<12} {priority:<10} {due_date:<12} {recurring_info:<15} {task.title[:29]:<30} {tags_str}")

        return True

    def sort_tasks(self) -> bool:
        """
        Sort tasks by various criteria through the CLI.

        Returns:
            bool: True if sorting was performed successfully, False otherwise
        """
        print("\n--- Sort Tasks ---")

        # Get sort criteria
        print("Sort by options:")
        print("1. ID")
        print("2. Title")
        print("3. Status")
        print("4. Priority")
        print("5. Due Date")
        sort_choice = input("Enter sort option (1-5, default is 1): ").strip()

        sort_options = {
            "1": "id",
            "2": "title",
            "3": "status",
            "4": "priority",
            "5": "due_date"
        }
        by = sort_options.get(sort_choice, "id")

        order_input = input("Sort order (asc/desc, default is asc): ").strip().lower()
        order = "desc" if order_input == "desc" else "asc"

        # Perform sorting
        tasks = self.task_service.sort_tasks(by=by, order=order)

        if not tasks:
            print("No tasks to display.")
            return True

        print(f"\nTasks sorted by {by} ({order}):")
        print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Title':<30} {'Tags'}")
        print("-" * 90)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            priority = task.priority if task.priority else "None"
            due_date = task.due_date if task.due_date else "None"
            tags_str = ", ".join(task.tags) if task.tags else "None"
            print(f"{task.id:<4} {status:<12} {priority:<10} {due_date:<12} {task.title[:29]:<30} {tags_str}")

        return True

    def show_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("Todo Application - Main Menu")
        print("="*50)
        print("1. Add new task")
        print("2. View all tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Mark task as complete")
        print("6. Mark task as incomplete")
        print("7. Set task priority")
        print("8. Add task tags")
        print("9. Remove task tags")
        print("10. Search tasks")
        print("11. Filter tasks")
        print("12. Sort tasks")
        print("13. Set task due date")
        print("14. Set task recurrence")
        print("15. View overdue tasks")
        print("16. Exit")
        print("-"*50)

    def get_user_choice(self) -> str:
        """
        Get user choice from the menu.

        Returns:
            str: The user's choice
        """
        try:
            choice = input("Enter your choice (1-16): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nOperation cancelled by user.")
            return "16"  # Return exit choice

    def run(self):
        """Run the main CLI loop."""
        print("Welcome to the Todo Application!")

        while True:
            self.show_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_task_complete()
            elif choice == "6":
                self.mark_task_incomplete()
            elif choice == "7":
                self.set_task_priority()
            elif choice == "8":
                self.add_task_tags()
            elif choice == "9":
                self.remove_task_tags()
            elif choice == "10":
                self.search_tasks()
            elif choice == "11":
                self.filter_tasks()
            elif choice == "12":
                self.sort_tasks()
            elif choice == "13":
                self.set_task_due_date()
            elif choice == "14":
                self.set_task_recurrence()
            elif choice == "15":
                self.view_overdue_tasks()
            elif choice == "16":
                print("Thank you for using the Todo Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 16.")