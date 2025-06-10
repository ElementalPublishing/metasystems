import argparse
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def print_backend_info():
    """Print which fuzzy backend is being used."""
    try:
        from greaper.algorithms import fuzzy
        backend = getattr(fuzzy.levenshtein, "__module__", "")
        if "cython_ext" in backend:
            print("[INFO] Using Cython-accelerated fuzzy backend.")
        else:
            print("[INFO] Using pure Python fuzzy backend.")
    except Exception as e:
        print(f"[ERROR] Could not determine fuzzy backend: {e}")

def print_results(results, color=True, context=0):
    """Print search results in a table or plain text."""
    if not results:
        print("No matches found.")
        return

    if RICH_AVAILABLE and color:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("File", style="cyan")
        table.add_column("Line", style="yellow")
        table.add_column("Match", style="white")
        if context > 0:
            table.add_column("Context Before", style="dim")
            table.add_column("Context After", style="dim")

        for file, line, match, before, after in results:
            before_text = "\n".join(before) if context > 0 else ""
            after_text = "\n".join(after) if context > 0 else ""
            if context > 0:
                table.add_row(str(file), str(line), match, before_text, after_text)
            else:
                table.add_row(str(file), str(line), match)
        console.print(table)
        console.print(f"[bold green]{len(results)} match(es) found.[/bold green]")
    else:
        for file, line, match, before, after in results:
            if context > 0:
                for b in before:
                    print(f"{file}:{line-context+before.index(b)}- {b}")
            print(f"{file}:{line}: {match}")
            if context > 0:
                for a in after:
                    print(f"{file}:{line+after.index(a)+1}+ {a}")
        print(f"{len(results)} match(es) found.")

def prompt_option(name, current, example=None, opt_type=str):
    """Prompt the user for an option, with type conversion and default fallback."""
    prompt = f"{name} [{current}]"
    if example:
        prompt += f" (e.g. {example})"
    prompt += ": "
    val = input(prompt).strip()
    if not val:
        return current
    if opt_type == bool:
        return val.lower() in ("1", "y", "yes", "on", "true")
    if opt_type == int:
        try:
            return int(val)
        except ValueError:
            print("Invalid integer, using default.")
            return current
    return val

def search_command(args):
    """Handle the 'search' command interactively if needed."""
    print_backend_info()

    # Step 1: Pattern
    while True:
        pattern = args.pattern
        if not pattern:
            print("\nWhat would you like to search for?")
            print("Type 'back' to return to the previous menu, or 'exit' to quit.")
            pattern = input("Enter search pattern:\n> ").strip()
            if pattern.lower() == "exit":
                print("Exiting Greaper.")
                return
            if pattern.lower() == "back":
                print("Returning to main menu.")
                return
            if not pattern:
                print("No pattern entered. Please enter a pattern, or type 'exit' to quit.")
                continue
        break

    # Step 2: Path
    path = args.path
    if not path:
        print("\nWhere do you want to search?")
        print("Type 'back' to return to the previous step, or 'exit' to quit.")
        path = input("Enter path to search (default: .):\n> ").strip() or "."

    # Step 3: Options (with ability to edit)
    print("\nSearch options:")
    options = [
        ("fuzzy", args.fuzzy, "Use fuzzy search (y/n)", bool),
        ("ignore_case", args.ignore_case, "Case-insensitive search (y/n)", bool),
        ("word", args.word, "Match whole words only (y/n)", bool),
        ("context", args.context, "Show N lines of context", int),
        ("syntax_aware", args.syntax_aware, "Only match in comments/strings/code (y/n)", bool),
        ("syntax_mode", getattr(args, "syntax_mode", "all"), "Syntax mode (all/comment/string/code/mixed)", str),
        ("include", args.include, "Glob patterns to include (e.g. *.py *.md, space-separated)", list),
        ("exclude", args.exclude, "Glob patterns to exclude (e.g. *.log *.tmp, space-separated)", list),
        ("max_results", args.max_results, "Maximum number of results", int),
        ("no_color", args.no_color, "Disable color output (y/n)", bool),
        ("tui", args.tui if hasattr(args, "tui") else False, "Launch the Textual TUI interface (y/n)", bool),
    ]
    args_dict = interactive_prompt(options)
    for k, v in args_dict.items():
        setattr(args, k, v)

    # Step 4: Confirm
    print("\nReady to search with these settings:")
    print(f"  Pattern:      {pattern}")
    print(f"  Path:         {path}")
    print(f"  Fuzzy:        {'ON' if args.fuzzy else 'OFF'}")
    print(f"  Ignore case:  {'ON' if args.ignore_case else 'OFF'}")
    print(f"  Whole word:   {'ON' if args.word else 'OFF'}")
    print(f"  Context:      {args.context}")
    print(f"  Syntax aware: {'ON' if args.syntax_aware else 'OFF'}")
    print(f"  Syntax mode:  {args.syntax_mode}")
    print(f"  Include:      {' '.join(args.include)}")
    print(f"  Exclude:      {' '.join(args.exclude)}")
    print(f"  Max results:  {args.max_results}")
    print(f"  Color:        {'OFF' if args.no_color else 'ON'}")
    print(f"  TUI:          {'ON' if args.tui else 'OFF'}")
    print("\nProceed? (Y/n, or type 'back' to edit options, 'exit' to quit)")
    confirm = input("> ").strip().lower()
    if confirm == "exit":
        print("Exiting Greaper.")
        return
    if confirm == "back":
        return search_command(args)  # Restart options editing
    if confirm == "n":
        print("Search cancelled.")
        return

    # Step 5: Run search or launch TUI
    if hasattr(args, "tui") and args.tui:
        from greaper.gui_textual import GreaperApp
        GreaperApp.from_cli_args(args).run()
        return

    print(f"\n[CLI] Searching for '{pattern}' in '{path}' ...")
    try:
        from greaper.core import search_files
        results = search_files(
            pattern=pattern,
            path=path,
            fuzzy=args.fuzzy,
            ignore_case=args.ignore_case,
            word=args.word,
            context=args.context,
            include=args.include,
            exclude=args.exclude,
            max_results=args.max_results,
            syntax_aware=args.syntax_aware,
            syntax_mode=args.syntax_mode,
        )
        print_results(results, color=not args.no_color, context=args.context)

        # Prompt for next action after showing results
        while True:
            next_action = input("\nPress Enter to return to the main menu, or type 'exit' to quit: ").strip().lower()
            if next_action == "exit":
                print("Exiting Greaper.")
                exit(0)
            if next_action == "":
                return  # Return to main menu
            print("Invalid input. Please press Enter or type 'exit'.")
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")

