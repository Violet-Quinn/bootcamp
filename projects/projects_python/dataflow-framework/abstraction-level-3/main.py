from typing import Iterable, Optional
from core import apply_processors
from pipeline import build_pipeline

def read_lines(path: str) -> Iterable[str]:
    """
    Read a text file line-by-line, yielding each line with 
    trailing whitespace stripped.
    """
    with open(path, "r") as infile:
        for line in infile:
            yield line.strip()

def write_output(lines: Iterable[str], output_path: Optional[str]) -> None:
    """
    Output lines either by writing to a file or printing to console.
    """
    if output_path:
        with open(output_path, "w") as outfile:
            for line in lines:
                outfile.write(line + "\n")
    else:
        for line in lines:
            print(line)

def run_pipeline(input_path: str, output_path: Optional[str], mode: str) -> None:
    """
    Loads processors dynamically from config YAML,
    processes input lines and writes output.
    """
    processors = build_pipeline(mode)
    lines = read_lines(input_path)
    processed_lines = apply_processors(lines, processors)
    write_output(processed_lines, output_path)
