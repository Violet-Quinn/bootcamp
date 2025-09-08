from typing import Iterator, Tuple

TaggedLine = Tuple[str, str]

class JoinEveryTwoLines:
    def __init__(self):
        self.buffer = []

    def __call__(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            self.buffer.append((tag, line))
            if len(self.buffer) == 2:
                combined_line = " ".join(l for _, l in self.buffer)
                combined_tag = self.buffer[0][0] or "default"
                self.buffer.clear()
                yield combined_tag, combined_line

        # Emit leftover line if odd count
        if self.buffer:
            yield self.buffer.pop()
            self.buffer.clear()
