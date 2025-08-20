# ravi-hello (ex-basics-3)

`ravi-hello` is a simple Python CLI tool that greets a user by name or defaults to “world” if no name is provided.  

---
## Implementation of `rich`

The Python rich library is used to make your terminal or console output more visually appealing and easier to understand by adding color, style, and formatting features.

## Implementation of `typer`

Typer is a modern Python library designed for building command-line interface (CLI) applications quickly and easily. It leverages Python’s type hints, which means for very little code, fully featured CLI tools with automatic help messages, argument parsing, and validation can be achieved.

## Features

- Simple CLI to say hello to any name  
- Defaults to greeting "world" if no name argument passed  
- Lightweight and minimal dependency  
- Uses Python’s built-in argument handling  

---

## Installation

To install typer:
```bash
uv pip install typer
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

Testing and Using ravi-hello

Step 1: Install

```bash
uv pip install -e .
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
## Recording with Asciinema

Asciinema is a tool that lets you record and share terminal sessions as lightweight, text-based “casts” that can be embedded into documentation or viewed online.

Install asciinema:
```bash
sudo apt install asciinema
```
or
```bash
pip install asciinema
```

Record a session

To record a terminal session:
```bash
asciinema rec
```

This will start recording everything you type and see in the terminal.
Run your commands as usual.

When you’re done, exit the recording by pressing:

```Ctrl+D```
or type exit