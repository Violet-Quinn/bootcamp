# ex-basics-1

---

## Task (ex-basics-1)
Setup of application
1. Initialize an application for use with uv (uv init)
2. Create a virtual environment uv venv and source it.
3. Start your IDE in this environment
4. Setup your IDE to use the virtual environment you setup.
5. Create a module called <yourname>-hello in that folder.
6. Write the code that says hello to the argument passed or world, by default.
7. Publish the module in TestPyPI for Package Testing.
In your readme, please provide the link to the package. Also, do the readme.md well enough so that the package page looks good.

---

## Solution
1. Go to the folder where you want your project.
2. Create the package project using:
    ```bash
    uv init --package ravi-hello
    ```
    This will create the directory and the necessary files.
3. Write the hello module code(__init__.py):
    ```bash
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
    ```
4. Add a __main__.py
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
5. Add an entry point in `pyproject.toml` to map a command to a callable inside the package, like:
    ```bash
    [project.scripts]
    ravi-hello = "ravi_hello:main"
    ravi_hello = "ravi_hello:main" #optional
    ```
6. Test your code:
    Run it using uv run from your project root:
```bash
    uv run ravi-hello
```
7. Build your project:
    Update your project’s `pyproject.toml` and uv settings to specify TestPyPI as your upload target. You can then build:
```bash
    uv build
```
8. Create a file named `.pypirc` in your home directory with contents like this:
    ```bash
    [distutils]
    index-servers =
    pypi
    testpypi

    [pypi]
    username = your-username
    password = your-password-or-api-token

    [testpypi]
    repository = https://test.pypi.org/legacy/
    username = your-username
    password = your-password-or-api-token
    ```
9. Publish it:
```bash
    uvx uv-publish
```
10. Test your package published on TestPyPI and verify that when you run it with an argument like x it outputs hello x, you can do the following with uv:
```bash
        uv run --with ravi-hello --no-project -- ravi-hello x
```

## Package Link
[https://test.pypi.org/project/ravi-hello/](https://test.pypi.org/project/ravi-hello/)

---
