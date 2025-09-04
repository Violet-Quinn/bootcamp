from typing import Iterator


def join_pairs(lines: Iterator[str]) -> Iterator[str]:
    """
    Joins pairs of lines into single lines, separated by a space.
    If there's an odd line out, it is yielded as is.
    """
    buffer = []
    for line in lines:
        buffer.append(line)
        if len(buffer) == 2:
            yield " ".join(buffer)
            buffer = []
    if buffer:
        yield buffer[0]
