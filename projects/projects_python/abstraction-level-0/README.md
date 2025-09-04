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
    python your_script.py < input.txt
```