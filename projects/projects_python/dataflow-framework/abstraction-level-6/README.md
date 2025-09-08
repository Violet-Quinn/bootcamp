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
1. main.py
* Entry point CLI script using Typer.
* Accepts input file and optional config path.
* Instantiates the StateEngine with config.
* Runs the engine on the input lines.
* Prints the final output lines to the console.
* Supports optional graph visualization.

2. state_engine.py
* Core state routing engine.
* Loads YAML config defining processors and routing graph.
* Uses importlib to load processor functions dynamically.
* Builds the routing graph internally with networkx.DiGraph.
* Validates the graph for cycles and proper routing tags.
* Implements runtime run() that iteratively routes lines through processors based on tags, using a queue.
* Detects infinite loops with visit counting.
* Provides optional visualization method to display routing graph with arrows.

3. core.py
* Provides an alternative routing implementation using a DAG and queues.
* Builds internal routing queues for nodes.
* Routes lines through nodes according to routing rules.
* Can be adapted to use networkx for graph validation and visualization.

4. pipeline.py
* Implements a DAG-based pipeline (Level 5).
* Loads YAML config.
* Dynamically loads processors.
* Constructs PipelineNode instances and connects them according to routing.
* Runs pipeline in batch mode by passing lines from node to node.
* Different from StateEngine as routing is static graph without dynamic tags.

5. processor modules (e.g., start.py, filters.py, formatters.py, output.py, etc.)
* Contain individual processing units called by the state engine.
* Defined as callable functions taking an iterator of (tag, line) tuples.
* Perform filtering, tagging, formatting, output etc.
* Emit (tag, line) pairs for downstream routing.

Overall Flow of Execution:
* User runs CLI (main.py) with input file and config.
* StateEngine loads config, builds routing graph, loads processors.
* Input lines are tagged with start and seeded into the queue.
* Iteratively, for each (tag, line) pair:
    * The processor for tag processes the line.
    * Outputs are emitted as (next_tag, line) pairs.
    * Lines are queued to downstream processors per routing.
* Lines continue flowing through states until tagged with end and emitted as output.
* Visualization (optional) shows flow graph for debugging or understanding.
* Final lines printed/displayed as the system output.

Run:
python3 main.py --input test_input.txt --config pipeline.yaml --visualize
Or
python3 main.py --input test_input.txt --config pipeline.yaml
