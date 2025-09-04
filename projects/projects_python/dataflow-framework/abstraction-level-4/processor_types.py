from typing import Iterator, Callable

ProcessorFn = Callable[[Iterator[str]], Iterator[str]]

"""
Type alias for functions that take a string argument and return a string.
Using this to indicate a callable that processes a string and outputs a string.
"""
