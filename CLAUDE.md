# Todo In-Memory Python Console Application - AI Agent Instructions

## Overview
This document provides instructions for AI agents working on the Todo In-Memory Python Console Application. This is a console-based todo application that stores tasks in memory with full CRUD functionality (Add, View, Update, Delete) plus status management (Mark Complete/Incomplete).

## Project Structure
- `src/todo_app/` - Main application source code
  - `models/` - Data models (Task, TaskList, exceptions)
  - `services/` - Business logic (TaskService)
  - `cli/` - Console interface
  - `main.py` - Application entry point
- `tests/` - Test files
  - `unit/` - Unit tests
  - `integration/` - Integration tests

## Key Implementation Details
- Python 3.13+ syntax and standards must be followed
- All data is stored in memory (no persistent storage)
- Console-based interface only (no GUI or web front-end)
- App handles invalid inputs gracefully without crashing
- Tasks have: ID (auto-generated), Title, Description, Status (Complete/Incomplete)

## Task Model
- ID: Unique identifier (auto-incrementing integer)
- Title: Required, max 100 characters
- Description: Optional, max 500 characters
- Status: "Complete" or "Incomplete" (default: "Incomplete")

## Implementation Guidelines
- Follow clean architecture with separation of concerns (models, services, CLI)
- Implement proper validation for all inputs
- Provide clear error messages for invalid operations
- Use custom exceptions for business logic errors
- Include inline comments explaining complex logic
- Write unit tests for all business logic
- Implement menu-driven console interface

## Common Operations
- Add task: Create new task with title and description
- View tasks: Display all tasks with ID, title, description, and status
- Update task: Modify existing task title or description
- Delete task: Remove task by ID
- Mark complete/incomplete: Change task status by ID

## Error Handling
- Validate task titles (non-empty, max 100 chars)
- Validate task descriptions (max 500 chars)
- Validate task IDs (must exist in the system)
- Handle invalid menu selections gracefully
- Prevent duplicate task IDs

## Implementation Details
- Task model includes ID, title, description, and status fields with proper validation
- TaskList manages the collection of tasks with unique ID generation
- TaskService provides business logic layer with proper exception handling
- CLI interface provides menu-driven console interaction with input validation
- Custom exceptions for different error scenarios (TaskNotFoundError, TaskValidationError, etc.)
- Comprehensive unit and integration tests covering all functionality
- Input sanitization and validation at multiple levels (CLI, service, model)
- Consistent error messaging and user feedback