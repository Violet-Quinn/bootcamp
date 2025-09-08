import typer
from dotenv import load_dotenv
import os
from typing import Iterator, Optional

app = typer.Typer()
load_dotenv()

def read_lines(path: str) -> Iterator[str]:
    """Yield lines from a file, stripped of trailing whitespace."""
    with open(path) as f:
        for line in f:
            yield line.strip()

def transform_line(line: str, mode: str) -> str:
    """Transform line: uppercase or snakecase (spaces to underscores + lowercase)."""
    if mode == "uppercase":
        return line.upper()
    elif mode == "snakecase":
        return line.replace(" ", "_").lower()
    raise ValueError(f"Unsupported mode: {mode}")

def write_output(lines: Iterator[str], output_path: Optional[str]) -> None:
    """Write lines to a file if output_path given; else print to stdout."""
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
    mode: str = typer.Option(os.getenv("MODE", "uppercase"), "--mode", "-m", help="Processing mode"),
):
    """Process lines from input file and output transformed lines."""
    lines = (transform_line(line, mode) for line in read_lines(input_path))
    write_output(lines, output)

if __name__ == "__main__":
    app()
