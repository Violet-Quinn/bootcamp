
from rich import print
import typer
from typing import Optional

app = typer.Typer()

def hello(name: Optional[str] = None) -> str:
    """
    Return a formatted greeting message.

    Args:
        name (Optional[str]): The name of the person to greet. 
            If not provided, defaults to "World".

    Returns:
        str: A greeting message with rich formatting.
    """
    if name is None:
        name = "World"
    return f"Hello [bold blue]{name}[/bold blue]"

@app.command()
def hello_command(name: Optional[str] = typer.Argument(None, help="Name to greet")) -> None:
    """
    Print a greeting message to the console.

    This function is exposed as a CLI command via Typer.

    Args:
        name (Optional[str]): The name of the person to greet. 
            If not provided, defaults to "World".
    """
    print(hello(name))

def main() -> None:
    """
    Entry point for the Typer application.

    Runs the CLI app, enabling the `hello-command`.
    """
    app()

if __name__ == "__main__":
    main()
