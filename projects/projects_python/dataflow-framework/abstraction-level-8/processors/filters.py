def only_error(lines):
    prefix = "[ERROR]"
    for tag, line in lines:
        if "error" in line.lower():
            yield ("end", f"{prefix} {line}")

def only_warn(lines):
    prefix = "[WARN]"
    for tag, line in lines:
        if "warn" in line.lower():
            yield ("end", f"{prefix} {line}")
