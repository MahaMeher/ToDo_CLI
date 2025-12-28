"""
Main entry point for the Todo In-Memory Python Console Application.

This module serves as the application entry point and runs the main CLI loop.
"""
from .cli.interface import CLIInterface


def main():
    """Main application entry point."""
    print("Starting Todo Application...")
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()