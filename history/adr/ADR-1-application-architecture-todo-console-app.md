# ADR-1: Application Architecture for Todo Console Application

## Status
Accepted

## Date
2025-12-29

## Context
We need to develop a console-based todo application that stores tasks in memory with full CRUD functionality plus status management. The application must follow Python 3.13+ standards with clean architecture and proper error handling. We need to make decisions about the overall architecture, data storage approach, and component organization.

## Decision
We will implement a clean architecture pattern with the following key decisions:

**Technology Stack:**
- Language: Python 3.13+
- Dependencies: Standard library only (no external dependencies)
- Testing: pytest for unit and functional tests

**Architecture Pattern:**
- Layered architecture with clear separation of concerns:
  - Models layer: Task data model and TaskList collection
  - Services layer: Business logic for task operations
  - CLI layer: Console interface and command handlers

**Data Management:**
- In-memory storage using Python data structures (list/dict combination)
- Auto-incrementing integer IDs for task identification
- Task objects with validation rules for title, description, and status

**User Interface:**
- Menu-driven console interface with numbered options
- Input validation to prevent crashes from invalid input
- User-friendly error messages for graceful error handling

## Alternatives Considered
- **Technology Stack Alternatives:**
  - Full web framework (too complex for console app)
  - Multiple external dependencies (violates in-memory constraint)
  - Different programming languages (would not meet Python requirement)

- **Architecture Pattern Alternatives:**
  - Monolithic approach (would create tightly coupled code)
  - Event-driven architecture (unnecessarily complex for simple todo app)
  - Direct-to-console without layers (harder to test and maintain)

- **Data Management Alternatives:**
  - UUID strings for IDs (too complex for console app)
  - Random integers for IDs (potential collision issues)
  - Pure dictionary storage (would lose ordering)
  - Pure list storage (slow ID lookups)

- **Interface Alternatives:**
  - Command-line arguments only (less user-friendly)
  - Natural language processing (unnecessarily complex)
  - Interactive prompts without menu (less structured)

## Consequences
**Positive:**
- Clear separation of concerns makes code easier to test and maintain
- In-memory storage meets the requirement for no external databases
- Auto-incrementing IDs provide simplicity and user-friendliness
- Menu-driven interface provides clear user experience
- Layered architecture allows for easier future enhancements

**Negative:**
- In-memory storage means data is lost when application exits
- Layered architecture may be slightly more complex than a simple script
- Validation rules add some overhead to operations

## References
- specs/1-todo-app/plan.md
- specs/1-todo-app/research.md
- specs/1-todo-app/data-model.md