# Level 2 – Modular Structure and Standardized Processing

---

## Task (abstraction-level-2)
1. Split your code into the following modules:
```bash
    abstraction-level-2/
    ├── main.py         # Reads input, writes output
    ├── cli.py          # Handles CLI via typer
    ├── core.py         # Applies a list of processors to each line
    ├── pipeline.py     # Assembles the processor list based on mode
    └── types.py        # Defines ProcessorFn types
```
2. Define a common function signature for processors
3. Implement these processors in `core.py`:
    - `to_uppercase(line: str) -> str`
    - `to_snakecase(line: str) -> str`
4. Create a list of processors in `pipeline.py`. Pay attention to the mode. This is a static pipeline.
5. Apply all processors in sequence to each line of input.
6. CLI should stay the same as Level 1, with `--input`, `--output`, and `--mode`.

---

## Supported Modes
- `uppercase`: convert each line to uppercase
- `snakecase`: replace spaces in each line with underscores and convert to lowercase
Implement both using basic string operations. Choose the behavior based on the selected mode.

---

## Solution
How it works:
- Reads an input text file specified by `--input`.
- Builds a static pipeline of processor functions based on the selected `--mode`.
- Applies all processors sequentially on every input line.
- Outputs results either to the console (default) or to a specified output file (`--output`).

## Usage
All commands use python -m cli to run the CLI package.
1. Default usage (uppercase transform):
```bash
    python3 -m cli --input test_input.txt
```
2. Specify transformation mode(`snakecase`):
```bash
    python3 -m cli --input test_input.txt --mode snakecase
```
3. Save results to a file:
```bash
    python -m cli --input test_input.txt --output test_output.txt
```

Environment Variables
A default processing mode was set using an environment variable.
Create a .env file with following:
```bash
    MODE=snakecase
```
Override it with the --mode option

Notes:
    - Your project folder must contain an `__init__.py` file to be recognized as a package.