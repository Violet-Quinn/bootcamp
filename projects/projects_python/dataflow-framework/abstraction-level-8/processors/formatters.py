def snake(lines):
    """Convert lines to snake_case."""
    import re
    def to_snake_case(s):
        s = re.sub(r'[\W]+', '_', s)
        s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
        return s.lower().strip('_')

    for tag, line in lines:
        yield ("end", to_snake_case(line))
