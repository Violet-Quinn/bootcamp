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
How Each File Works

1. main.py
Role: Entry point, runs the CLI app.
* This file is minimal.
* It simply imports the Typer CLI app from cli.py and calls app() if the script is run directly.
* It does not deal with any reading, writing, or processing.
* This keeps the project clean by isolating execution start here, separate from logic.

2. cli.py
Role: Command-line interface handler using Typer, manages user interactions.
* Defines the Typer app instance.
* Defines the main command (main) decorated with @app.callback(invoke_without_command=True) to make it the default command.
* Defines CLI options (--input, --output, --mode), reading mode from environment variables if unspecified.
* Handles file IO: reading lines from input file, writing processed lines to output or stdout.
* Converts the mode string to a list (supports multiple modes comma-separated).
* Build a list of processors for the pipeline from modes by calling build_pipeline from pipeline.py.
* Applies the processors to each input line by calling apply_processors from core.py.
* Orchestrates the complete flow but delegates actual computing logic to other modules.

3. core.py
Role: Implements text-processing logic and processor composition.
* Defines processor functions that transform lines (e.g., to_uppercase, to_snakecase).
* Each processor matches the common ProcessorFn signature: (str) -> str.
* Contains apply_processors, which takes a single line and applies all the processors in the pipeline sequentially.
* Centralizes all processing logic in one module, so adding or changing processors doesn’t affect CLI or pipeline.

4. pipeline.py
Role: Builds a list of processors based on modes.
* Responsible for translating mode names (strings like "uppercase", "snakecase") into actual processor functions defined in core.py.
* Returns a static pipeline (list) of processors for the given modes in order.
* Raises an error if an unsupported mode is passed.
* Encapsulates mode-to-processor mapping so the rest of the system calls this single entry point for pipeline construction.

5. types.py
Role: Defines type aliases and interfaces.
* Defines ProcessorFn as a type alias for a function signature (str) -> str.
* This creates a clear contract all processors must follow.
* Helps code readability, static analysis, and future extensibility with consistent processor interfaces.


## Usage
```bash
    python3 cli.py --input test_input.txt --mode uppercase --mode snakecase
```

Environment Variables
A default processing mode was set using an environment variable.
Create a .env file with following:
```bash
    MODE=snakecase,uppercase
```
Override it with the --mode option
