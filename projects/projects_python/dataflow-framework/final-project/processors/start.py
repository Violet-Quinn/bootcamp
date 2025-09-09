def tag_lines(lines):
    for line in lines:
        _tag, content = line if isinstance(line, tuple) else ("", line)
        content_lower = content.lower()
        if "error" in content_lower:
            tag = "error"
        elif "warn" in content_lower:
            tag = "warn"
        else:
            tag = "general"
        print(f"Tagging line: '{content}' as '{tag}'")  # Debug log
        yield (tag, content)
