"""
Mainframe: The System Connector

This program is designed as a true system, not just a launcher.
It connects your metasystems, enabling interaction, data sharing, and emergent workflows.
The architecture is modular, extensible, and focused on synergy—so the whole becomes greater than the sum of its parts.
"""

import importlib
import sys
import os
import ast
import inspect
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- ECS Component Defaults ---
DEFAULT_COMPONENTS = {
    "tags": [],
    "dependencies": [],
    "status": "idle",
    "config": {},
    "result": None,
    "documentation": "",
    "created": None,
    "last_run": None,
    "author": "",
    "visualization_hints": {},
    "permissions": [],
    "metrics": {},
}

# Discover all metasystem modules in the current directory (except mainframe itself)
def discover_systems():
    systems = {}
    for fname in os.listdir(os.path.dirname(__file__)):
        if fname.endswith(".py") and fname not in ("mainframe.py", "__init__.py"):
            modname = fname[:-3]
            systems[modname] = modname
    return systems

AVAILABLE_SYSTEMS = discover_systems()

def analyze_outputs(filepath):
    outputs = []
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=filepath)
    for node in ast.walk(tree):
        # Detect file writes
        if (
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == "open"
        ):
            if len(node.args) >= 2:
                mode_arg = node.args[1]
                file_arg = node.args[0]
                # Python 3.8+: ast.Constant, before: ast.Str
                mode = getattr(mode_arg, "value", None) if isinstance(mode_arg, ast.Constant) else getattr(mode_arg, "s", None)
                filename = getattr(file_arg, "value", None) if isinstance(file_arg, ast.Constant) else getattr(file_arg, "s", None)
                if mode and "w" in mode:
                    if filename:
                        outputs.append(
                            {
                                "type": "file",
                                "filename": filename,
                                "mode": mode,
                                "description": "File written by program",
                            }
                        )
        # Detect print statements
        if (
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == "print"
        ):
            outputs.append(
                {
                    "type": "console",
                    "description": "Prints output to the terminal",
                }
            )
    return outputs

def scan_for_metadata(module):
    # Try to extract docstring from main()
    if hasattr(module, "main"):
        doc = inspect.getdoc(module.main)
        if doc:
            return {"description": doc}
    # Try to find argparse or top-level comments
    try:
        source = inspect.getsource(module)
        if "argparse" in source:
            return {"description": "This module uses argparse. Run with --help for options."}
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                return {"description": node.value.s}
    except Exception:
        pass
    return {"description": "No metadata or docstring found."}

def get_metadata_and_outputs(system_name):
    filepath = os.path.join(os.path.dirname(__file__), f"{system_name}.py")
    # Brute force: scan for metadata and outputs in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_meta = executor.submit(lambda: scan_for_metadata(importlib.import_module(system_name)))
        future_outputs = executor.submit(lambda: analyze_outputs(filepath))
        meta = future_meta.result()
        outputs = future_outputs.result()
    return meta, outputs

def analyze_inputs(filepath):
    """
    Analyze the Python file to detect likely input arguments for main() and CLI usage.
    Looks for main() function arguments and input() calls.
    """
    inputs = []
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=filepath)
    # Detect main() function arguments
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for arg in node.args.args:
                if arg.arg != "self":
                    inputs.append(
                        {
                            "type": "argument",
                            "name": arg.arg,
                            "description": f"Argument for main(): {arg.arg}",
                        }
                    )
    # Detect input() calls
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == "input"
        ):
            prompt = ""
            if node.args:
                arg0 = node.args[0]
                if isinstance(arg0, ast.Constant):  # Python 3.8+
                    prompt = arg0.value
                elif hasattr(arg0, "s"):  # Python <3.8
                    prompt = arg0.s
            inputs.append(
                {
                    "type": "input",
                    "description": f"User input requested: {prompt}" if prompt else "User input requested",
                }
            )
    return inputs

def analyze_tags(filepath):
    tags = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Look for tags in comments like: # tags: foo, bar
            if "# tags:" in line.lower():
                tag_line = line.split(":", 1)[1]
                tags.update(tag.strip() for tag in tag_line.split(","))
            # Look for @tag in comments
            if "#@" in line:
                tags.update(tag.strip("#@ \n") for tag in line.split() if tag.startswith("#@"))
    return list(tags)

def analyze_dependencies(filepath):
    dependencies = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Look for dependencies in comments: # depends: foo, bar
            if "# depends:" in line.lower():
                dep_line = line.split(":", 1)[1]
                dependencies.update(dep.strip() for dep in dep_line.split(","))
            # Look for import statements
            if line.strip().startswith("import "):
                dep = line.strip().split()[1]
                dependencies.add(dep)
            elif line.strip().startswith("from "):
                dep = line.strip().split()[1]
                dependencies.add(dep)
    return list(dependencies)

def analyze_documentation(filepath):
    # Try to extract module-level docstring
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source)
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
            return tree.body[0].value.s
    except Exception:
        pass
    return ""

