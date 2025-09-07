from typing import Iterator, Tuple

def snake(lines: Iterator[str]) -> Iterator[Tuple[str, str]]:
    """
    Convert line to snake_case: lowercase and replace spaces with underscores.
    Yields 'snake' tag and processed line.
    """
    for line in lines:
        snake_line = line.strip().replace(" ", "_").lower()
        yield ("snake", snake_line)
