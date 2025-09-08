from typing import Iterator

class JoinEveryTwoLines:
    def __init__(self):
        self.buffer = []

    def __call__(self, lines: Iterator[str]) -> Iterator[str]:
        for line in lines:
            self.buffer.append(line)
            if len(self.buffer) == 2:
                yield " ".join(self.buffer)
                self.buffer.clear()

        # Emit leftover if odd number of lines
        if self.buffer:
            yield self.buffer.pop()
