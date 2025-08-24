# ex-basics-3

---

## Task (ex-basics-3)
Writing command line application
1. Install typer
2. Use it to write a command line application in the module
3. Now, make the cli app as a part of the pyproject.toml so that it gets installed when we install the package.
4. Record and show the demo where you install the package and run the command and show it.

---

## Solution
1. Go to the folder where you want your project.
2. Create the package project using:
    ```bash
    uv init --package ravi-hello
    ```
    This will create the directory and the necessary files.
3. Install `rich` and `typer`:
```bash
    uv add rich typer
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
8. Record the demo using asciinema
```bash
    asciinema rec demo.cast
    ravi-hello Alex
    exit
```
9. Playing Recording
    demo.cast location: `bootcamp/ex-basics-3/ravi-hello/demo.cast`
    You can play the recording using:
```bash
    asciinema play demo.cast
```
Note: There was some error while uploading the recording:
    ultraviolet@Altars-MacBook-Air ravi-hello % asciinema upload demo.cast      
    asciinema: upload failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1020)>
    asciinema: retry later by running: asciinema upload demo.cast

---
