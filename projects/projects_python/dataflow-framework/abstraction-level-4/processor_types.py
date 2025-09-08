from typing import Iterator, Callable

# Processor function now takes and returns iterators of strings
ProcessorFn = Callable[[Iterator[str]], Iterator[str]]
