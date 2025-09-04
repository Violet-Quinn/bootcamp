def to_snakecase(line: str) -> str:
    """
    Convert a string to snake_case.
    """
    return line.replace(" ", "_").lower()