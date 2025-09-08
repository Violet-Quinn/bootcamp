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
This script provides a simple command-line interface (CLI) built with Typer to process text files line by line. It offers configurable text transformations and output options.
How it works:
* Reads an input file specified with the `--input` (or `-i`) option.
* Transforms each line according to the selected mode:
    * uppercase (default or specified by `--mode` uppercase): converts lines to uppercase.
    * snakecase (specified by `--mode snakecase`): converts lines to lowercase and replaces spaces with underscores.
* Outputs the transformed lines:
    * To the console (standard output) by default.
    * To a file if the `--output` option is provided.
Usage Examples:
1. Basic usage (default uppercase transformation)
```bash
python process.py --input input.txt
```
2. Specify snakecase transformation
```bash
python process.py --input input.txt --mode snakecase
```
3. Write the output to a file
```bash
python process.py --input input.txt --output out.txt
```
Environment Variable Support
* The mode option defaults can be set via a `.env` file, making the behavior configurable without changing the command line.
* Example `.env` file content to default to snakecase mode:
```bash
MODE=snakecase
```
* The CLI option `--mode` overrides the `.env` default when specified.