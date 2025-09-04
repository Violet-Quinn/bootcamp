# Level 4 – Stream Processing and State

---

## Task (abstraction-level-4)
In this level, you will move from simple str -> str functions to full stream-based processing. This opens the door to much more powerful behaviors, including:

- Returning multiple lines from one line (fan-out)
- Combining multiple lines into one output (fan-in)
- Stateful processing (e.g. counters, buffers, aggregators)
- More modular and lifecycle-aware processors
Problem Context:
The current `str -> str` processors are limited:
- They can’t drop lines easily.
- They can’t emit zero or multiple lines.
- They can’t maintain state across lines.
To build a real-world pipeline, we need processors that operate on streams — meaning, they take an iterator of lines and yield processed output lines one by one.

You will:
- Redesign your processor interface to be Iterator[str] -> Iterator[str]
- Convert your simple processors using a decorator or wrapper so you can still reuse existing ones
- Build at least one processor that requires internal state (e.g., line counting)

Requirements:
1. Redesign the processor interface: Each processor now works on a stream.
2. Write a stream-aware processor that performs one of the following:
    - Keeps a count of how many lines it has seen and emits that count with the line
    - Joins every two lines into one (fan-in)
    - Splits lines on a delimiter and emits multiple lines (fan-out)
3. Introduce a processor with initialization/configuration: It should be initialized with options that affect how it behaves. Think about how to separate configuration from processing logic.
4. Support processors that maintain internal state: For example, a counter, buffer, or matcher. You may use class-based processors to manage this state.
5. Do not change your config format yet — just adapt your pipeline to use the new streaming interface.

---

## Solution
This project is a configurable text processing pipeline. It reads lines from an input file, processes them using a sequence of functions (processors), and writes the results to an output file or prints them.

How it works (step by step):
1. Configuration
The pipeline steps are defined in pipeline.yaml. Each step is a processor function specified by its import path (e.g., processors.line_count.LineCountProcessor).

2. CLI Entry Point
You run the program using the CLI in cli.py, providing the input file, output file (optional), and config file.

3. Pipeline Building
The function build_pipeline reads the YAML config and dynamically loads each processor function/class.

4. Reading Input
`read_lines` reads lines from the input file.

5. Processing
`apply_processors` applies each processor to the lines in sequence.

Some processors work on each line (e.g., uppercase).
Some work on the whole stream (e.g., joining pairs of lines, counting lines).
6. Writing Output
`write_output` writes the processed lines to the output file or prints them.

You can easily add new processors and change the pipeline by editing `pipeline.yaml` without changing the main code.