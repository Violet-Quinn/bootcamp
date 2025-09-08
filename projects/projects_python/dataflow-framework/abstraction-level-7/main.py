import threading
import typer
from state_engine import StateEngine
from fastapi.staticfiles import StaticFiles
import uvicorn

from dashboard.dashboard import create_dashboard_app  # your refactored dashboard app factory

app = typer.Typer(help="Level-7 Observability Dataflow Engine CLI")

def process_engine(engine, input_lines):
    outputs = engine.run(input_lines)
    typer.echo("\n--- Final Output (State Engine) ---")
    for line in outputs:
        typer.echo(line)

@app.command()
def run(
    input: typer.FileText = typer.Option(..., help="Input text file with lines to process"),
    config: str = typer.Option("pipeline.yaml", help="Path to pipeline config YAML file"),
    trace: bool = typer.Option(False, help="Enable tracing of line journeys"),
    dashboard: bool = typer.Option(False, help="Start FastAPI observability dashboard")
):
    input_lines = [line.strip() for line in input if line.strip()]
    engine = StateEngine(config, trace=trace)

    if dashboard:
        # Run pipeline in background thread
        processing_thread = threading.Thread(target=process_engine, args=(engine, input_lines), daemon=True)
        processing_thread.start()

        # Create FastAPI app instance including API routes
        app_instance = create_dashboard_app(engine)

        # Mount static files (your frontend dashboard) at root
        app_instance.mount("/", StaticFiles(directory="static", html=True), name="static")

        # Start Uvicorn server to serve both API and frontend
        uvicorn.run(app_instance, host="127.0.0.1", port=8000)

    else:
        # Run pipeline synchronously without dashboard
        process_engine(engine, input_lines)

if __name__ == "__main__":
    app()
