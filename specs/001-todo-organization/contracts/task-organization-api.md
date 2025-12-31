# API Contracts: todo-organization

## Task Organization Endpoints

### Priority Management

#### Set Task Priority
- **Endpoint**: `POST /tasks/{id}/priority`
- **Request Body**:
  ```json
  {
    "priority": "high|medium|low"
  }
  ```
- **Response**: 200 OK with updated task object
- **Error Responses**: 400 (invalid priority), 404 (task not found)

#### Get Task Priority
- **Endpoint**: `GET /tasks/{id}/priority`
- **Response**: 200 OK with priority value
- **Error Responses**: 404 (task not found)

### Tag Management

#### Add Tags to Task
- **Endpoint**: `POST /tasks/{id}/tags`
- **Request Body**:
  ```json
  {
    "tags": ["tag1", "tag2"]
  }
  ```
- **Response**: 200 OK with updated task object
- **Error Responses**: 404 (task not found)

#### Remove Tags from Task
- **Endpoint**: `DELETE /tasks/{id}/tags`
- **Request Body**:
  ```json
  {
    "tags": ["tag1", "tag2"]
  }
  ```
- **Response**: 200 OK with updated task object
- **Error Responses**: 404 (task not found)

### Search Functionality

#### Search Tasks
- **Endpoint**: `GET /tasks/search`
- **Query Parameters**:
  - `q`: search keyword
- **Response**: 200 OK with array of matching task objects
- **Example**: `/tasks/search?q=meeting`

### Filter Functionality

#### Filter Tasks
- **Endpoint**: `GET /tasks/filter`
- **Query Parameters**:
  - `status`: filter by status
  - `priority`: filter by priority
  - `due_date_start`: filter by due date range start
  - `due_date_end`: filter by due date range end
  - `tags`: filter by tags
- **Response**: 200 OK with array of filtered task objects
- **Example**: `/tasks/filter?priority=high&status=Incomplete`

### Sort Functionality

#### Sort Tasks
- **Endpoint**: `GET /tasks/sort`
- **Query Parameters**:
  - `by`: field to sort by (priority, due_date, title)
  - `order`: sort order (asc, desc)
- **Response**: 200 OK with array of sorted task objects
- **Example**: `/tasks/sort?by=priority&order=desc`