from typing import Iterator, Tuple

def line_count(lines: Iterator[str]) -> Iterator[Tuple[str, str]]:
    """
    Counts lines seen so far and appends count info to line.
    Yields tagged lines with tag 'counted'.
    """
    count = 0
    for line in lines:
        count += 1
        yield ("counted", f"{line.strip()} [count={count}]")