def replace_command(args):
    """Handle the 'replace' command interactively."""
    print("\n[Replace Mode]")
    options = [
        ("pattern", args.pattern, "Pattern to search for", str),
        ("replacement", args.replacement, "Replacement text", str),
        ("path", args.path, "Path to search", str),
        ("fuzzy", args.fuzzy, "Use fuzzy search (y/n)", bool),
        ("ignore_case", args.ignore_case, "Case-insensitive search (y/n)", bool),
        ("preview", args.preview, "Preview changes before applying (y/n)", bool),
    ]
    args_dict = interactive_prompt(options)
    for k, v in args_dict.items():
        setattr(args, k, v)

    print("\nReady to replace with these settings:")
    print(f"  Pattern:      {args.pattern}")
    print(f"  Replacement:  {args.replacement}")
    print(f"  Path:         {args.path}")
    print(f"  Fuzzy:        {'ON' if args.fuzzy else 'OFF'}")
    print(f"  Ignore case:  {'ON' if args.ignore_case else 'OFF'}")
    print(f"  Preview:      {'ON' if args.preview else 'OFF'}")
    print("\nProceed? (Y/n, or type 'back' to edit options, 'exit' to quit)")
    confirm = input("> ").strip().lower()
    if confirm == "exit":
        print("Exiting Greaper.")
        return
    if confirm == "back":
        return replace_command(args)
    if confirm == "n":
        print("Replace cancelled.")
        return

    print(f"[CLI] Replace '{args.pattern}' with '{args.replacement}' in '{args.path}'")
    print(f"  Fuzzy: {args.fuzzy} | Ignore case: {args.ignore_case} | Preview: {args.preview}")
    # TODO: Implement replace logic

