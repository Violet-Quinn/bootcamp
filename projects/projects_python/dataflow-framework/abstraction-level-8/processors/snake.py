from typing import Iterator, Tuple

def to_snakecase(lines: Iterator[str]) -> Iterator[Tuple[str, str]]:
    """
    Converts spaces to underscores and lowercases the line, yields tagged lines.
    Tag is 'snake'.
    """
    for line in lines:
        snake_line = line.strip().replace(" ", "_").lower()
        yield ("snake", snake_line)
