# ravi-hello

`ravi-hello` is a simple Python CLI tool that greets a user by name or defaults to “world” if no name is provided.  

---

## Link
[https://test.pypi.org/project/ravi-hello/](https://test.pypi.org/project/ravi-hello/)

## Features

- Simple CLI to say hello to any name  
- Defaults to greeting "world" if no name argument passed  
- Lightweight and minimal dependency  
- Uses Python’s built-in argument handling  

---

## Installation

Install the package from TestPyPI (the Python package testing repository):
```bash
uv pip install -i https://test.pypi.org/simple/ ravi-hello
```

---

## Usage

Once installed, use the `ravi-hello` command from your terminal:

```bash
uv run ravi-hello ravi
```
This command will output:
Hello ravi
If you run the command without an argument:

```bash
uv run ravi-hello
```

It defaults to:
Hello world

---

## Development

To test locally:

1. Clone the repository.
2. Create a Python virtual environment:

```bash
uv venv .venv
source .venv/bin/activate
```


3. Install dependencies (if any) and package in editable mode:

```bash
uv tool install . -e
```

4. Run and test commands directly from your development environment.

---

Testing and Using ravi-hello from TestPyPI

You can install and test the package directly from TestPyPI.
Step 1: Install from TestPyPI

Run this command to install your package from the TestPyPI repository:

```bash
uv pip install -i https://test.pypi.org/simple/ ravi-hello
```

Step 2: Use the CLI Tool

After installation, you can run the ravi-hello command in your terminal:

```bash
uv run ravi-hello ravi
```

This should output:

Hello ravi

If you run it without an argument:

```bash
uv run ravi-hello
```

It outputs the default:

Hello world

---
