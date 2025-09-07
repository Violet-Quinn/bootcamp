from typing import Iterator, Tuple, Callable

ProcessorFn = Callable[[Iterator[str]], Iterator[Tuple[str, str]]]
"""Defines the type for a processor function in a dataflow framework."""
