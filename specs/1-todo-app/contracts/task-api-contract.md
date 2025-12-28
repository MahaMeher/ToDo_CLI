# Task Management API Contracts

## Task Creation Contract

**Endpoint**: `create_task(title: str, description: str) -> Task`
**Description**: Creates a new task with the provided title and description

**Input**:
- `title` (str, required): Task title (1-100 characters)
- `description` (str, optional): Task description (0-500 characters)

**Output**:
- `Task` object with assigned ID and "Incomplete" status

**Validation**:
- Title must not be empty or only whitespace
- Title must not exceed 100 characters
- Description, if provided, must not exceed 500 characters

**Error Cases**:
- Invalid title: Returns error message
- Title too long: Returns error message

## Task Retrieval Contract

**Endpoint**: `get_task(task_id: int) -> Task | None`
**Description**: Retrieves a task by its ID

**Input**:
- `task_id` (int, required): Unique identifier of the task

**Output**:
- `Task` object if found, `None` if not found

**Error Cases**:
- Task not found: Returns None

## Task Listing Contract

**Endpoint**: `get_all_tasks() -> List[Task]`
**Description**: Retrieves all tasks in the system

**Input**: None
**Output**: List of all Task objects

## Task Update Contract

**Endpoint**: `update_task(task_id: int, title: str = None, description: str = None) -> bool`
**Description**: Updates an existing task's information

**Input**:
- `task_id` (int, required): ID of the task to update
- `title` (str, optional): New title for the task
- `description` (str, optional): New description for the task

**Output**:
- `True` if update successful, `False` if task not found

**Error Cases**:
- Task not found: Returns False
- Invalid title: Returns False with error

## Task Deletion Contract

**Endpoint**: `delete_task(task_id: int) -> bool`
**Description**: Deletes a task by its ID

**Input**:
- `task_id` (int, required): ID of the task to delete

**Output**:
- `True` if deletion successful, `False` if task not found

**Error Cases**:
- Task not found: Returns False

## Task Status Update Contract

**Endpoint**: `update_task_status(task_id: int, status: str) -> bool`
**Description**: Updates the completion status of a task

**Input**:
- `task_id` (int, required): ID of the task to update
- `status` (str, required): New status ("Complete" or "Incomplete")

**Output**:
- `True` if update successful, `False` if task not found

**Validation**:
- Status must be either "Complete" or "Incomplete"

**Error Cases**:
- Task not found: Returns False
- Invalid status: Returns False