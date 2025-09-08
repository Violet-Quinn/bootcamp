from typing import Iterator, Tuple
from processor_types import TaggedLine

class TagError:
    def __call__(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            if "error" in line.lower():
                yield "error", line
            else:
                yield "general", line
