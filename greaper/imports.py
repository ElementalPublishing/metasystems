import os
import ast
import difflib
import importlib.util
import sys

UTILITY_DIR = os.path.dirname(os.path.abspath(__file__))
SELF_PATH = os.path.abspath(__file__)

def find_all_py_files(directory):
    py_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                if os.path.abspath(full_path) != SELF_PATH:
                    py_files.append(full_path)
    return py_files

def find_best_matches(module_path, base_dir):
    candidates = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        rel_dir = os.path.relpath(dirpath, base_dir)
        if rel_dir == ".":
            rel_dir = ""
        for d in dirnames:
            mod = ".".join(filter(None, [rel_dir.replace(os.sep, "."), d]))
            candidates.append(mod)
        for f in filenames:
            if f.endswith(".py"):
                mod = ".".join(filter(None, [rel_dir.replace(os.sep, "."), f[:-3]]))
                candidates.append(mod)
    matches = difflib.get_close_matches(module_path, candidates, n=3)
    return matches

def suggest_import_fix(import_line, module_path, base_dir):
    matches = find_best_matches(module_path, base_dir)
    if matches:
        suggestions = []
        for match in matches:
            if import_line.startswith("import "):
                suggestions.append(f"import {match}")
            elif import_line.startswith("from "):
                suggestions.append(import_line.replace(module_path, match, 1))
        return suggestions
    return None

def is_builtin_or_installed(module_name):
    try:
        return importlib.util.find_spec(module_name) is not None
    except Exception:
        return False

def module_exists(module_path, base_dir):
    mod_path = os.path.join(base_dir, *module_path.split("."))
    candidates = [
        mod_path,
        mod_path + ".py",
        mod_path + ".pyc",
        mod_path + ".pyd",
        mod_path + ".so",
        mod_path + ".dll",
    ]
    # Check for namespace package (folder exists, no __init__.py)
    if os.path.isdir(mod_path):
        print(f"  [LOG] Found namespace package or directory: {mod_path}")
        return True
    # Check for any file type
    for candidate in candidates[1:]:
        if os.path.isfile(candidate):
            print(f"  [LOG] Found file: {candidate}")
            return True
    # Check for zip/egg/wheel on sys.path
    for path in sys.path:
        for ext in [".zip", ".egg", ".whl"]:
            archive_path = os.path.join(path, module_path + ext)
            if os.path.isfile(archive_path):
                print(f"  [LOG] Found archive: {archive_path}")
                return True
    # Case-insensitive check (for Windows/macOS)
    for candidate in candidates[1:]:
        dir_name = os.path.dirname(candidate)
        base_name = os.path.basename(candidate).lower()
        if os.path.isdir(dir_name):
            for f in os.listdir(dir_name):
                if f.lower() == base_name:
                    print(f"  [LOG] Found case-insensitive match: {os.path.join(dir_name, f)}")
                    return True
    # Symlink check
    if os.path.islink(mod_path):
        print(f"  [LOG] Found symlink: {mod_path}")
        return True
    return False

def check_imports(py_file, base_dir):
    discrepancies = []
    with open(py_file, "r", encoding="utf-8") as f:
        try:
            source = f.read()
            tree = ast.parse(source, filename=py_file)
        except Exception as e:
            error_line = None
            try:
                import re
                match = re.search(r'line (\d+)', str(e))
                if match:
                    error_line = int(match.group(1))
            except Exception:
                pass
            print("\n" + "-" * 70)
            print(f"SYNTAX ERROR in file: {py_file}")
            print(f"Error details: {e}")
            print("Context (first 10 lines):")
            with open(py_file, "r", encoding="utf-8") as f2:
                for i, line in enumerate(f2, 1):
                    prefix = ">>>" if error_line and i == error_line else "   "
                    print(f"{prefix} {i:3}: {line.rstrip()}")
                    if i >= 10:
                        break
            print("-" * 70)
            print("Suggestion: Please fix the syntax error above (see highlighted line) before checking imports.\n")
            discrepancies.append((1, "SYNTAX ERROR", str(e), None, None))
            return discrepancies
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_path = alias.name
                if is_builtin_or_installed(module_path.split('.')[0]):
                    print(f"  [LOG] '{module_path}' is a built-in or installed module.")
                    continue
                if module_exists(module_path, base_dir):
                    continue
                import_line = f"import {alias.name}"
                reason = f"Module '{module_path}' could not be resolved locally or as a known extension/module type"
                suggestions = suggest_import_fix(import_line, module_path, base_dir)
                discrepancies.append((node.lineno, import_line, reason, module_path, suggestions))
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            module_path = node.module
            if is_builtin_or_installed(module_path.split('.')[0]):
                print(f"  [LOG] '{module_path}' is a built-in or installed module.")
                continue
            # Handle relative imports
            if node.level > 0:
                rel_path = os.path.dirname(py_file)
                for _ in range(node.level):
                    rel_path = os.path.dirname(rel_path)
                mod_path = os.path.join(rel_path, *module_path.split(".")) if module_path else rel_path
            else:
                mod_path = os.path.join(base_dir, *module_path.split("."))
            if module_exists(module_path, base_dir):
                continue
            import_line = f"from {'.' * node.level + (module_path or '')} import ..."
            reason = f"Module '{module_path}' could not be resolved locally or as a known extension/module type"
            suggestions = suggest_import_fix(import_line, module_path, base_dir)
            discrepancies.append((node.lineno, import_line, reason, module_path, suggestions))
    return discrepancies

