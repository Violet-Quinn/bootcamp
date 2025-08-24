import sys
from typing import List, Optional

def main(argv: Optional[List[str]] = None) -> None:
    """
    Main entry point of the script.

    Args:
        argv (Optional[List[str]]): The list of command-line arguments.
                                   Defaults to sys.argv if None.

    Behavior:
        - If an argument is provided, it will be used as the name.
        - If no argument is provided, defaults to "world".
        - Prints a greeting to standard output.
    """
    if argv is None:
        argv = sys.argv
    name: str = argv[1] if len(argv) > 1 else "world"
    print(f"Hello {name}")



# if __name__ == "__main__":
#     main(sys.argv)
