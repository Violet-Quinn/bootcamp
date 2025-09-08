from typing import List, Iterator
from processor_types import ProcessorFn

def apply_processors(lines: Iterator[str], processors: List[ProcessorFn]) -> Iterator[str]:
    """Apply processors sequentially in streaming fashion."""
    for processor in processors:
        lines = processor(lines)
    return lines

def line_to_stream_processor(line_processor):
    """
    Decorator to adapt simple str -> str processor into stream processor.
    """
    def processor(lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            result = line_processor(line)
            if result is not None:
                yield result
    return processor
