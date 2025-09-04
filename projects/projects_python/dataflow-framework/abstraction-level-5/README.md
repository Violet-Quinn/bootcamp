# Level 5 – DAG Routing and Conditional Flows

---

## Task (abstraction-level-5)
So far, your pipeline has processed all lines the same way — each line goes through the same sequence of processors.
That works for uniform data, but real-world inputs are rarely that clean.

In this level, you will build a general-purpose DAG-based processing engine where each line can take a different path through the system based on its content or tags. This is a major abstraction step — you’re no longer just transforming lines, you're building a flexible routing system.

 What You’re Building
A general DAG-based processing engine where:
- Each processor is a node
- Processors yield tagged lines (e.g., ("errors", line))
- The engine uses routing rules to send lines to the right downstream node(s)
- You can define multiple paths in one config

___

## Solution
The pipeline is a Directed Acyclic Graph (DAG) of processing nodes (called processors). Each node processes input lines and yields output lines tagged with labels (tags). These tags determine how lines flow to downstream nodes according to routing rules defined in the YAML config.

Flow of the pipeline
1. Configuration (pipeline.yaml)
    - Defines nodes by name.
    - Each node specifies a processor function (like snake_case converter or uppercase converter).
    - Each node defines routing rules: for each tag, which downstream nodes receive that output.
2. Initialization
- Your code reads this YAML config.
- For each node:
        - Dynamically imports the processor function.
        - Creates a PipelineNode object for the node.
- Sets up downstream routing based on tags.
3. Identifying entry points
- Nodes with no incoming edges are marked as entry points.
- These entry points get the initial raw input lines.
4. Processing runs
- Maintains a queue of input lines for each node.
- Seeds input lines to entry nodes.
- For each node with queued input lines:
    - Feeds input lines (an iterator) to the node's processor function.
    - The processor yields (tag, line) pairs.
    - Looks up routing rules for the tag.
    - Routes the output line to all downstream nodes configured for that tag.
    - If no downstream node for the tag, line is collected as final output.
- This loop continues until no node has queued lines to process.
5. Yielding final output
- All lines that reach a tag with no downstream nodes are yielded as pipeline final output.