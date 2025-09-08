def tag_lines(lines):
    """Assign tags 'error', 'warn', or 'general' based on line content."""
    for line in lines:
        _tag, content = line if isinstance(line, tuple) else ("", line)
        content_lower = content.lower()
        if "error" in content_lower:
            yield ("error", content)
        elif "warn" in content_lower:
            yield ("warn", content)
        else:
            yield ("general", content)
