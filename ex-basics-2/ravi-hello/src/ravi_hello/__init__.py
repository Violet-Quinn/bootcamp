import sys
from typing import List, Optional
from rich import print  # rich's print supports colors and styles

def main(argv: Optional[List[str]] = None) -> None:
    """
    Main entry point of the script.

    Args:
        argv (Optional[List[str]]): Command-line argument list; defaults to sys.argv.

    Prints a greeting, using rich for colored output.
    """
    if argv is None:
        argv = sys.argv

    name: str = argv[1] if len(argv) > 1 else "world"
    print(f"Hello [bold green]{name}[/bold green]")
