from typing import Iterator, Tuple


def join_pairs(lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
    """
    Joins pairs of lines into single lines separated by a space.
    Yields lines tagged 'joined'.
    """
    buffer = []
    for _, line in lines:
        buffer.append(line)
        if len(buffer) == 2:
            joined_line = " ".join(buffer)
            yield ('joined', joined_line)
            buffer = []
    # Yield leftover if any
    if buffer:
        yield ('joined', buffer[0])
