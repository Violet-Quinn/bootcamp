import typer
from typing import Optional
from dotenv import load_dotenv
from pipeline import load_pipeline_from_config
from core import apply_processors

app = typer.Typer()
load_dotenv()

def read_lines(path: str):
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n")

def write_output(lines, output_path: Optional[str]) -> None:
    if output_path:
        with open(output_path, "w") as f:
            for line in lines:
                f.write(line + "\n")
    else:
        for line in lines:
            typer.echo(line)

@app.command()
def main(
    input_path: str = typer.Option(..., "--input", "-i", help="Input file path"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    config: str = typer.Option("pipeline.yaml", "--config", "-c", help="Pipeline YAML config path"),
):
    processors = load_pipeline_from_config(config)
    lines = read_lines(input_path)
    processed = apply_processors(lines, processors)
    write_output(processed, output)

if __name__ == "__main__":
    app()
