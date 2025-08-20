from rich import print
import sys
from typing import Optional

def hello(name: Optional[str] = None) -> str:
    if name is None:
        name = "World"
    return f"Hello [bold blue]{name}[/bold blue]"

def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else None
    print(hello(name))

if __name__ == "__main__":
    main()
