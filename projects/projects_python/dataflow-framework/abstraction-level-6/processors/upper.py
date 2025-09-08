def upper(lines):
    for tag, line in lines:
        yield ("end", line.upper())