def analyze_author(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "__author__" in line or "# author:" in line.lower():
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""

def analyze_visualization_hints(filepath):
    # Look for # viz: {...} or # visualization: {...}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# viz:" in line.lower() or "# visualization:" in line.lower():
                try:
                    hint = line.split(":", 1)[1].strip()
                    return json.loads(hint)
                except Exception:
                    pass
    return {}

def analyze_permissions(filepath):
    # Look for # permissions: admin, user
    permissions = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# permissions:" in line.lower():
                perm_line = line.split(":", 1)[1]
                permissions.update(perm.strip() for perm in perm_line.split(","))
    return list(permissions)

def analyze_metrics(filepath):
    # Look for # metrics: {...}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# metrics:" in line.lower():
                try:
                    metric = line.split(":", 1)[1].strip()
                    return json.loads(metric)
                except Exception:
                    pass
    return {}

def analyze_config(filepath):
    # Look for # config: {...}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# config:" in line.lower():
                try:
                    config = line.split(":", 1)[1].strip()
                    return json.loads(config)
                except Exception:
                    pass
    return {}

def analyze_status(filepath):
    # Look for # status: running, idle, etc.
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# status:" in line.lower():
                return line.split(":", 1)[1].strip().lower()
    return "idle"

def analyze_result(filepath):
    # Look for # result: some result or # result: {...}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# result:" in line.lower():
                result = line.split(":", 1)[1].strip()
                try:
                    return json.loads(result)
                except Exception:
                    return result
    return None

def analyze_created(filepath):
    # Look for # created: 2024-06-04T12:00:00 or similar
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# created:" in line.lower():
                return line.split(":", 1)[1].strip()
    return None

def analyze_last_run(filepath):
    # Look for # last_run: 2024-06-04T12:00:00 or similar
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "# last_run:" in line.lower():
                return line.split(":", 1)[1].strip()
    return None

def run_system(system_name, *args):
    if system_name not in AVAILABLE_SYSTEMS:
        print(f"System '{system_name}' not found.")
        return
    meta, outputs = get_metadata_and_outputs(system_name)
    filepath = os.path.join(os.path.dirname(__file__), f"{system_name}.py")
    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()
    # Consolidate duplicate detected_outputs
    unique_outputs = []
    seen = set()
    for out in outputs:
        key = (out.get("type"), out.get("description"))
        if key not in seen:
            unique_outputs.append(out)
            seen.add(key)
    # Detect and consolidate inputs
    inputs = analyze_inputs(filepath)
    unique_inputs = []
    seen_inputs = set()
    for inp in inputs:
        key = (inp.get("type"), inp.get("name", ""), inp.get("description", ""))
        if key not in seen_inputs:
            unique_inputs.append(inp)
            seen_inputs.add(key)
    formatted_code = "\n".join(line.rstrip() for line in source_code.splitlines())

    # --- ECS Component Data Assembly ---
    output_info = {
        "system": system_name,
        "description": meta.get("description") if meta else "",
        "detected_inputs": unique_inputs,
        "detected_outputs": unique_outputs,
        "source_code": formatted_code,
        "tags": analyze_tags(filepath),
        "dependencies": analyze_dependencies(filepath),
        "status": analyze_status(filepath),
        "config": analyze_config(filepath),
        "result": analyze_result(filepath),
        "documentation": analyze_documentation(filepath),
        "created": analyze_created(filepath),
        "last_run": analyze_last_run(filepath),
        "author": analyze_author(filepath),
        "visualization_hints": analyze_visualization_hints(filepath),
        "permissions": analyze_permissions(filepath),
        "metrics": analyze_metrics(filepath),
    }
    json_filename = f"{system_name}_analysis.json"
    with open(json_filename, "w", encoding="utf-8") as jf:
        json.dump(output_info, jf, indent=2, ensure_ascii=False)
    print(f"Analysis written to {json_filename}")
    module = importlib.import_module(AVAILABLE_SYSTEMS[system_name])
    if hasattr(module, "main"):
        module.main(*args)
    else:
        print(f"Module '{system_name}' does not have a main() function.")

def main():
    print("=== Mainframe: Your Connected Meta Systems ===")
    print("This platform is designed for synergy, interaction, and emergent workflows.")
    while True:
        print("\nWhich meta system do you want to run?")
        print("Available meta systems:")
        for name in sorted(AVAILABLE_SYSTEMS):
            print(f" - {name}")
        print("Type the name of a system to run it, or 'exit' to quit.")
        system = input("\nSystem> ").strip()
        if system.lower() == "exit":
            print("Goodbye!")
            break
        if system not in AVAILABLE_SYSTEMS:
            print("Not found. Try again.")
            continue
        args = input(f"Arguments for {system} (space-separated, or leave blank): ").strip().split()
        run_system(system, *args)

if __name__ == "__main__":
    main()