import os
import ast
import re
from pathlib import Path

def find_math_functions(source_code):
    """Find functions that use math operators."""
    tree = ast.parse(source_code)
    math_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, (ast.BinOp, ast.UnaryOp)):
                    math_funcs.append(node)
                    break
    return math_funcs

def find_hardware_functions(source_code):
    """Find functions that use multiprocessing/threading."""
    tree = ast.parse(source_code)
    hardware_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if (isinstance(child, ast.Attribute) and
                    (child.attr in ["Process", "Thread", "Pool"])):
                    hardware_funcs.append(node)
                    break
                if (isinstance(child, ast.Name) and
                    child.id in ["multiprocessing", "threading"]):
                    hardware_funcs.append(node)
                    break
    return hardware_funcs

def collect_imports(func):
    """Collect import statements needed for a function."""
    imports = set()
    aliases = {
        "np": "import numpy as np",
        "pd": "import pandas as pd",
        "urlparse": "from urllib.parse import urlparse",
        "as_completed": "from concurrent.futures import as_completed",
        "ThreadPoolExecutor": "from concurrent.futures import ThreadPoolExecutor",
        "RobotsRules": "from .robots_rules import RobotsRules",
    }
    for node in ast.walk(func):
        if isinstance(node, ast.Name):
            if node.id in aliases:
                imports.add(aliases[node.id])
            elif node.id in {"math", "re", "time", "os", "sys", "threading", "multiprocessing"}:
                imports.add(f"import {node.id}")
        if isinstance(node, ast.Attribute):
            if node.attr in {"Process", "Thread", "Pool"}:
                imports.add("import multiprocessing")
    return imports

def guess_arg_type(arg_name):
    """Annotate arguments for Cython. Only 'self' is left untyped."""
    return arg_name if arg_name == "self" else f"float {arg_name}"

def guess_return_type(func):
    """Guess return type: float if returns a BinOp, object if returns any value, void if only bare return or no return."""
    for stmt in func.body:
        if isinstance(stmt, ast.Return):
            if stmt.value is None:
                continue
            elif isinstance(stmt.value, ast.BinOp):
                return "float"
            else:
                return "object"
    return "void"

def function_has_supported_body(func):
    """Disallow async, yield, lambda, etc."""
    for stmt in func.body:
        if isinstance(stmt, (ast.Lambda, ast.Yield, ast.YieldFrom, ast.AsyncFunctionDef)):
            return False
    return True

def annotate_parents(tree):
    """Annotate AST nodes with parent pointers."""
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent

def generate_pyx(functions, output_path):
    """Write a .pyx file for the given functions."""
    if not functions:
        return
    # Annotate parents for method detection
    annotate_parents(ast.Module(body=functions))
    all_imports = set()
    for func in functions:
        all_imports |= collect_imports(func)
    with open(output_path, "w", encoding="utf-8") as f:
        for imp in sorted(all_imports):
            f.write(f"{imp}\n")
        if all_imports:
            f.write("\n")
        for func in functions:
            is_method = hasattr(func, "parent") and isinstance(func.parent, ast.ClassDef)
            func_name = func.name
            arg_names = [arg.arg for arg in func.args.args]
            if is_method and (not arg_names or arg_names[0] != "self"):
                arg_names = ["self"] + arg_names
            args_str = ", ".join([guess_arg_type(name) for name in arg_names])
            ret_type = guess_return_type(func)
            if ret_type == "float":
                f.write(f"cpdef float {func_name}({args_str}):\n")
            elif ret_type == "object":
                f.write(f"cpdef object {func_name}({args_str}):\n")
            elif ret_type == "void":
                f.write(f"cpdef void {func_name}({args_str}):\n")
            else:
                args_joined = ", ".join(arg_names)
                f.write(f"def {func_name}({args_joined}):\n")
            unsupported = False
            has_return = False
            for stmt in func.body:
                # Skip unsupported statements
                if isinstance(stmt, (ast.Lambda, ast.Yield, ast.YieldFrom, ast.AsyncFunctionDef)):
                    f.write("    # Skipped: unsupported closure/generator/async\n    pass\n")
                    unsupported = True
                    break
                try:
                    src = ast.unparse(stmt)
                except Exception:
                    f.write("    # Skipped: could not unparse statement\n    pass\n")
                    continue
                # Remove f-string markers and curly braces (Cython can't parse them)
                src = src.replace("f'", "'").replace('f"', '"')
                src = src.replace("{", "").replace("}", "")
                src = fix_common_syntax_issues(src)
                # Check for return in float functions
                if ret_type == "float" and isinstance(stmt, ast.Return):
                    has_return = True
                    if not isinstance(stmt.value, ast.BinOp):
                        f.write("    # Skipped: non-math return in float function\n    pass\n")
                        unsupported = True
                        break
                # If assignment has no value, skip or comment
                if isinstance(stmt, ast.Assign):
                    if not hasattr(stmt, "value") or stmt.value is None:
                        f.write("    # Skipped: incomplete assignment\n    pass\n")
                        continue
                src = "\n".join("    " + line for line in src.splitlines())
                f.write(src + "\n")
            if ret_type == "float" and not has_return:
                f.write("    return 0.0\n")
            if not unsupported and not func.body:
                f.write("    pass\n")
            f.write("\n")
            if not function_has_supported_body(func):
                f.write(f"def {func.name}():\n    # Skipped: unsupported closure/generator/async\n    pass\n\n")

