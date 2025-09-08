from typing import Callable

# A processor is a function that takes str and returns str
ProcessorFn = Callable[[str], str]
