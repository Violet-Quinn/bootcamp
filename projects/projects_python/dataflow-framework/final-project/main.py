import threading
import typer
from state_engine import StateEngine
from fastapi.staticfiles import StaticFiles
import uvicorn
from dashboard.dashboard import create_dashboard_app
from folder_monitor import FolderMonitor

app = typer.Typer(help="Level-8 Folder Monitor Dataflow Engine CLI")

def run_folder_monitor_and_dashboard(state_engine: StateEngine, watch_dir: str):
    monitor = FolderMonitor(watch_dir, state_engine)
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()

    app_instance = create_dashboard_app(state_engine)
    # Serve frontend static files (your dashboard UI)
    app_instance.mount("/", StaticFiles(directory="static", html=True), name="static")

    uvicorn.run(app_instance, host="127.0.0.1", port=8000)

def run_single_file(state_engine: StateEngine, input_file: str):
    # Process a single file once and exit
    from os import path
    if not path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    print(f"Processing single file: {input_file}")
    # Read file lines
    with open(input_file, 'r') as f:
        input_lines = [line.strip() for line in f if line.strip()]
    # Run processing pipeline
    output_lines = state_engine.run(input_lines)
    # Write output back (or to a new file)
    output_file = input_file + ".processed"
    with open(output_file, 'w') as f:
        for line in output_lines:
            f.write(line + "\n")
    print(f"Finished processing. Output saved to {output_file}")

@app.command()
def run(
    input: str = typer.Option(None, help="Specify a single input file to process once"),
    watch: bool = typer.Option(False, help="Watch mode: watch for files continuously in watch_dir/unprocessed"),
    watch_dir: str = typer.Option("watch_dir", help="Directory to watch for input files"),
    config: str = typer.Option("pipeline.yaml", help="Path to pipeline configuration YAML"),
    dashboard: bool = typer.Option(True, help="Whether to start the dashboard server in watch mode")
):
    engine = StateEngine(config, trace=True)  # Enable tracing for observability

    if input and watch:
        typer.echo("Error: Please specify either --input or --watch, not both")
        raise typer.Exit(code=1)

    if input:
        run_single_file(engine, input)
        return

    if watch:
        run_folder_monitor_and_dashboard(engine, watch_dir)
    else:
        typer.echo("Please specify at least one mode: --input <file> or --watch")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
