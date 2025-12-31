# Research: todo-organization

## Decision: Priority representation
**Rationale**: Using string enumeration (high, medium, low) rather than numeric values or separate enum class. This approach is simpler to implement with Python standard library only, provides clear semantic meaning, and is easily validated. Strings are also more readable in console output.
**Alternatives considered**:
- Numeric values (1, 2, 3) - less readable
- Python Enum class - would require additional imports, not in standard library approach
- Boolean flags (urgent, normal) - doesn't support three-tier system

## Decision: Tag structure
**Rationale**: Implementing tags as a list of strings allows for multiple tags per task as required by the specification (FR-008). Using a simple list is memory efficient and allows for flexible tagging without complex relationships. This approach supports the requirement for multiple tags per task.
**Alternatives considered**:
- Single tag per task - doesn't meet requirement for multiple tags
- Tag objects with ID and name - over-engineering for this use case
- Dictionary-based tags - unnecessary complexity

## Decision: Filtering strategy
**Rationale**: Implementing filtering as a combination of boolean checks on task attributes. This approach allows for combining multiple filters (status, priority, date) and can be efficiently implemented using Python list comprehensions. The approach supports the requirement to filter by multiple attributes (FR-004).
**Alternatives considered**:
- Separate filter classes - over-engineering for this use case
- Database-style query language - too complex for in-memory implementation
- Multiple separate filtering methods - harder to combine filters

## Decision: Sorting precedence rules
**Rationale**: Implementing stable sorting with primary, secondary, and tertiary criteria. For example, when sorting by priority, tasks with the same priority will maintain their relative order or can be further sorted by other criteria if specified. Python's built-in sort is stable, which helps maintain consistent ordering. The approach supports all required sorting methods (due date, priority, alphabetical) as specified in FR-005.
**Alternatives considered**:
- Complex comparison functions - harder to maintain
- Multiple sort passes - less efficient
- Priority-based sorting only - doesn't support all required sorting methods

## Decision: Search implementation
**Rationale**: Implementing case-insensitive substring search across title and description fields using simple string operations. This meets the requirement for keyword search (FR-003) and case-insensitive search (FR-009). Using 'in' operator with lower() is efficient for in-memory operations.
**Alternatives considered**:
- Regular expressions - overkill for simple keyword matching
- Full-text search engines - inappropriate for in-memory console app
- Exact matching only - doesn't meet usability requirements

## Decision: Data model extensions
**Rationale**: Extending the existing Task model with optional priority, tags, and due_date attributes. This maintains backward compatibility while adding new functionality. The extended attributes are optional to maintain compatibility with existing tasks.
**Alternatives considered**:
- Separate organization model - would complicate relationships
- Complete model rewrite - unnecessary breaking change
- Composition pattern - adds complexity without benefit for this use case