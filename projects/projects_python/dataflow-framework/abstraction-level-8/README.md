# Level 8 – Automated Folder Monitor and Recovery

---

## Task (abstraction-level-8)
Turn your file processing tool into a self-running, fault-tolerant system.

Instead of processing a single input file, your system should now:
- Continuously monitor a folder for new files
- Process each file using your existing streaming/tag-routing engine
- Recover and retry automatically if the system crashes or is restarted
This mimics how real-world ingestion services and ETL daemons work — autonomously, robustly, and safely.

Task:
1. Implement the folder queue structure
2. At startup, move all files from underprocess/ back to unprocessed/
3. Continuously monitor unprocessed/:
    - When a new file appears:
        - Move to underprocess/
        - Process it line by line through your system
        - Move to processed/ when done
4. Update your dashboard to show:
    - Number of files in each folder
    - Name of the file currently being processed
    - Last N processed files and timestamps


___

## Solution
Level 8 Directory Structure and Roles:
abstraction-level-8/
├── main.py                          # CLI entry point, starts folder monitor and dashboard
├── folder_monitor.py                # Core file watcher: monitors folders, manages file lifecycle, processes files, writes output
├── state_engine.py                 # Stateful tag-based routing engine for line processing pipeline (reused from Level 7)
├── processor_types.py              # Processor function type definitions (callable signature) (reused)
├── observability/
│   ├── shared_state.py             # Thread-safe shared metrics, errors, traces, and folder queue stats
│   ├── instrumentation.py          # Wrapping processors for metrics, tracing, error collection
│   ├── dashboard.py                # FastAPI dashboard server exposing metrics, traces, errors, plus folder queue endpoints
├── processors/                     # Pure text-line processor functions (transforms only; one output line per input)
│   ├── filters.py                  # Filter processors like only_error, only_warn
│   ├── join_pairs.py               # Stateful processor joining line pairs
│   ├── line_count.py               # Stateful processor counting lines
│   ├── output.py                   # Final output processor that prints lines (used for "end")
│   ├── snake.py                   # Snake case formatter (replaces formatters.py)
│   ├── start.py                   # Start node processor: tags lines (error, warn, general)
│   ├── upper.py                   # Uppercase processing (optional)
├── pipeline_state.yaml             # YAML config defining nodes (tags) and their processor functions
├── utils.py                       # Utility functions like atomic file moves, timestamp helpers
└── test_input.txt                  # Example input file for testing the pipeline

How It Works:
1. Startup
    - main.py is started from the command line, with options to specify the --watch-dir and enable tracing/dashboard.
    - It creates a shared observability state instance (SharedState) used to collect runtime metrics, traces, errors, and folder queue stats.
    - It launches the FastAPI dashboard (on separate thread) for live monitoring.
    - It creates and runs an instance of FolderMonitor, passing it the shared state and trace flag.
2. Folder Monitor Initialization
    - The FolderMonitor class initializes by creating a directory structure under the given watch_dir:
        - unprocessed/: for new files awaiting processing.
        - underprocess/: for files currently being processed.
        - processed/: for files successfully processed.
    - On startup, the monitor runs _recover_incomplete_files() to move any files left in underprocess back to unprocessed so they can be retried—providing fault tolerance and recovery from crashes.
3. File Monitoring Loop
    - The monitor runs indefinitely (run_forever()).
    - It polls unprocessed/ folder regularly (e.g., every second).
    - When it detects files, it atomically moves each file from unprocessed/ to underprocess/ to claim ownership for processing.
    - It updates observability state with current folder counts and current file processing info.
4. File Processing
    - The monitor reads all lines from the file (skipping blank lines).
    - It calls the StateEngine.run(lines) method, which drives the state-machine pipeline using the YAML-configured processors.
    - The state engine routes lines between processors based on tags, handles branching/fan-out, and collects observability data (metrics, tracing).
    - Processors in the processors/ folder perform line transformations (e.g., tagging, filtering, formatting).
    - The final output lines are collected after the pipeline run.
5. Saving Processed Files
    - After processing, the monitor writes the output lines back as a new file with the same filename into processed/, overwriting or replacing the old content.
    - The patrol removes the old file from underprocess/.
    - It updates the processed file history with timestamps in shared observability state.
6. Observability
    - Metrics, traces, error logs are recorded per processor and overall.
    - Folder counts (unprocessed, underprocess, processed), the current file being processed, and recent processed file history are also stored in shared state.
    - The FastAPI dashboard at http://localhost:8000 exposes REST API endpoints to view real-time metrics and file queue states.
7. Fault Tolerance
    - If the system crashes or is killed during processing:
        - On restart, the folder monitor moves any files left in underprocess back to unprocessed.
        - This guarantees idempotent retry and no stuck files.
    - File atomic moves and locking ensure no partial or concurrent processing occurs.
    - The infinite loop recovers from transient errors and keeps running indefinitely.


Run:
`python3 main.py --watch-dir watch_dir --trace`