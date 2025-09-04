from typing import Iterator

class LineCountProcessor:
    def __init__(self):
        """Initializes the line count processor."""
        self.count = 0
    
    def __call__(self, lines: Iterator[str]) -> Iterator[str]:
        """Processes lines and prefixes each with a line count.
        """
        for line in lines:
            self.count += 1
            yield f"{self.count}: {line}"
