from typing import Iterable, Optional
import typer

def read_lines(path: str) -> Iterable[str]:
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

def write_output(lines: Iterable[str], output_path: Optional[str]) -> None:
    """
    Output lines either by writing to a file or printing to console.
    Args:
        lines (Iterable[str]): Iterable of lines to output.
        output_path (Optional[str]): Path to the output file. If None, 
            lines are printed to the console.
    """
    if output_path:
        with open(output_path, "w") as outfile:
            for line in lines:
                outfile.write(line + "\n")
    else:
        for line in lines:
            typer.echo(line) 