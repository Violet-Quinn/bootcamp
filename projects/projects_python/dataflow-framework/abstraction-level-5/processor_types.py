from typing import Iterator, Tuple, Callable, List, Dict

TaggedLine = Tuple[str, str]
ProcessorFn = Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]
