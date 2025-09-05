import typer
from typing import TextIO
from state_engine import StateEngine
from pipeline import Pipeline

app = typer.Typer(help="Dataflow pipeline runner with DAG or State Machine modes.")

@app.command()
def run(
    input: typer.FileText = typer.Option(..., help="Input text file with lines to process"),
    mode: str = typer.Option("state", help="Pipeline mode: 'state' or 'dag'")
):
    """Run the dataflow pipeline in specified mode."""
    input_lines = [line.strip() for line in input if line.strip()]
    
    if mode == "dag":
        typer.echo("Running Level-5 DAG pipeline...")
        pipeline = Pipeline("pipeline.yaml")
        outputs = pipeline.run(input_lines)
        typer.echo("\n--- Final Output (DAG) ---")
        for line in outputs:
            typer.echo(line)
    elif mode == "state":
        typer.echo("Running Level-6 State Routing engine...")
        engine = StateEngine("pipeline_state.yaml")
        outputs = engine.run(input_lines)
        typer.echo("\n--- Final Output (State Engine) ---")
        for line in outputs:
            typer.echo(line)
    else:
        typer.echo(f"Invalid mode '{mode}'. Use 'dag' or 'state'.", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
