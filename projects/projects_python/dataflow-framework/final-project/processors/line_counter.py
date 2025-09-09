def count_lines(lines):
    count = 0
    for tag, line in lines:
        count += 1
        yield ("end", f"{count}: {line}")
