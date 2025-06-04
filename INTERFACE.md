# Meta Systems Interface Specification

This document defines the standard interface for all meta systems to ensure seamless integration and synergy within the `mainframe` orchestrator.

---

## 1. Entry Point

Each meta system **must** provide a `main()` function as its entry point.

```python
def main(*args):
    """
    Entry point for the meta system.
    Args:
        *args: Command-line style arguments as strings, passed from mainframe or CLI.
    """
    # Implementation here
```

---

## 2. Arguments

- All arguments are passed as strings, similar to how they would be entered on the command line.
- Arguments should be parsed using standard Python techniques (e.g., `argparse`, manual parsing, or simple indexing).
- If no arguments are provided, the program should display usage/help information.

---

## 3. Output

- Output should be printed to the console (stdout) or written to a file in a clear, human-readable format (e.g., Markdown, JSON, or plain text).
- If the program generates files, print the file path(s) to the console.
- Errors and warnings should be clearly indicated.

---

## 4. Example

```python
# Example meta system: exampletool.py

def main(*args):
    if not args:
        print("Usage: exampletool.py <input>")
        return
    input_value = args[0]
    print(f"Processing: {input_value}")
    # ... do work ...
    print("Done!")
```

---

## 5. Best Practices

- Keep the core logic separate from input/output handling for easier reuse and testing.
- Document any required or optional arguments at the top of your script or in a help message.
- Ensure your `main()` function can be called both from the CLI and from the mainframe orchestrator.

---

## 6. Adding a New Meta System

1. Create a new `.py` file in the metasystems directory.
2. Implement a `main(*args)` function as described above.
3. (Optional) Add documentation or usage instructions at the top of your script.

---

By following this interface, all your meta systems will be interoperable, discoverable, and easily orchestrated by the mainframe.