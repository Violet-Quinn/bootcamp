def terminal(lines):
    """Output lines as is, tagged 'end'."""
    for tag, line in lines:
        yield ("end", line)
