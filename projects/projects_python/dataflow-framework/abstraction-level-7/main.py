import typer
from typing import Optional
from state_engine import StateEngine
from pipeline import Pipeline
from observability.shared_state import SharedState
from observability.dashboard import start_dashboard_thread


app = typer.Typer(help="Dataflow pipeline runner with DAG or State Machine modes.")


@app.command()
def run(
    input: typer.FileText = typer.Option(..., help="Input text file with lines to process"),
    mode: str = typer.Option("state", help="Pipeline mode: 'state' or 'dag'"),
    trace: bool = typer.Option(False, help="Enable trace collection and observability dashboard"),
) -> None:
    """
    Run the dataflow pipeline using either DAG or State Engine mode.

    Args:
        input (typer.FileText): Input text file containing lines to process.
        mode (str): Pipeline mode ('dag' or 'state'). Defaults to 'state'.
        trace (bool): Whether to enable trace collection and observability dashboard.
    """
    input_lines = [line.strip() for line in input if line.strip()]
    shared_state: Optional[SharedState] = None

    if trace:
        shared_state = SharedState()
        start_dashboard_thread(shared_state)
        typer.echo("Observability dashboard running at http://localhost:8000")

    if mode == "dag":
        typer.echo("Running Level-5 DAG pipeline...")
        pipeline = Pipeline("pipeline.yaml")
        outputs = pipeline.run(input_lines)
        typer.echo("\n--- Final Output (DAG) ---")
        for line in outputs:
            typer.echo(line)
    elif mode == "state":
        typer.echo("Running Level-6 State Routing engine...")
        engine = StateEngine("pipeline_state.yaml", shared_state, trace_enabled=trace)
        outputs = engine.run(input_lines)
        typer.echo("\n--- Final Output (State Engine) ---")
        for line in outputs:
            typer.echo(line)
    else:
        typer.echo(f"Invalid mode '{mode}'. Use 'dag' or 'state'.", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
