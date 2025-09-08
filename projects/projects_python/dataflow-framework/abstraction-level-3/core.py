from typing import List
from processor_types import ProcessorFn

def apply_processors(line: str, processors: List[ProcessorFn]) -> str:
    for processor in processors:
        line = processor(line)
    return line
