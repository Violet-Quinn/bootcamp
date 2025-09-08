from typing import List
from processor_types import ProcessorFn
from core import to_uppercase, to_snakecase

def build_pipeline(modes: List[str]) -> List[ProcessorFn]:
    """Return a static list of processors for the given modes."""
    processors: List[ProcessorFn] = []
    for mode in modes:
        if mode == "uppercase":
            processors.append(to_uppercase)
        elif mode == "snakecase":
            processors.append(to_snakecase)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
    return processors
