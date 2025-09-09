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
1. main.py
* This is the entry point of your application.
* Sets up the StateEngine that manages pipeline processing state, metrics, traces, and errors.
* Starts the FolderMonitor in a background thread to watch a directory for new files.
* The folder monitor picks up files, processes them via the StateEngine, and updates metrics continuously.
* Creates and runs the FastAPI dashboard app which serves the frontend UI and API endpoints.
* The dashboard shows processing stats, recent traces, and errors in near real-time by querying the backend APIs.

2. folder_monitor.py
* Watches a target "watch" directory continuously.
* Manages subfolders: unprocessed, underprocess, and processed for file state.
* Moves files through these directories as they are picked up, processed, and finalized.
* Calls StateEngine.run() to process lines through the multi-stage pipeline.
* Updates shared metrics on folder states and currently processing file in the StateEngine.
* Captures and reports errors occurring during file processing for dashboard display.

3. state_engine.py
* Core pipeline processing engine managing processors, routing, and pipeline state.
* Loads processing nodes from a YAML config, dynamically imports processor code.
* Maintains a directed acyclic graph of tags and their routes through processors.
* Runs lines through processors maintaining routing, metrics (counts, timings, errors), traces, and errors.
* Thread-safe data structures with locks for concurrent updates by folder monitor and dashboard.

4. dashboard.py
* Defines FastAPI API routes serving JSON data representing metrics, traces, and errors.
* Adds CORS middleware allowing frontend JS to access backend APIs.
* Returns real-time state data protected by locks to ensure consistency.
* Returns cache-control headers majorly to prevent browser-side caching of stale data.

5. static/index.html
* Frontend dashboard UI consuming the FastAPI API endpoints.
* Displays processor metrics as cards, recent processing traces, and recent errors in tables.
* Auto-refreshes every 5 seconds fetching fresh JSON from API endpoints.
* Uses inline CSS styles for UI styling.
* Dynamically creates and updates DOM elements to represent live backend data.

Flow of Execution:
1. Startup: main.py initializes StateEngine, starts FolderMonitor thread, and runs FastAPI dashboard server.
2. File Watching & Processing:
    * FolderMonitor sees new files in unprocessed/, moves them to underprocess/.
    * Calls StateEngine.run() to send lines through processors following routing.
    * Updates file state metrics in StateEngine.metrics.
3. State & Metrics Updates:
    * StateEngine tracks processor call counts, timings, errors.
    * FolderMonitor updates folder/file counts in metrics.
    * Traces and errors collected for troubleshooting and display.
4. Dashboard UI Updates:
    * Frontend periodically fetches /api/stats, /api/trace, and /api/errors.
    * Backend protects shared state with locks and returns fresh JSON data with no-cache headers.
    * Frontend reconstructs HTML to show up-to-date stats, traces, errors to user.


Run:
python3 main.py --watch-dir watch_dir --config pipeline.yaml --dashboard