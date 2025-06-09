import os
import importlib
from pathlib import Path

UTILS_DIR = Path(__file__).parent.parent / "utils"

def list_utilities():
    """List all utility modules in the utils folder (excluding __init__.py)."""
    return [
        f.stem for f in UTILS_DIR.glob("*.py")
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

def run_utility(name, *args):
    """Import and run the main() function of a utility by name."""
    if name not in list_utilities():
        raise ValueError(f"Utility '{name}' not found in utils folder.")
    mod = importlib.import_module(f"utils.{name}")
    if hasattr(mod, "main"):
        return mod.main(*args)
    else:
        raise AttributeError(f"Utility '{name}' does not have a main() function.")

def get_utility_doc(name):
    """Get the docstring of a utility, if available."""
    if name not in list_utilities():
        return ""
    mod = importlib.import_module(f"utils.{name}")
    return mod.__doc__ or ""