from typing import Iterable, Iterator
from processor_types import ProcessorFn



def apply_processors(lines: Iterable[str], processors: list[ProcessorFn]) -> Iterator[str]:
    """
    Apply a processing function to each line in an iterable of strings.

    Args:
        lines (Iterable[str]): An iterable of string lines to process.
        processor (ProcessorFn): A function that takes a string and returns a processed string.

    Yields:
        str: Each processed line.
    """
    for line in lines:
        for processor in processors:
            line = processor(line)
        yield line