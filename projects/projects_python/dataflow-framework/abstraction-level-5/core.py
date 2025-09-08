from typing import List, Iterator, Callable
from processor_types import ProcessorFn, TaggedLine

def apply_processors(lines: Iterator[str], processors: List[Callable[[Iterator[str]], Iterator[str]]]) -> Iterator[str]:
    for processor in processors:
        lines = processor(lines)
    return lines

def line_fn_to_dag_processor(fn: Callable[[str], str]) -> ProcessorFn:
    def processor(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            yield tag or "default", fn(line)
    return processor