def fix_import_in_file(py_file, lineno, old_line, new_line):
    with open(py_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    idx = lineno - 1
    if 0 <= idx < len(lines):
        if old_line.strip() in lines[idx]:
            lines[idx] = lines[idx].replace(old_line.strip(), new_line)
            with open(py_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"    -> Fixed line {lineno}: {new_line}")
        else:
            import_part = old_line.strip().split()[0]
            if import_part in lines[idx]:
                print(f"    Current line {lineno}: {lines[idx].rstrip()}")
                confirm = input(f"    Replace this line with:\n    {new_line}\n    Proceed? (y/n): ").strip().lower()
                if confirm == "y":
                    lines[idx] = new_line + "\n"
                    with open(py_file, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    print(f"    -> Fixed line {lineno}: {new_line}")
                else:
                    print(f"    -> Skipped fixing line {lineno}.")
            else:
                print(f"    -> Could not auto-fix line {lineno} (line mismatch).")

if __name__ == "__main__":
    print("=" * 70)
    print("PYTHON IMPORTS TEST UTILITY".center(70))
    print(f"Running from: {UTILITY_DIR}".center(70))
    print("=" * 70)
    print("Searching for all .py files in this directory and all subdirectories...\n")

    py_files = find_all_py_files(UTILITY_DIR)
    broken_files = []
    for f in py_files:
        discrepancies = check_imports(f, UTILITY_DIR)
        if discrepancies:
            broken_files.append((f, discrepancies))

    if not broken_files:
        print("All Python files have valid imports.")
    else:
        print(f"Found {len(broken_files)} Python file(s) with broken imports:\n")
        print("-" * 70)
        for idx, (f, discrepancies) in enumerate(broken_files, 1):
            rel_path = os.path.relpath(f, UTILITY_DIR)
            print(f"{idx:3}. {rel_path}")
            for lineno, import_stmt, reason, module_path, suggestions in discrepancies:
                print(f"     [Line {lineno}] {import_stmt} --> {reason}")
                if module_path and is_builtin_or_installed(module_path.split('.')[0]):
                    print(f"         Suggestion: This import refers to an installed package. Make sure '{module_path.split('.')[0]}' is installed (e.g., pip install {module_path.split('.')[0]}).")
                elif "SYNTAX ERROR" in import_stmt:
                    print("         Suggestion: This file has a syntax error and cannot be parsed. Please fix the syntax before checking imports.")
                elif suggestions:
                    print("         Suggested fix(es):")
                    for sidx, suggestion in enumerate(suggestions, 1):
                        print(f"           {sidx}. {suggestion}")
                    user = input("         Apply one of these fixes? Enter number or n to skip: ").strip().lower()
                    if user.isdigit():
                        sidx = int(user) - 1
                        if 0 <= sidx < len(suggestions):
                            fix_import_in_file(f, lineno, import_stmt, suggestions[sidx])
                    else:
                        print("         Skipped.")
                else:
                    print("         No suggestion available.")
        print("-" * 70)
        print(f"Total: {len(broken_files)} Python file(s) with broken imports.")
    print("=" * 70)