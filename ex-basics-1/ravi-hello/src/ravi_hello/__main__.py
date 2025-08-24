"""
Entry point module for running the main function.

This script executes the imported `main` function when run as
a standalone program. It is designed so that the functionality
can also be imported and reused without executing automatically.
"""

from . import main


if __name__ == "__main__":
    main()
