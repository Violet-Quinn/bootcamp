# Level 5 – DAG Routing and Conditional Flows

---

## Task (abstraction-level-5)
So far, your pipeline has processed all lines the same way — each line goes through the same sequence of processors.

That works for uniform data, but real-world inputs are rarely that clean.

In this level, you will build a general-purpose DAG-based processing engine where each line can take a different path through the system based on its content or tags. This is a major abstraction step — you’re no longer just transforming lines, you're building a flexible routing system.

Desired Flow
1. All lines go through a trim processor.
2. Each line is tagged by tag_error or tag_warn (adds routing info).
    * A generic splitter sends lines to different branches:
    * errors → count and archive
    * warnings → tally
    * general → format and print
Now you need a system where:
* Processors can tag their output
* The engine routes based on tags
* You define all routing behavior in a config file

A general DAG-based processing engine where:
* Each processor is a node
* Processors yield tagged lines (e.g., ("errors", line))
* The engine uses routing rules to send lines to the right downstream node(s)
* You can define multiple paths in one config

---

## Solution
Execution Flow
1. CLI Input: The command-line interface accepts:
    * Input file path
    * Output path (optional)
    * DAG pipeline config YAML path
    * Start node name (entry point in DAG)
2. Reading Input Lines: Lines from the input file are read one-by-one and initially tagged with None (or a default tag).
3. Loading DAG Pipeline:
    * The YAML config is parsed.
    * Each node defines a processor by its dotted import path.
    * Processors are dynamically imported and instantiated.
    * Routes map tags emitted by one node to downstream node names.
4. DAG Engine Initialization: The DAGEngine is instantiated with the processors dictionary and the routing rules dictionary.
5. Processing Start:
    * The engine begins with the start node.
    * Lines tagged with None are passed to the start node's processor.
6. Iterative Processing:
    * The engine maintains a queue of (current_node, lines) tuples to process.
    * For each dequeued node, its processor is called with the input tagged lines.
    * The processor yields tagged output lines (tag, line).
7. Routing of Output Lines:
    * For each output tagged line, the routing dictionary is consulted.
    * Lines are assigned to one or more downstream nodes based on their tag.
    * If a tag doesn’t map downstream, the line is considered terminal output.
    * Downstream nodes and their input lines are queued for further processing.
8. Completion:
    * When the queue is empty, the accumulated terminal output lines are returned.
    * The CLI writes these lines to a file or prints to stdout.

Run:
uv run main.py --input test_input.txt --config pipeline.yaml --start-node joiner