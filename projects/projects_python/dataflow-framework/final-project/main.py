import typer
from observability.shared_state import SharedState
from observability.dashboard import start_dashboard_thread
from folder_monitor import FolderMonitor
from state_engine import StateEngine

app = typer.Typer(help="Level 8: Folder Monitor + Single File Processor with Observability")

@app.command()
def run(
    watch_dir: str = typer.Option(None, help="Root directory to watch with queue subfolders"),
    input: typer.FileText = typer.Option(None, help="Single input text file for one-shot processing"),
    trace: bool = typer.Option(False, help="Enable tracing and observability dashboard"),
):
    shared_state = SharedState()  # <-- Always create SharedState

    if watch_dir:
        if trace:
            start_dashboard_thread(shared_state)
            typer.echo("Observability dashboard running at http://localhost:8000")
        monitor = FolderMonitor(watch_dir, shared_state, trace_enabled=trace)
        typer.echo(f"Starting folder monitor for directory: {watch_dir}")
        try:
            monitor.run_forever()
        except KeyboardInterrupt:
            typer.echo("\nShutting down folder monitor gracefully...")

    elif input:
        input_lines = [line.strip() for line in input if line.strip()]
        engine = StateEngine("pipeline_state.yaml", shared_state, trace_enabled=trace)
        outputs = engine.run(input_lines)
        typer.echo("\n--- Final Output ---")
        for line in outputs:
            typer.echo(line)

    else:
        typer.echo("Error: Please specify either --watch-dir or --input.", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
