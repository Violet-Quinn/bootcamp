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
What Each File Does
* types.py: Defines the updated processor function type as Callable[[Iterator[str]], Iterator[str]].
* core.py: Provides functions to sequentially apply streaming processors to input lines and a decorator to adapt old-style line processors.
* processors/: Contains processor implementations:
    * Simple stateless ones like snakecase, uppercase adapted for streaming.
    * Stateful ones such as LineCounter and JoinEveryTwoLines demonstrating state and fan-in/fan-out behaviors.
* pipeline.py: Loads pipeline config YAML, dynamically imports processors by dotted path, instantiates classes, and wraps simple functions for streaming compatibility.
* cli.py: Handles command-line interface, reads input lines, loads the dynamic streaming pipeline, applies processors in order, and writes output.
* main.py: Entry point that imports app from cli.py and runs the Typer CLI app.

Flow of Execution
1. User runs CLI
2. main.py calls app() from cli.py, triggering Typer.
3. cli.py:
    * Reads input.txt line by line as a stream.
    * Loads processors dynamically based on YAML config in pipeline.py.
    * Applies processors sequentially to the input stream using core.py utilities.
    * Writes the final transformed lines to output.
4. In pipeline.py:
    * YAML is parsed.
    * Processor functions/classes are dynamically imported.
    * Classes are instantiated; simple functions wrapped for streaming compatibility.
5. Each processor:
    * Receives an iterator of lines.
    * Yields processed output lines, optionally maintaining state or buffering lines.
6. Output is streamed to console or output file as configured.

Run:
uv run cli.py --input test_input.txt --config pipeline.yaml