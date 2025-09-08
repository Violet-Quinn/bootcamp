import typer
import os
from typing import Optional
from dotenv import load_dotenv

from pipeline import build_pipeline
from core import apply_processors

app = typer.Typer()
load_dotenv()

def read_lines(path: str):
    with open(path) as f:
        for line in f:
            yield line.strip()

def write_output(lines, output_path: Optional[str]) -> None:
    if output_path:
        with open(output_path, "w") as f:
            for line in lines:
                f.write(line + "\n")
    else:
        for line in lines:
            typer.echo(line)

@app.callback(invoke_without_command=True)
def main(
    input_path: str = typer.Option(..., "--input", "-i", help="Input file path"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    mode: str = typer.Option(os.getenv("MODE", "uppercase"), "--mode", "-m", help="Comma-separated processing modes"),
):
    """
    Process lines using a sequence of transformations.
    Multiple modes can be given (e.g. --mode uppercase,snakecase).
    If not provided, defaults to MODE from .env.
    """
    modes = [m.strip() for m in mode.split(",")]
    processors = build_pipeline(modes)

    lines = (apply_processors(line, processors) for line in read_lines(input_path))
    write_output(lines, output)

if __name__ == "__main__":
    app()
