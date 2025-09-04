# Level 1 – Parameters and CLI Interface

---

## Task (abstraction-level-1)
Refactor your script to:
Use `typer` to define a command-line interface
Accept:
- `--input`: input file path (required)
- `--output`: output file path (optional)
- `--mode`: processing mode (optional, defaults via `.env`)
- Load default values (in this case mode) from a `.env` file using `python-dotenv`
- Implement different processing behaviors based on the mode

---

## Supported Modes
- `uppercase`: convert each line to uppercase
- `snakecase`: replace spaces in each line with underscores and convert to lowercase
Implement both using basic string operations. Choose the behavior based on the selected mode.

---

## Solution
This script provides a simple command-line interface built with Typer to process text files line by line. It allows you to transform text into different formats (uppercase or snake_case) and write the output either to the console or to a file.

How it works:
- Read an input text file using --input (or -i)

- Transform each line into:
    Uppercase (default or --mode uppercase)
    Snake case (via --mode snakecase)

- Output results to:
    Console (stdout) (default)
    A file using --output

## Usage
1. Basic usage (default uppercase transform)
```bash
    python process.py --input input.txt
```
2. Specify transformation mode
```bash
    python process.py --input input.txt --mode snakecase
```
3. Save results to a file
```bash
    python process.py --input input.txt --output out.txt
```
Environment Variables
A default processing mode was set using an environment variable.
Create a .env file with following:
```bash
    MODE=snakecase
```
Override it with the --mode option