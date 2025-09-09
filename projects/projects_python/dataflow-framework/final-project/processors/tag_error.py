def tag_error(lines):
    for tag, line in lines:
        if "error" in line.lower():
            yield ("error", line)
        else:
            yield ("general", line)