def export_command(args):
    """Handle the 'export' command interactively."""
    print("\n[Export Mode]")
    options = [
        ("pattern", "", "Pattern to search for", str),
        ("path", ".", "Path to search", str),
        ("format", "json", "Export format (vscode/sublime/jetbrains/vim/emacs/json/csv/md)", str),
        ("ignore_case", False, "Case-insensitive search (y/n)", bool),
        ("fuzzy", False, "Use fuzzy search (y/n)", bool),
        ("syntax_aware", False, "Syntax-aware search (y/n)", bool),
        ("syntax_mode", "all", "Syntax mode (all/comment/string/code/mixed)", str),
        ("include", ["*"], "Glob patterns to include", list),
        ("exclude", [], "Glob patterns to exclude", list),
        ("max_results", 1000, "Maximum number of results", int),
        ("export_path", "", "Export file path (optional)", str),
    ]
    args_dict = interactive_prompt(options)
    for k, v in args_dict.items():
        setattr(args, k, v)

    print(f"\nReady to export results to {args.format} format.")
    print("Proceed? (Y/n, or type 'back' to edit options, 'exit' to quit)")
    confirm = input("> ").strip().lower()
    if confirm == "exit":
        print("Exiting Greaper.")
        return
    if confirm == "back":
        return export_command(args)
    if confirm == "n":
        print("Export cancelled.")
        return

    print(f"[CLI] Exporting results to {args.format} format")
    from greaper.integraton import (
        export_for_vscode, export_for_sublime, export_for_jetbrains,
        export_for_vim_quickfix, export_for_emacs,
        export_as_json, export_as_csv, export_as_markdown
    )
    export_map = {
        "vscode": export_for_vscode,
        "sublime": export_for_sublime,
        "jetbrains": export_for_jetbrains,
        "vim": export_for_vim_quickfix,
        "emacs": export_for_emacs,
        "json": export_as_json,
        "csv": export_as_csv,
        "md": export_as_markdown,
        "markdown": export_as_markdown,
    }
    func = export_map.get(args.format.lower())
    if not func:
        print(f"[ERROR] Unknown export format: {args.format}")
        return

    output = func(
        pattern=args.pattern,
        path=args.path,
        ignore_case=args.ignore_case,
        fuzzy=args.fuzzy,
        syntax_aware=args.syntax_aware,
        syntax_mode=args.syntax_mode,
        include=args.include,
        exclude=args.exclude,
        max_results=args.max_results,
        export_path=args.export_path if hasattr(args, "export_path") and args.export_path else None,
    )
    if not args.export_path:
        print("\n--- Export Output ---\n")
        print(output)
        print("\n--- End Export ---\n")
    else:
        print(f"Exported results to {args.export_path}")

def summarize_command(args):
    """Summarize code using HuggingFace Transformers."""
    from greaper.integraton import hf_summarize_code
    import os

    # Prompt for file path if not provided
    code_path = args.code_path if hasattr(args, "code_path") and args.code_path else ""
    while not code_path or not os.path.isfile(code_path):
        code_path = input("Enter path to code file to summarize:\n> ").strip()
        if not code_path:
            print("No file provided. Exiting.")
            return
        if not os.path.isfile(code_path):
            print("File not found. Try again.")
            code_path = ""
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
    print("\n[Summarizing code...]\n")
    try:
        summary = hf_summarize_code(code)
        print(f"Summary:\n{summary}")
    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}")

def print_available_options():
    print("\n[Greaper CLI Options]")
    print("search   - Search for a pattern in files (supports archives, syntax-aware, fuzzy, etc.)")
    print("replace  - Replace a pattern in files (preview, fuzzy, future: archive-aware)")
    print("export   - Export search results for editors/tools (VS Code, Sublime, JetBrains, Vim, Emacs, JSON, CSV, Markdown)")
    print("summarize - Summarize code using HuggingFace Transformers")
    print("\n[Search Options]")
    print("  pattern         Pattern to search for (regex or fuzzy)")
    print("  path            Path to search (default: current directory, supports archives: .zip, .tar, .7z, .rar, etc.)")
    print("  -f, --fuzzy     Use fuzzy search")
    print("  -i, --ignore-case   Case-insensitive search")
    print("  -w, --word      Match whole words only")
    print("  -C, --context   Show N lines of context")
    print("  --syntax-aware  Only match in comments/strings/code (syntax aware)")
    print("  --syntax-mode   Syntax mode: all/comment/string/code/mixed")
    print("  --include       Glob patterns to include (e.g. *.py *.md)")
    print("  --exclude       Glob patterns to exclude (e.g. *.log *.tmp)")
    print("  --max-results   Maximum number of results")
    print("  --no-color      Disable color output")
    print("  --tui           Launch the Textual TUI interface")
    print("\n[Export Options]")
    print("  format          Export format: vscode, sublime, jetbrains, vim, emacs, json, csv, md/markdown")
    print("  export_path     Export file path (optional, prints to stdout if omitted)")
    print("\n[Archive Support]")
    print("  Greaper will search inside .zip, .tar, .gz, .bz2, .xz, .lzma, .7z, .rar, .whl, .egg, .jar, .nupkg, and nested archives automatically!")
    print("\nType the command you want to use (e.g., 'search') or press Enter to exit.")

