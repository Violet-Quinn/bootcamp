import typer
from dotenv import load_dotenv
import os
from typing import Iterator, Optional


app = typer.Typer()
load_dotenv()


def read_lines(path: str) -> Iterator[str]:
    """
    Read a text file line-by-line, yielding each line with 
    trailing whitespace stripped.

    Args:
        path (str): Path of the file to read.

    Yields:
        str: Each line in the file, stripped of trailing newlines.

    This function opens the file at the specified path and 
    streams the lines lazily, which is efficient for large files.
    """
    with open(path, "r") as infile:
        for line in infile:
            yield line.strip()


def transform_line(line: str, mode: str) -> str:
    """
    Transform a string line based on the selected mode.

    Args:
        line (str): Input string line to transform.
        mode (str): Mode for transformation. Supported values:
            - "uppercase": converts text to uppercase.
            - "snakecase": replaces spaces with underscores and 
              converts text to lowercase.

    Returns:
        str: The transformed line resulting from the applied mode.

    Raises:
        ValueError: If an unsupported mode is provided.
    """
    if mode == "uppercase":
        return line.upper()
    elif mode == "snakecase":
        return line.replace(" ", "_").lower()
    else:
        raise ValueError(f"Unsupported mode: {mode}")


def write_output(lines: Iterator[str], output_path: Optional[str]) -> None:
    """
    Output lines either by writing to a file or printing to console.

    Args:
        lines (Iterator[str]): Iterable of lines to output.
        output_path (Optional[str]): File path to write output to. 
            If None, output is printed.

    This function handles outputting the processed text lines 
    based on whether an output path is specified.
    """
    if output_path:
        with open(output_path, "w") as outfile:
            for line in lines:
                outfile.write(line + "\n")
    else:
        for line in lines:
            typer.echo(line)


@app.command()
def main(
    input_path: str = typer.Option(..., "--input", "-i", help="Input file path"),
    output: Optional[str] = typer.Option(None, help="Output file path"),
    mode: str = typer.Option(os.getenv("MODE", "uppercase"), help="Processing mode"),
) -> None:
    """
    Main CLI command for reading, transforming, and writing lines.

    Args:
        input_path (str): Path to the input file.
        output (Optional[str]): Path for the output file. Prints
            to stdout if not provided.
        mode (str): Text transformation mode to apply, defaulted 
            from environment or 'uppercase'.

    This command reads lines from input_path, processes them 
    according to mode, and writes the output.
    """
    raw_lines = read_lines(input_path)
    processed_lines = (transform_line(line, mode) for line in raw_lines)
    write_output(processed_lines, output)


if __name__ == "__main__":
    app()
