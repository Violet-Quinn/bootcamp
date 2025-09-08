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
1. state_engine.py
* This is the core processing engine of the pipeline.
* It loads the pipeline configuration YAML to set up processing nodes and routing.
* Dynamically loads processor functions.
* Runs tubes of lines through processors according to routing until reaching the end.
* Maintains thread-safe metrics, traces, and errors collections during processing, used later for observability.
* Returns final output lines after processing input.

2. dashboard.py
* Defines FastAPI API routes to expose pipeline metrics, traces, and errors.
* Wraps routes in a router with CORS middleware for cross-origin access.
* Provides JSON responses for /api/stats, /api/trace, /api/errors.
* Also exposes a root /api/ endpoint for a status message.
* Intended to be imported and mounted into your FastAPI application.

3. main.py
* Defines CLI commands using typer.
* On run command:
    * Reads input file lines and sets up the StateEngine with pipeline config.
    * If dashboard requested, starts pipeline processing in background thread.
    * Instantiates FastAPI app from dashboard.py, mounts static frontend files at /.
    * Calls uvicorn.run() to start ASGI server serving both frontend and API.
    * If no dashboard requested, runs pipeline synchronously and outputs final lines.
* Acts as the application entry point controlling lifecycle and coordination.

4. index.html (inside static/ folder)
* Vanilla HTML/CSS/JS frontend dashboard, visually inspired by Kubernetes dashboard.
* Uses vanilla JS fetch calls every 5 seconds to /api/stats, /api/trace, /api/errors.
* Dynamically updates metric cards, trace table, and error table on the page.
* Simple, clean UI allowing real-time monitoring of data pipeline observability outputs.

Flow of execution overview
1. User runs command:
```bash
    python3 main.py --input input.txt --dashboard or without --dashboard to run without UI.
```
2. main.py:
    * Loads input lines.
    * Instantiates StateEngine with pipeline config.
    * If dashboard enabled:
        * Runs pipeline processing on a background thread, which processes each input line through pipeline nodes.
        * Sets up FastAPI app with API routes from dashboard.py.
        * Serves static frontend (index.html) at root path /.
        * Starts Uvicorn ASGI server to serve API + UI.
3. Pipeline processing:
    * StateEngine.run() feeds lines to processors in order.
    * Collects metrics (counts, durations, errors), traces of line paths, and errors, updating thread-safe stores.
    * Outputs final processed lines on completion.
4. Frontend:
    * Loads HTML+JS dashboard.
    * Calls /api/stats, /api/trace, /api/errors endpoints every 5 seconds.
    * Displays live metrics, traces, and error logs visually.
5. User can monitor pipeline execution and debug via dashboard UI in browser.

Run:
python3 main.py --input test_input.txt --trace --dashboard --config pipeline.yaml
Or
python3 main.py --input test_input.txt --config pipeline.yaml