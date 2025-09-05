def terminal(lines):
    """
    Final output processor — just prints and passes to 'end'.
    """
    for line in lines:
        print("FINAL:", line)
        yield ("end", line)
