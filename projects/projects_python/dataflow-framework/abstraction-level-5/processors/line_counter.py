from typing import Iterator, Tuple

TaggedLine = Tuple[str, str]

class LineCounter:
    def __init__(self):
        self.count = 0

    def __call__(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            self.count += 1
            yield tag or "default", f"{self.count}: {line}"
