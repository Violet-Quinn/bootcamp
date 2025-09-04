from processor_types import ProcessorFn
from typing import Iterator, Iterable, List, Callable

def apply_processors(lines: Iterator[str], processors: List[ProcessorFn]) -> Iterator[str]:
    """Applies a list of processors to an iterator of lines."""
    for processor in processors:
        lines = processor(lines)
    yield from lines

        
def stream_wrapper(simple_processor: Callable[[str], str]) -> ProcessorFn:
    """Wraps a simple line processor into a processor function."""
    def processor(lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            yield simple_processor(line)
    return processor
