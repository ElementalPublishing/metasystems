# UTILS.md

## Python File Finder & Import Refactor Utility

This utility helps you quickly locate all `.py` (Python) files in a specified directory and its subdirectories.  
**It is also designed to help you refactor `import` and `from ... import ...` statements** across your codebase, making it easy to reorganize, move, or restructure your Python project.

---

### Location

`greaper/utils/find_py_files.py`

---

## Usage

Run from your project root or any directory:

```sh
python -m greaper.utils.find_py_files [directory] [options]
```

- If no directory is specified, it defaults to the current directory.

---

## Options

| Option                  | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| `directory`             | Directory to search (default: current directory)                 |
| `-n`, `--non-recursive` | Only search the top-level directory (do not search subdirectories)|
| `-c`, `--count`         | Show only the count of `.py` files found                        |
| `-s`, `--show-size`     | Show file sizes in bytes                                        |

---

## Examples

- **Find all Python files recursively in the current directory:**
  ```
  python -m greaper.utils.find_py_files
  ```

- **Find all Python files in a specific directory:**
  ```
  python -m greaper.utils.find_py_files path/to/your/folder
  ```

- **Only search the top-level directory:**
  ```
  python -m greaper.utils.find_py_files path/to/your/folder -n
  ```

- **Show only the count of Python files:**
  ```
  python -m greaper.utils.find_py_files -c
  ```

- **Show file sizes for each Python file:**
  ```
  python -m greaper.utils.find_py_files -s
  ```

---

## Output

- Lists all `.py` files found, optionally with their sizes.
- Prints a summary with the total number of files found.
- If `--count` is used, only the count is displayed.

---

## Error Handling

- If the specified directory does not exist, a clear error message is shown.
- If no Python files are found, a message is displayed.

---

## Extending

You can use or modify this utility as a base for more advanced codebase analysis, such as:
- Searching for specific code patterns
- Refactoring imports
- Batch processing Python files

---