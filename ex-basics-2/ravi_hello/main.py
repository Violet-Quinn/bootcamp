from rich import print
import sys
from typing import Optional

def hello(name: Optional[str] = None) -> str:
    """
    Generate a greeting message.

    Args:
        name (Optional[str]): The name of the person to greet. 
            If None, defaults to "World".

    Returns:
        str: A formatted greeting message with rich text styling.
    """
    if name is None:
        name = "World"
    return f"Hello [bold blue]{name}[/bold blue]"

def main() -> None:
    """
    Entry point for the CLI application.

    Reads the name argument from the command line (if provided),
    generates a greeting using `hello()`, and prints it to the console.
    """
    name = sys.argv[1] if len(sys.argv) > 1 else None
    print(hello(name))

if __name__ == "__main__":
    main()

