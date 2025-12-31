# Data Model: todo-organization

## Extended Task Model

### Entity: Task
**Description**: Represents a todo item with extended attributes for organization features

**Fields**:
- `id`: integer (auto-generated, unique identifier)
- `title`: string (required, max 100 characters)
- `description`: string (optional, max 500 characters)
- `status`: string (enum: "Complete", "Incomplete", default: "Incomplete")
- `priority`: string (enum: "high", "medium", "low", optional, default: null/None)
- `tags`: list of strings (optional, default: empty list)
- `due_date`: string or date object (optional, ISO format: YYYY-MM-DD, default: null/None)

**Validation Rules**:
- `priority` must be one of: "high", "medium", "low" (FR-007)
- `tags` must be a list of strings (FR-008)
- `title` and `description` validation remains from basic functionality
- `status` validation remains from basic functionality

**State Transitions**:
- `status` can transition between "Complete" and "Incomplete" (existing functionality)
- `priority` can be set/updated independently (FR-001)
- `tags` can be added/removed independently (FR-002)
- `due_date` can be set/updated independently

### Entity: SearchResult
**Description**: Represents filtered subset of tasks based on search criteria

**Fields**:
- `tasks`: list of Task objects (matching search criteria)
- `query`: string (the search keyword used)
- `total_count`: integer (total number of matching tasks)

### Entity: FilterCriteria
**Description**: Represents parameters for filtering tasks

**Fields**:
- `status`: string (optional, filter by status)
- `priority`: string (optional, filter by priority: "high", "medium", "low")
- `date_range`: object with `start_date` and `end_date` (optional, filter by due date range)
- `tags`: list of strings (optional, filter by tags)

### Entity: SortCriteria
**Description**: Represents parameters for sorting tasks

**Fields**:
- `field`: string (sort by: "due_date", "priority", "title", "status")
- `direction`: string (sort order: "asc", "desc", default: "asc")
- `priority_order`: list (custom priority order for sorting: e.g., ["high", "medium", "low"])

## Data Relationships

### Task Relationships
- One Task can have multiple Tags (one-to-many relationship through the tags list)
- Task contains all organization features within a single entity

## Validation Rules Summary

1. **Priority Validation**: Task priority must be one of "high", "medium", "low" (FR-007)
2. **Multiple Tags**: Tasks must support multiple tags (FR-008)
3. **Case-Insensitive Search**: Search functionality must be case-insensitive (FR-009)
4. **Required Fields**: Existing validation for title and description remains
5. **Status Validation**: Existing validation for status remains

## Backward Compatibility

- All new fields (priority, tags, due_date) are optional to maintain compatibility with existing tasks
- Existing task functionality remains unchanged (FR-006, FR-011)
- Default values ensure existing tasks work without modification