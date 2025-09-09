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
Key Files and Their Roles
1. main.py
* Entry point of the system and CLI interface.
* Supports dual execution modes:
    * Single File Mode: Processes one specified file and exits.
    * Watch Mode: Monitors a folder for new files continuously.
* Initializes the StateEngine that manages processing pipelines, routing, and metrics.
* Starts the FolderMonitor in watch mode on a background thread.
* Starts the FastAPI dashboard server exposing REST APIs and frontend UI.
* Uses typer to parse CLI commands and options.
2. folder_monitor.py
* Watches a configured directory structure:
    * unprocessed/ for incoming files,
    * underprocess/ for files being processed,
    * processed/ for completed files.
* Moves files through these folders as it processes them.
* For each file, reads lines and calls StateEngine to process data.
* Updates metrics and collects errors/traces.
* Enables fault-tolerant, real-time file ingestion.
3. state_engine.py
* Contains the core processing pipeline logic.
* Loads pipeline configuration from YAML (pipeline.yaml).
* Manages a graph of processing nodes and routing steps.
* Processes input lines by passing through various processors.
* Records metrics (counts, times, errors), event traces, and error logs.
* Thread-safe for concurrent access by monitor and dashboard.
4. dashboard.py
* Defines FastAPI endpoints to provide observability data:
    * /api/stats - processor metrics summary.
    * /api/trace - recent line traces through pipeline.
    * /api/errors - recent errors.
* Serves the frontend UI (HTML+JS) displaying metrics, traces, errors.
* Provides auto-refreshing, real-time dashboard visualization.
* Uses CORS middleware for flexible access.
5. Frontend (static/index.html + CSS/JS)
* Browser-side dashboard UI.
* Fetches JSON data from FastAPI APIs every 5 seconds.
* Displays metrics as cards, recent trace lines in tables, and error logs.
* Provides simple, intuitive real-time observability for users.
6. run.sh
* Shell script wrapping common commands:
    * Build and run Docker container.
    * Run app in watch or single file mode.
    * Build Python package.
    * Clean build artifacts.
* Simplifies running and deployment for developers and CI/CD.
7. Dockerfile
* Containerizes application with Python 3.12 slim image.
* Installs dependencies from requirements.txt via pip.
* Copies application code.
* Defines default command to run FastAPI app with Uvicorn in watch mode.
* Enables consistent environment for deployment.

Flow of Execution
1. Start Application:
* Run via CLI or run.sh in watch or single file mode.
2. Single File Mode:
* Reads the specified input file.
* Passes lines to StateEngine.run() for processing.
* Writes processed output to a file.
* Exits.
3. Watch Mode:
* FolderMonitor continuously polls unprocessed/ folder.
* Moves new files into underprocess/ and processes them line-by-line.
* Updates StateEngine metrics, traces, and errors in memory.
4. Dashboard Server:
* FastAPI serves REST APIs exposing processing stats.
* Serves frontend dashboard URL /.
* Frontend polls backend APIs for live state.
* Visualizes pipeline observability and errors in real time.
5. Containerization:
* Docker builds reproducible environment with dependencies.
* Runs the app inside container exposing port 8000.

Run:
Give execute permissions:
`chmod +x run.sh`

Run using:
`bash run.sh [option]`