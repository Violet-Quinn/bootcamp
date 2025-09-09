import threading
import typer
from state_engine import StateEngine
from fastapi.staticfiles import StaticFiles
import uvicorn
from dashboard.dashboard import create_dashboard_app
from folder_monitor import FolderMonitor  # New import


app = typer.Typer(help="Level-8 Folder Monitor Dataflow Engine CLI")


def run_folder_monitor_and_dashboard(state_engine: StateEngine, watch_dir: str):
    monitor = FolderMonitor(watch_dir, state_engine)
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()

    app_instance = create_dashboard_app(state_engine)
    app_instance.mount("/", StaticFiles(directory="static", html=True), name="static")

    uvicorn.run(app_instance, host="127.0.0.1", port=8000)


@app.command()
def run(
    config: str = typer.Option("pipeline.yaml", help="Path to pipeline config YAML file"),
    watch_dir: str = typer.Option("watch_dir", help="Directory to watch for input files"),
    dashboard: bool = typer.Option(True, help="Whether to start the observability dashboard"),
):
    engine = StateEngine(config, trace=True)  # Enable trace for visibility

    if dashboard:
        run_folder_monitor_and_dashboard(engine, watch_dir)
    else:
        typer.echo("Dashboard must be enabled to run folder monitor.")


if __name__ == "__main__":
    app()
