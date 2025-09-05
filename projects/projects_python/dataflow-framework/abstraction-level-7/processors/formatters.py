def snake(lines):
    """Converts general logs to snake_case."""
    for line in lines:
        snake_case = line.lower().replace(" ", "_")
        yield ("end", snake_case)
