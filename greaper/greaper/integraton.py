"""
Integration layer for Greaper.
Provides high-level functions to connect Greaper's core features with external tools, editors, and scripts.
"""

from greaper.core import search_files

import json
import csv
import io

# --- VS Code Integration ---
def export_for_vscode(pattern, path=".", **kwargs):
    """
    Export results in VS Code 'problems' format: file:line: matched line
    """
    results = search_files(pattern=pattern, path=path, **kwargs)
    return "\n".join(f"{r[0]}:{r[1]}: {r[2]}" for r in results)

# --- Sublime Text Integration ---
def export_for_sublime(pattern, path=".", **kwargs):
    """
    Export results in Sublime Text 'Find Results' format.
    """
    results = search_files(pattern=pattern, path=path, **kwargs)
    output = []
    last_file = None
    for r in results:
        if r[0] != last_file:
            output.append(f"{r[0]}:")
            last_file = r[0]
        output.append(f"  {r[1]}: {r[2]}")
    return "\n".join(output)

# --- JetBrains IDEs (PyCharm, IntelliJ, etc.) Integration ---
def export_for_jetbrains(pattern, path=".", **kwargs):
    """
    Export results in JetBrains 'Find in Path' format: file(line): matched line
    """
    results = search_files(pattern=pattern, path=path, **kwargs)
    return "\n".join(f"{r[0]}({r[1]}): {r[2]}" for r in results)

# --- Vim/Neovim Quickfix Integration ---
def export_for_vim_quickfix(pattern, path=".", **kwargs):
    """
    Export results in Vim/Neovim quickfix format: file:line:col: matched line
    (col is always 1 for now; can be improved with match highlighting)
    """
    results = search_files(pattern=pattern, path=path, **kwargs)
    return "\n".join(f"{r[0]}:{r[1]}:1: {r[2]}" for r in results)

# --- Emacs Compilation Buffer Integration ---
def export_for_emacs(pattern, path=".", **kwargs):
    """
    Export results in Emacs compilation buffer format: file:line: matched line
    """
    results = search_files(pattern=pattern, path=path, **kwargs)
    return "\n".join(f"{r[0]}:{r[1]}: {r[2]}" for r in results)

# --- JSON/CSV/Markdown Export for Data Science/Reporting ---
def export_as_json(pattern, path=".", export_path=None, **kwargs):
    results = search_files(pattern=pattern, path=path, **kwargs)
    output = json.dumps(results, indent=2)
    if export_path:
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output

def export_as_csv(pattern, path=".", export_path=None, **kwargs):
    results = search_files(pattern=pattern, path=path, **kwargs)
    output_io = io.StringIO()
    writer = csv.writer(output_io)
    writer.writerow(["file", "line_number", "line", "before", "after"])
    for row in results:
        writer.writerow(row)
    output = output_io.getvalue()
    if export_path:
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output

def export_as_markdown(pattern, path=".", export_path=None, **kwargs):
    results = search_files(pattern=pattern, path=path, **kwargs)
    output = "| File | Line | Match |\n|------|------|-------|\n"
    for r in results:
        output += f"| `{r[0]}` | {r[1]} | `{r[2]}` |\n"
    if export_path:
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output

# --- Batch Replace Integration (for scripting/editors) ---
def batch_replace_and_export(pattern, replacement, path=".", export_path=None, **kwargs):
    """
    Run batch replace and export a report of changes.
    """
    from greaper.core import batch_replace_files  # You'd implement this in core.py
    changes = batch_replace_files(pattern, replacement, path=path, **kwargs)
    output = json.dumps(changes, indent=2)
    if export_path:
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output

# --- HuggingFace Transformers Integration ---
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

def hf_summarize_code(code, model_name="Salesforce/codet5-base-multi-sum"):
    """
    Use HuggingFace Transformers to summarize code locally or via HuggingFace Hub.
    Example model: Salesforce/codet5-base-multi-sum
    """
    if pipeline is None:
        raise ImportError("transformers package not installed. Run 'pip install transformers'")
    summarizer = pipeline("summarization", model=model_name)
    # HuggingFace models may have input length limits; truncate if needed
    code = code[:1024]
    summary = summarizer(code, max_length=128, min_length=16, do_sample=False)
    return summary[0]['summary_text']

# Example usage:
# summary = hf_summarize_code("def foo(x):\n    return x + 1")