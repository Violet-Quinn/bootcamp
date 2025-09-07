# Final Project Wrap-Up – Real-Time File Processing System
---

## Task (final-project)
You've now built a dynamic, observable, fault-tolerant, self-managing file processing system. In this final step, you'll polish your work, make it easier to run, and reflect on the architecture you've created.

Add a Makefile (or `run.sh`)
Create a Makefile that simplifies common operations like build-docker, run, build-package, publish-package, clean etc.
This helps others use your project immediately and supports both local and containerized runs.

Add Dual Execution Modes
Update your CLI or startup logic to support two modes:

1. Single File Mode
`python main.py --input somefile.txt`
Processes one file and exits.

2. Watch Mode
`python main.py --watch`
Continuously monitors the watch_dir/unprocessed/ folder and processes files as they appear.
Let the user choose mode via `--watch` or `--input`.


___

## Solution
Final Project Directory Structure and Roles:
final-project/
├── main.py                          # CLI entry point, starts folder monitor and dashboard
├── core.py
├── pipeline.py
├── requirements.txt
├── folder_monitor.py                # Core file watcher: monitors folders, manages file lifecycle, processes files, writes output
├── state_engine.py                 # Stateful tag-based routing engine for line processing pipeline (reused from Level 7)
├── processor_types.py              # Processor function type definitions (callable signature) (reused)
├── observability/
│   ├── shared_state.py             # Thread-safe shared metrics, errors, traces, and folder queue stats
│   ├── instrumentation.py          # Wrapping processors for metrics, tracing, error collection
│   ├── dashboard.py                # FastAPI dashboard server exposing metrics, traces, errors, plus folder queue endpoints
├── watch_dir/
│   ├── unprocessed/
│   ├── underprocess/
│   ├── processed/
├── test_inputs/
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
└── dockerfile

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

Usage:
Make it executable once:
```bash
chmod +x run.sh
```

Using the run.sh Script for Common Project Operations:
To streamline development and deployment, the project includes a `run.sh` shell script that simplifies common tasks and improves usability. Instead of running long or complex commands manually, simply execute predefined commands with `./run.sh`.

Provided Commands:
- install
Installs all required Python dependencies listed in requirements.txt.
Use:
```bash
./run.sh install
```

- build-docker
Builds a Docker image tagged dataflow-pipeline for containerized runs, packaging your entire app and dependencies.
Use:
```bash
./run.sh build-docker
```

- run
Starts the folder monitoring service with the observability dashboard enabled (default watch folder is watch_dir). This runs the core Level 8 pipeline in continuous mode.
Use:
```bash
./run.sh run
```

- clean
Cleans up compiled Python bytecode files (*.pyc) and __pycache__ directories to keep the repository tidy.
Use:
```bash
./run.sh clean
```

- help
Displays usage information about the available commands.


How to use:
Make the script executable (once):
```bash
chmod +x run.sh
```

Run any command, for example:
```bash
./run.sh install
./run.sh build-docker
./run.sh run
./run.sh clean
```

To run single file mode at container start, override the CMD:
```bash
docker run -it --rm -v /Users/yourname/data:/app dataflow-pipeline python3 main.py run --input /app/testfile.txt

```