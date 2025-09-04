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
This project implements a fully dynamic, config-driven text processing pipeline. Users specify the sequence of processing steps in [`pipeline.yaml`](pipeline.yaml) using dotted import paths for processor functions. The pipeline is built at runtime by loading each processor dynamically.

How it works:
- The CLI (`cli.py`) accepts `--input`, `--output`, and `--config` (YAML) arguments.
- The pipeline configuration is parsed from [`pipeline.yaml`](pipeline.yaml) via [`build_pipeline`](pipeline.py).
- Each processor function is loaded dynamically using Python’s import system.
- Input lines are read from the specified file, processed sequentially by all pipeline steps, and written to the output file or printed to the console.

Example pipeline.yaml:
```yaml
pipeline:
  - type: processors.snake.to_snakecase
  - type: processors.upper.to_uppercase
```

Usage:
```bash
python3 -m cli --input test_input.txt --config pipeline.yaml
python3 -m cli --input test_input.txt --output result.txt --config pipeline.yaml
```

Extensibility: 
To add new processors, simply create new functions in the [`processors/`](processors/) directory and reference them in [`pipeline.yaml`](pipeline.yaml) without modifying the main codebase.

Notes:
    - Your project folder must contain an `__init__.py` file to be recognized as a package.