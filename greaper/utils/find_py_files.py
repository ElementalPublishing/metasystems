import os
import argparse
from typing import List

def find_py_files(directory: str, recursive: bool = True) -> List[str]:
    """Find all .py files in the given directory (and optionally subdirectories)."""
    py_files = []
    if recursive:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".py"):
                    py_files.append(os.path.join(dirpath, filename))
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                py_files.append(os.path.join(directory, filename))
    return py_files

def main():
    parser = argparse.ArgumentParser(
        description="Find all Python (.py) files in a directory (optionally recursively)."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search (default: current directory)"
    )
    parser.add_argument(
        "-n", "--non-recursive",
        action="store_true",
        help="Only search the top-level directory (not subdirectories)"
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Show only the count of .py files found"
    )
    parser.add_argument(
        "-s", "--show-size",
        action="store_true",
        help="Show file sizes in bytes"
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    py_files = find_py_files(directory, recursive=not args.non_recursive)

    if args.count:
        print(f"Found {len(py_files)} Python file(s) in '{directory}'.")
    else:
        if not py_files:
            print("No Python files found.")
        else:
            print(f"Python files in '{directory}':\n")
            for f in py_files:
                if args.show_size:
                    try:
                        size = os.path.getsize(f)
                        print(f"{f} ({size} bytes)")
                    except Exception:
                        print(f"{f} (size unavailable)")
                else:
                    print(f)
            print(f"\nTotal: {len(py_files)} file(s) found.")

if __name__ == "__main__":
    main()