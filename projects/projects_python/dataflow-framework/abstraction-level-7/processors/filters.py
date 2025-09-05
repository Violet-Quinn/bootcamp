def only_error(lines):
    """Processes only error lines."""
    for line in lines:
        yield ("end", f"[ERROR] {line}")

def only_warn(lines):
    """Processes only warning lines."""
    for line in lines:
        yield ("end", f"[WARN] {line}")
