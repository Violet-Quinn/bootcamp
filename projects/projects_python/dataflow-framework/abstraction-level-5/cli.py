import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command()
def run(
    input: typer.FileText = typer.Option(..., help="Input file path"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
    config: str = typer.Option("pipeline.yaml", help="Pipeline config YAML file"),
):
    """
    Run the DAG-based processing pipeline on the input file lines using the specified config.
    Writes output to the given file or prints to stdout if no output file is provided.
    """
    from pipeline import Pipeline

    lines = (line.rstrip("\n") for line in input)
    pipeline = Pipeline(config)

    results = pipeline.run(lines)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as f:
            for line in results:
                f.write(line + "\n")
    else:
        for line in results:
            print(line)

if __name__ == "__main__":
    app()
