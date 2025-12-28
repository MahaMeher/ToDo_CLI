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
            task = self.task_service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
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

        print(f"{'ID':<4} {'Status':<12} {'Title':<30} {'Description'}")
        print("-" * 80)
        for task in tasks:
            status = f"[{task.status}]" if task.status == "Complete" else f" {task.status} "
            print(f"{task.id:<4} {status:<12} {task.title[:29]:<30} {task.description[:30]}")

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

        print(f"Current task: ID {task.id}, Title: '{task.title}', Description: '{task.description}'")

        # Get new title (optional)
        new_title_input = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        new_title = None
        if new_title_input:
            new_title = new_title_input

        # Get new description (optional)
        new_description_input = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ")
        new_description = None
        if new_description_input != task.description:
            new_description = new_description_input

        try:
            # Update the task
            result = self.task_service.update_task(task_id, new_title, new_description)
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
        print("7. Exit")
        print("-"*50)

    def get_user_choice(self) -> str:
        """
        Get user choice from the menu.

        Returns:
            str: The user's choice
        """
        try:
            choice = input("Enter your choice (1-7): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nOperation cancelled by user.")
            return "7"  # Return exit choice

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
                print("Thank you for using the Todo Application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")