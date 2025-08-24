# ex-basics-2

---

## Task (ex-basics-2)
Enhance the application with the following:

1. Install the following modules in your environment from pypi: `rich`
2. Enhance your code to use rich to print rich message.

---

## Solution
1. Go to the folder where you want your project.
2. Create the package project using:
    ```bash
    uv init --package ravi-hello
    ```
    This will create the directory and the necessary files.
3. Install `rich`:
```bash
    uv add rich
```
4. Write the hello module code(__init__.py):
```bash
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
```
5. Add a __main__.py
    `uv run` doesn't run a bare package folder name as a command unless the command is registered or a script is specified. You need either a script file, a `__main__.py`, or registered CLI commands for `uv run` to work as expected.
```bash
    """
    Entry point module for running the main function.

    This script executes the imported `main` function when run as
    a standalone program. It is designed so that the functionality
    can also be imported and reused without executing automatically.
    """

    from . import main


    if __name__ == "__main__":
        main()
```
6. Add an entry point in `pyproject.toml` to map a command to a callable inside the package, like:
```bash
    [project.scripts]
    ravi-hello = "ravi_hello:main"
    ravi_hello = "ravi_hello:main" #optional
```
7. Test your code:
    Run it using uv run from your project root:
```bash
    uv run ravi-hello
```

---
