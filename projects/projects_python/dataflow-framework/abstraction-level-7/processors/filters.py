def only_error(lines):
    for tag, line in lines:
        if "error" in line.lower():
            yield ("end", line)

def only_warn(lines):
    for tag, line in lines:
        if "warn" in line.lower():
            yield ("end", line)
