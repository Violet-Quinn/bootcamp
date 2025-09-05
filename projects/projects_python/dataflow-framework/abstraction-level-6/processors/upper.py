from typing import Iterator, Tuple

def upper(lines: Iterator[str]) -> Iterator[Tuple[str, str]]:
    """
    Converts each line to uppercase and yields tagged lines.
    Tag is 'upper' (arbitrary, can be used in routing).
    """
    for line in lines:
        yield ("upper", line.upper())