def interactive_prompt(options):
    """Prompt user for each option, using defaults, and handle 'back' and 'exit'."""
    args = {}
    idx = 0
    while idx < len(options):
        name, default, help_text, opt_type = options[idx]
        # Special prompt for glob patterns
        if name in ("include", "exclude"):
            prompt = (
                f"{name} [{ ' '.join(default) if default else '' }] "
                "(space-separated glob patterns, e.g. *.py *.md)\n"
                "Type 'back' to go to the previous option, or 'exit' to quit."
            )
        else:
            prompt = (
                f"{name} [{default}]"
                f"{' (' + help_text + ')' if help_text and name not in ('include', 'exclude') else ''}\n"
                "Type 'back' to go to the previous option, or 'exit' to quit."
            )
        prompt += "\n> "
        val = input(prompt).strip()
        if val.lower() == "exit":
            print("Exiting Greaper.")
            exit(0)
        if val.lower() == "back":
            if idx > 0:
                idx -= 1
                continue
            else:
                print("Already at the first option.")
                continue
        if not val:
            val = default
        if opt_type == bool:
            val = str(val).lower() in ("1", "y", "yes", "on", "true")
        elif opt_type == int:
            try:
                val = int(val)
            except ValueError:
                val = default
        elif opt_type == list:
            val = val.split() if val else default
        args[name] = val
        idx += 1
    return args

def importfix_command(args=None):
    """Run the import fixer utility from utils."""
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils import imports
    imports.main()

def utilities_command(args=None):
    from greaper.utils import list_utilities, run_utility, get_utility_doc

    print("\nAvailable Utilities:")
    for util in list_utilities():
        print(f"  {util} - {get_utility_doc(util).strip().splitlines()[0] if get_utility_doc(util) else ''}")
    util = input("Enter utility name to run (or blank to cancel): ").strip()
    if util in list_utilities():
        print(f"\nRunning utility: {util}\n{'-'*40}")
        run_utility(util)
    else:
        print("Cancelled or not found.")

def main():
    print_available_options()
    user_cmd = input("> ").strip()
    if not user_cmd:
        print("Exiting Greaper.")
        return

    import argparse
    if user_cmd == "search":
        options = [
            ("pattern", "", "Pattern to search for (regex or fuzzy)", str),
            ("path", ".", "Path to search", str),
            ("fuzzy", False, "Use fuzzy search (y/n)", bool),
            ("ignore_case", False, "Case-insensitive search (y/n)", bool),
            ("word", False, "Match whole words only (y/n)", bool),
            ("context", 0, "Show N lines of context", int),
            ("syntax_aware", False, "Only match in comments/strings (y/n)", bool),
            ("include", ["*"], "Glob patterns to include (e.g. *.py *.md, space-separated)", list),
            ("exclude", [], "Glob patterns to exclude (e.g. *.log *.tmp, space-separated)", list),
            ("max_results", 1000, "Maximum number of results", int),
            ("no_color", False, "Disable color output (y/n)", bool),
            ("tui", False, "Launch the Textual TUI interface (y/n)", bool),
        ]
        args_dict = interactive_prompt(options)
        args = argparse.Namespace(**args_dict)
        search_command(args)
    elif user_cmd == "replace":
        options = [
            ("pattern", "", "Pattern to search for", str),
            ("replacement", "", "Replacement text", str),
            ("path", ".", "Path to search", str),
            ("fuzzy", False, "Use fuzzy search (y/n)", bool),
            ("ignore_case", False, "Case-insensitive search (y/n)", bool),
            ("preview", False, "Preview changes before applying (y/n)", bool),
        ]
        args_dict = interactive_prompt(options)
        args = argparse.Namespace(**args_dict)
        replace_command(args)
    elif user_cmd == "export":
        options = [
            ("pattern", "", "Pattern to search for", str),
            ("path", ".", "Path to search", str),
            ("format", "json", "Export format (vscode/sublime/jetbrains/vim/emacs/json/csv/md)", str),
            ("ignore_case", False, "Case-insensitive search (y/n)", bool),
            ("fuzzy", False, "Use fuzzy search (y/n)", bool),
            ("syntax_aware", False, "Syntax-aware search (y/n)", bool),
            ("syntax_mode", "all", "Syntax mode (all/comment/string/code/mixed)", str),
            ("include", ["*"], "Glob patterns to include", list),
            ("exclude", [], "Glob patterns to exclude", list),
            ("max_results", 1000, "Maximum number of results", int),
            ("export_path", "", "Export file path (optional)", str),
        ]
        args_dict = interactive_prompt(options)
        args = argparse.Namespace(**args_dict)
        export_command(args)
    elif user_cmd == "importfix":
        importfix_command()
    elif user_cmd == "utilities":
        utilities_command()
    elif user_cmd == "summarize":
        options = [
            ("code_path", "", "Path to code file to summarize", str),
        ]
        args_dict = interactive_prompt(options)
        args = argparse.Namespace(**args_dict)
        summarize_command(args)
    else:
        print("Unknown command. Exiting.")

if __name__ == "__main__":
    main()