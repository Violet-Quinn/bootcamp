from typing import Iterator, Tuple

def join_pairs(lines: Iterator[str]) -> Iterator[Tuple[str, str]]:
    """
    Joins every two consecutive lines with a space in between.
    Tags output lines as 'joined'.
    """
    buffer = []
    for line in lines:
        buffer.append(line.strip())
        if len(buffer) == 2:
            joined_line = buffer[0] + " " + buffer[1]
            yield ("joined", joined_line)
            buffer = []
    # If odd line count, emit the leftover line as is
    if buffer:
        yield ("joined", buffer[0])
