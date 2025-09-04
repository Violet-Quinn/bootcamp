from typing import Iterator, Tuple, Callable

ProcessorFn = Callable[[Iterator[str]], Iterator[Tuple[str, str]]]
