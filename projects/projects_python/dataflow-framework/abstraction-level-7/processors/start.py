def tag_lines(lines):
    """
    Start processor: classify inputs into error / warn / general.
    """
    for line in lines:
        text = line.strip()
        if "error" in text.lower():
            yield ("error", text)
        elif "warn" in text.lower():
            yield ("warn", text)
        else:
            yield ("general", text)
