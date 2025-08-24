"""
Entry point module for running the Typer CLI application.

This script executes the imported `app` (Typer instance) when run as a standalone program.
"""

from . import app

if __name__ == "__main__":
    app()
