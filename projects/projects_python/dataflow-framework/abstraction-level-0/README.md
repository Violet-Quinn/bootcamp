# Level 0 – Basic Script (No Abstraction)

---

## Task (abstraction-level-0)
Write a Python script that:
- Reads the stdin line by line
- Strips leading and trailing whitespace from each line
- Converts the result to uppercase
- Prints the processed lines to the stdout
- Put everything in a single file named process.py.

---

## Constraints
- No functions. Just sequential, top-to-bottom code.
- Use only Python built-in tools.

---

## Solution
This Python script reads input line by line from standard input (stdin, used `import sys` for this), processes each line by stripping leading and trailing whitespace, converts the text to uppercase, and writes the processed lines to standard output (stdout).
The script is designed to be simple and efficient, making it easy to integrate into pipelines or use with file redirection.

How it works:
- Reads each input line sequentially as it is received.
- Removes any extra spaces before and after the text using strip().
- Converts all characters in the line to uppercase using upper().
- Prints the resulting line immediately to the console or redirected output.

Run the script from the command line, providing input via file redirection:
```bash
    python3 your_script.py < input.txt
```

or
```bash
    echo -e "hello\nworld" | python3 script.py
```
Use -e to handle escape sequences properly.

Why Line by Line?
    - Memory Efficiency: Processing one line at a time ensures that only a small chunk of data is stored and handled at any moment, which is crucial for very large input files or streams.

    - Immediate Feedback: Data can be acted upon immediately as it arrives, enabling responsive, real-time processing and output.