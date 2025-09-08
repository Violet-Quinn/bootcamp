def tag_lines(lines):
    """Example processor tagging lines as error, warn, or general."""
    for line in lines:
        _tag, content = line if isinstance(line, tuple) else ("", line)
        content_lower = content.lower()
        if "error" in content_lower:
            yield ("error", content)
        elif "warn" in content_lower:
            yield ("warn", content)
        else:
            yield ("general", content)
