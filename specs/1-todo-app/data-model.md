# Data Model: Todo In-Memory Python Console Application

## Task Entity

**Name**: Task
**Description**: Represents a single todo item with ID, title, description, and status

**Fields**:
- `id` (int): Unique identifier for the task, auto-generated, positive integer
- `title` (str): Short description of the task, required, max 100 characters
- `description` (str): Detailed information about the task, optional, max 500 characters
- `status` (str): Completion status, either "Incomplete" or "Complete", default "Incomplete"

**Validation Rules**:
- ID must be unique across all tasks
- ID must be a positive integer
- Title must not be empty or only whitespace
- Title must not exceed 100 characters
- Status must be either "Complete" or "Incomplete"
- Description, if provided, must not exceed 500 characters

**State Transitions**:
- Default state: "Incomplete"
- Can transition to: "Complete" or back to "Incomplete"

## TaskList Collection

**Name**: TaskList
**Description**: Collection of Task entities stored in memory

**Fields**:
- `tasks` (list): List of Task objects
- `next_id` (int): Counter for generating next unique ID, starts at 1

**Operations**:
- Add task: Creates new task with unique ID and adds to collection
- Get task by ID: Returns task with specified ID or None if not found
- Update task: Modifies existing task fields
- Delete task: Removes task from collection
- List all tasks: Returns all tasks in the collection
- Mark task status: Updates status of specified task

**Validation Rules**:
- No duplicate IDs allowed
- Task ID must exist before update/delete/mark operations
- All operations must maintain data integrity