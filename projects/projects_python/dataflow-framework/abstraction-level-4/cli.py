import typer
from main import run_pipeline
from typing import Optional

app = typer.Typer()

@app.command()
def main(
    input: str = typer.Option(..., help="Input file path"),
    output: Optional[str] = typer.Option(None, help="Output file path (optional)"),
    config: str = typer.Option(..., help="Path to pipeline YAML config file")
):
    """
    CLI command that runs the processing pipeline based on YAML config.
    """
    try:
        run_pipeline(input, output, config)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
