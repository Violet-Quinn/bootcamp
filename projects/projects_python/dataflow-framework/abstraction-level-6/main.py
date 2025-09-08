import typer
from state_engine import StateEngine

app = typer.Typer(help="Level-6 State-Based Routing Engine CLI")

@app.command()
def run(
    input: typer.FileText = typer.Option(..., help="Input text file with lines to process"),
    config: str = typer.Option("pipeline_state.yaml", help="Path to pipeline config YAML file"),
    visualize: bool = typer.Option(False, help="Visualize routing graph and exit without processing")
):
    """
    Run the Level-6 State Routing engine on input lines, optionally visualize routing graph.
    """
    engine = StateEngine(config)

    if visualize:
        typer.echo(f"Visualizing routing graph from config: {config}")
        engine.visualize()
        raise typer.Exit()

    input_lines = [line.strip() for line in input if line.strip()]
    typer.echo(f"Using config file: {config}")
    outputs = engine.run(input_lines)

    typer.echo("\n--- Final Output (State Engine) ---")
    for line in outputs:
        typer.echo(line)

if __name__ == "__main__":
    app()
