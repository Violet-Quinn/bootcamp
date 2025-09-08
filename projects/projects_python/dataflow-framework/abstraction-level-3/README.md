# Level 3 – Dynamic Config-Driven Pipeline

---

## Task (abstraction-level-3)
In this level, your task is to fully decouple pipeline logic from code. You'll allow users to specify their desired line-processing steps via a configuration file, using dotted import paths to dynamically load the processor functions at runtime.

This unlocks extensibility: users can create and reuse their own processors without changing your program’s source code.

1. Create a `pipeline.yaml` file that defines the processing steps using import paths:
```bash
    pipeline:
        - type: processors.snake.to_snakecase
        - type: processors.upper.to_uppercase
```
2. Write a function that:
- Parses the config file
- Loads each function dynamically from its import path
- Returns a list of ProcessorFn functions
3. Replace your static pipeline from Level 2 with this dynamic list.
4. Update your CLI to accept --config pipeline.yaml instead of --mode.

Expected Structure
You should now have at least:
```bash
    abstraction-level-3/
    ├── main.py
    ├── cli.py
    ├── core.py
    ├── pipeline.py         # now loads pipeline from YAML
    ├── types.py
    ├── processors/
    │   ├── upper.py
    │   └── snake.py
    └── pipeline.yaml
```


---

## Solution
Level 3 advances beyond static pipelines by fully decoupling the pipeline configuration from source code

processors/upper.py and processors/snake.py
* These modules each contain a single processor function (to_uppercase and to_snakecase respectively).
* They are referenced via dotted paths in the YAML config.
* This modular design allows users to add their own processor modules and functions anywhere in the import path.

pipeline.yaml
* A YAML configuration file containing the pipeline definition.
* Each step specifies a processor by its full dotted import path as the type value.
* This file replaces the static pipeline logic from Level 2.

types.py
* Defines a type alias ProcessorFn which is a function from str to str.
* This creates a clear contract for all processors, improving readability and type-safety.

core.py
* Contains the function apply_processors that sequentially applies a list of processor functions to a single input line.
* This repeats for every line read from input.
* Processing logic itself remains centralized and reusable.

pipeline.py
* Contains load_pipeline_from_config which:
    * Opens and reads the YAML config file.
    * Parses the pipeline steps.
    * Uses a helper load_function that dynamically imports the processor function using Python's importlib and the dotted path string.
* Returns a dynamically loaded list of processor functions to be used in the pipeline.
* This is the core of config-driven dynamic pipeline loading.

cli.py
* Defines the command-line interface using Typer.
* Accepts --input for input file, --output for optional output file, and --config for YAML config path (defaulting to pipeline.yaml).
* Reads input lines from the input file.
* Uses pipeline.load_pipeline_from_config to dynamically obtain the processor pipeline from the YAML config.
* Applies all processors sequentially on every input line via core.apply_processors.
* Writes the transformed lines to output or standard output.
* Acts as the orchestrator connecting CLI, dynamic pipeline loading, and processing.

main.py
* The simplest file: just imports the Typer app from cli.py and runs it if executed as a script.
* Acts as clean entry point, separating startup from logic.

How Level 3 Works
1. User executes the CLI 
2. main.py loads and runs Typer CLI app from cli.py.
3. cli.py reads the input file, loads processor functions dynamically according to pipeline.yaml using pipeline.py.
4. For each line, core.py applies all processors in order.
5. Outputs transformed lines to file or console.
6. The entire processing pipeline is configurable via YAML without any source code changes.
7. New processors can be added by creating new functions and referencing them by import path in pipeline.yaml.

Run:
python3 main.py --input test_input.txt --config pipeline.yaml
