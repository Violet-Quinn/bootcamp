def join_lines(lines):
    buffer = []
    for tag, line in lines:
        buffer.append(line)
        if len(buffer) == 2:
            joined = " ".join(buffer)
            yield ("end", joined)
            buffer.clear()
    # flush if odd number of lines
    if buffer:
        yield ("end", buffer[0])
