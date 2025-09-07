import typer
import time
from observability.shared_state import SharedState
from observability.dashboard import start_dashboard_thread
from folder_monitor import FolderMonitor

app = typer.Typer(help="Level 8: Automated Folder Monitor with Recovery and Observability")

@app.command()
def run(
    watch_dir: str = typer.Option(..., help="Root directory to watch with queue subfolders"),
    trace: bool = typer.Option(False, help="Enable tracing and observability dashboard"),
) -> None:
    """
    Start the folder monitoring service with live dashboard and pipeline processing.
    Runs indefinitely.
    """
    shared_state = SharedState()

    if trace:
        start_dashboard_thread(shared_state)
        typer.echo("Observability dashboard running at http://localhost:8000")

    monitor = FolderMonitor(watch_dir, shared_state, trace_enabled=trace)
    typer.echo(f"Starting folder monitor for directory: {watch_dir}")
    try:
        monitor.run_forever()
    except KeyboardInterrupt:
        typer.echo("\nShutting down folder monitor gracefully...")

if __name__ == "__main__":
    app()
