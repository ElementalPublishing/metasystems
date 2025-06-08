import os
import argparse
from typing import List

# This gives you the absolute path to the folder containing this script
UTILITY_DIR = os.path.dirname(os.path.abspath(__file__))

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
    print("=" * 70)
    print("PYTHON FILE FINDER UTILITY".center(70))
    print(f"Running from: {UTILITY_DIR}".center(70))
    print("=" * 70)
    print("What would you like to do?")
    print("  1. Find all .py files in the current directory")
    print("  2. Input a directory to search")
    print("  Type 'exit' at any prompt to quit.")
    print("-" * 70)
    choice = input("Enter 1 or 2: ").strip()
    if choice.lower() == "exit":
        print("Exiting. Goodbye!")
        return

    if choice == "1":
        directory = os.getcwd()
        print(f"\nSearching in current directory: {directory}")
    elif choice == "2":
        directory = input("Enter the full path to the directory you want to search:\n> ").strip()
        if directory.lower() == "exit":
            print("Exiting. Goodbye!")
            return
        if not directory:
            print("No directory entered. Exiting.")
            return
        print(f"\nSearching in: {directory}")
    elif choice.lower() == "exit":
        print("Exiting. Goodbye!")
        return
    else:
        print("Invalid choice. Exiting.")
        return

    parser = argparse.ArgumentParser(
        description="Find all Python (.py) files in a directory (optionally recursively)."
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
    args, unknown = parser.parse_known_args()

    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"\nERROR: '{directory}' is not a valid directory.")
        return

    py_files = find_py_files(directory, recursive=not args.non_recursive)

    print("\n" + "=" * 70)
    if args.count:
        print(f"TOTAL PYTHON FILES FOUND: {len(py_files)}")
    else:
        if not py_files:
            print("No Python files found in the specified directory.")
        else:
            print(f"PYTHON FILES FOUND IN '{directory}':\n")
            for idx, f in enumerate(py_files, 1):
                if args.show_size:
                    try:
                        size = os.path.getsize(f)
                        print(f"{idx:3}. {f}  [{size:,} bytes]")
                    except Exception:
                        print(f"{idx:3}. {f}  [size unavailable]")
                else:
                    print(f"{idx:3}. {f}")
            print("-" * 70)
            print(f"TOTAL: {len(py_files)} Python file(s) found.")
    print("=" * 70)

if __name__ == "__main__":
    main()