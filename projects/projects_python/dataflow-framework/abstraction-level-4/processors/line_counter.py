from typing import Iterator

class LineCounter:
    def __init__(self):
        self.count = 0

    def __call__(self, lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            self.count += 1
            yield f"{self.count}: {line}"
