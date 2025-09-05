# Level 6 – State-Based Routing System

---

## Task (abstraction-level-6)
In this level, you'll move beyond pipelines and DAGs to build a general-purpose state transition engine.
Instead of wiring processors in a fixed sequence, you will design a system where each line carries tags — and those tags determine which processors it flows through next.
This system behaves like a state machine or a router, where processors are states, transitions are tag-based, and routing is dynamic and potentially cyclic.

Core Ideas:
1. Lines enter the system tagged with 'start'
2. Each processor is registered under a tag name
3. When a processor receives a line, it:
    - Processes it
    - Emits (tag, line) pairs for the next steps
4. If a line is tagged 'end', it exits the system
5. Multiple tags → multiple downstream processors (fan-out)
6. The same tag may be reached from multiple places (fan-in)
7. The system does not assume acyclicity

Task:
1. Build a routing engine where:
    - Processors are registered under tag names
    - Each processor receives (tag, line) inputs
    - Each processor yields (tag, line) outputs
2. Start with a single 'start' node
3. Stop when the tag 'end' is emitted
4. Use a config file to define:
    - Available processors
    - The mapping from tags to processor modules
5. Use networkx internally to simulate and visualize flow (optional but encouraged)
___

## Solution
- The project is a text processing pipeline. It reads lines from an input file (test_input.txt), processes each line through a series of steps, and produces output.
- The processing steps and their connections are defined in a config file (pipeline_state.yaml).
- The main logic is in `state_engine.py`, which acts as a state machine: each line is routed through different processors based on its type (error, warning, general, etc.).

Flow of the Code
1. Read Input
    - The CLI in main.py reads lines from test_input.txt.
2. Load Pipeline Configuration
    - The pipeline config (pipeline_state.yaml) lists all processors and how lines should flow between them.
3. Initialize State Engine
    - `StateEngine` loads the processors dynamically (using Python imports) and sets up the routing.
4. Process Each Line
    - All lines start at the "start" processor (processors/start.py), which tags each line as "error", "warn", or "general" based on its content.
    - Depending on the tag, the line is sent to the corresponding processor:
        - "error" → processors/filters.py (only_error)
        - "warn" → processors/filters.py (only_warn)
        - "general" → processors/formatters.py (snake)
    - Each processor transforms the line and passes it to the "end" processor (processors/output.py), which prints the final output.
5. Output Generation
    - The "end" processor prints each final line with a FINAL: prefix and yields it as output.
    - All processed lines are collected and displayed.

Summary:
- Input lines are classified and routed through different processors.
- Processors transform lines based on their type.
- Output is printed after all processing steps.
You can see the routing and processor definitions in pipeline_state.yaml, and the processor logic in the processors/ folder.