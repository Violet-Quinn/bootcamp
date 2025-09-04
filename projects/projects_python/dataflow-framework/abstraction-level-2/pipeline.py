from core import to_uppercase, to_snakecase
from processor_types import ProcessorFn

def build_pipeline(mode: str) -> list[ProcessorFn]:
    """
    Build a list of processing functions based on the specified mode.
    Args:
        mode (str): The processing mode, e.g., "uppercase" or "snakecase".
    Returns:
        list[ProcessorFn]: A list of processing functions to apply.
    Raises:
        ValueError: If an unsupported mode is provided.
    """
    if mode == "uppercase":
        return [to_uppercase]
    elif mode == "snakecase":
        return [to_snakecase]
    else:
        raise ValueError(f"Unsupported mode: {mode}")
