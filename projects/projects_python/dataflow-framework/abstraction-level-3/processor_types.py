from typing import Callable

# Define a processor type: function that takes str and returns str
ProcessorFn = Callable[[str], str]
"""
Type alias for functions that take a string argument and return a string.
Using this to indicate a callable that processes a string and outputs a string.
"""
