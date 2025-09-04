import os
import typer
from dotenv import load_dotenv

from main import read_lines, write_output
from pipeline import build_pipeline
from core import apply_processors

app = typer.Typer()
load_dotenv()

@app.command()
def run(
    input_path: str = typer.Option(..., "--input", "-i", help="Input file path"),
    output: str = typer.Option(None, help="Output file path"),
    mode: str = typer.Option(os.getenv("MODE", "uppercase"), help="Processing mode"),
) -> None:
    """
    Read text from an input file, process it based on the mode, and write or display the result.
    Args:
        input_path (str): Path to the input text file.
        output (str, optional): Path to save the processed output. Prints to console if not set.
        mode (str): Text processing mode ('uppercase' or 'snakecase').
    """
    raw_lines = read_lines(input_path)
    processors = build_pipeline(mode)
    processed_lines = apply_processors(raw_lines, processors)
    write_output(processed_lines, output)

if __name__ == "__main__":
    app()