def generate_setup_py(pyx_filename, output_path):
    """Write a setup.py for the given .pyx file."""
    setup_code = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{pyx_filename}")
)
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(setup_code.strip())

def cythonize_all(root_folder, scan_subfolders=True):
    """Main entry: scan for .py files, generate .pyx and setup.py for math/hardware functions."""
    created_files = []
    checked_files = []
    print(f"Scanning '{root_folder}' for Python files...")
    for dirpath, _, filenames in os.walk(root_folder):
        if not scan_subfolders and dirpath != root_folder:
            continue
        print(f"  Entering directory: {dirpath}")
        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("setup"):
                py_path = os.path.join(dirpath, filename)
                checked_files.append(py_path)
                print(f"    Found file: {filename}")
                print(f"      Checking {py_path} for math-heavy/hardware functions...")
                with open(py_path, "r", encoding="utf-8") as f:
                    source = f.read()
                math_funcs = find_math_functions(source)
                hardware_funcs = find_hardware_functions(source)
                all_funcs = {f.name: f for f in math_funcs + hardware_funcs}.values()
                if not all_funcs:
                    print(f"        Skipped: No math-heavy or hardware functions found in {py_path}")
                    continue
                base = Path(filename).stem
                pyx_file = os.path.join(dirpath, f"{base}_cykernel.pyx")
                setup_file = os.path.join(dirpath, "setup.py")
                generate_pyx(list(all_funcs), pyx_file)
                generate_setup_py(f"{base}_cykernel.pyx", setup_file)
                print(f"        Generated {pyx_file} and {setup_file}")
                created_files.append((pyx_file, setup_file))
    if created_files:
        print("\nSummary of created files:")
        for pyx, setup in created_files:
            print(f"  {pyx}\n  {setup}")
    else:
        print("\nNo Cython files were created.")
    if checked_files:
        print("\nChecked the following Python files:")
        for f in checked_files:
            print(f"  {f}")
    else:
        print("\nNo Python files were found to check.")

def fix_common_syntax_issues(line):
    # Fix mismatched brackets/parentheses
    line = re.sub(r"\[([^\]]*)\)", r"[\1]", line)
    line = re.sub(r"\(([^\)]*)\]", r"(\1)", line)
    line = re.sub(r"\(([^\)]*)\}", r"(\1)", line)
    line = re.sub(r"\{([^\}]*)\}", r"{\1}", line)
    # Aggressively balance
    pairs = [("(", ")"), ("[", "]"), ("{", "}")]
    for open_c, close_c in pairs:
        diff = line.count(open_c) - line.count(close_c)
        if diff > 0:
            line = line.rstrip("\n") + (close_c * diff) + "\n"
    # Remove unmatched quotes at end of line
    if line.count("'") % 2 != 0:
        line = line.rstrip("\n") + "'\n"
    if line.count('"') % 2 != 0:
        line = line.rstrip("\n") + '"\n'
    return line

if __name__ == "__main__":
    scan = input("Are there subfolders to scan in 'metasystems'? (y/n): ").strip().lower()
    scan_subfolders = scan == "y"
    cythonize_all(".", scan_subfolders)