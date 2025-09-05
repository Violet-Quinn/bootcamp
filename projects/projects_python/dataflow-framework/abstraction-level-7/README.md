# Level 7 – Observability and System Introspection

---

## Task (abstraction-level-7)
In this level, you will add real-time observability to your processing system. You’ve built a powerful, dynamic engine — but now it’s time to make it transparent, measurable, and understandable.

This means:
- Capturing metrics and internal state
- Tracing the journey of lines through the system
- Displaying all of this live on a simple web dashboard
Your goal is to operate the system like a real one — not just build it.

Core Features
1. Metrics Layer
- Count of lines received and emitted per processor
- Processing time per processor
- Number of exceptions or retries
2. Execution Tracing
- Each line optionally carries a trace of its journey (e.g., ["start", "warn", "end"])
- Traces stored for a recent window (e.g., last 1000 lines)
- Optional --trace flag enables this
3. Web Dashboard
- Built using FastAPI
- Runs on a separate thread while processing continues
- Exposes endpoints:
    - `/stats`: live processor metrics
    - `/trace`: recent traces (e.g. top 100)
    - `/errors`: processor-level error logs
- Frontend may be plain JSON for now, or enhanced with simple HTML/JS
4. Concurrency Design
- The dashboard reads from shared memory structures (dicts, counters)
- Use `threading` and locks if needed
- Keep your system responsive

Task
1. Add a metrics and tracing layer to your engine
2. Create a background thread that runs a FastAPI server
3. Provide at least 3 live endpoints:
    - `/stats` → { processor_name: { count, time, errors } }
    - `/trace` → last N line traces
    - `/errors` → recent errors with processor and message
4. Allow users to toggle tracing from the command line
5. Ensure your system remains responsive and consistent under load
___

## Solution
This level builds a state-machine-based dataflow pipeline for text processing, with observability (metrics, tracing, errors) and a live dashboard via FastAPI. The pipeline is dynamically configured and routes lines between processors based on tags.

Directory Structure & Roles
- main.py: CLI entry point. Runs the pipeline in either DAG or state-machine mode, with optional tracing/dashboard.
- pipeline_state.yaml: Configures the state-machine pipeline: tags, processor functions, routing.
- pipeline.py: Implements DAG pipeline logic (not used in state mode, but available).
- core.py: Contains a generic DAG routing function (not used directly in this level).
- processor_types.py: Defines the processor function type signature.
- state_engine.py: Implements the state-machine routing engine, with observability hooks.
- test_input.txt: Example input file for pipeline runs.
- observability/: Implements metrics, tracing, error logging, and the FastAPI dashboard.
- processors/: Contains all processor functions (transformers, filters, output, etc.).

Summary
- Intent: Build a dynamic, observable, state-machine-based text processing pipeline.
- Flow: CLI → config → state engine → processors → output, with live metrics/tracing/errors via dashboard.
- Extensibility: Add new processors or change routing by editing config, not code.
