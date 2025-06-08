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
    pattern = args.pattern
    if not pattern:
        print("\nWhat would you like to search for?")
        pattern = input("Enter search pattern (e.g. 'def ', 'TODO', 'main'): ").strip()
        if not pattern:
            print("No pattern entered. Exiting.")
            return

    # Step 2: Path
    path = args.path
    if not path:
        print("\nWhere do you want to search?")
        path = input("Enter path to search (default: .): ").strip() or "."

    # Step 3: Options (with ability to edit)
    print("\nSearch options:")
    options = [
        ("Fuzzy search", args.fuzzy, "ON/OFF", bool),
        ("Ignore case", args.ignore_case, "ON/OFF", bool),
        ("Whole word", args.word, "ON/OFF", bool),
        ("Context lines", args.context, "2", int),
        ("Syntax aware", args.syntax_aware, "ON/OFF", bool),
        ("Include globs", " ".join(args.include), "*.py *.md", str),
        ("Exclude globs", " ".join(args.exclude), "*.log *.tmp", str),
        ("Max results", args.max_results, "1000", int),
        ("Color output", not args.no_color, "ON/OFF", bool),
    ]
    for idx, (name, val, example, _) in enumerate(options, 1):
        print(f"  {idx}. {name}: {val} (e.g. {example})")

    print("\nWould you like to change any options? (y/N)")
    if input().strip().lower() == "y":
        for idx, (name, val, example, opt_type) in enumerate(options, 1):
            if name in ["Include globs", "Exclude globs"]:
                new_val = prompt_option(name, val, example)
                if name == "Include globs":
                    args.include = new_val.split()
                else:
                    args.exclude = new_val.split()
            elif name == "Context lines":
                args.context = prompt_option(name, val, example, int)
            elif name == "Max results":
                args.max_results = prompt_option(name, val, example, int)
            elif name == "Color output":
                args.no_color = not prompt_option(name, val, example, bool)
            else:
                setattr(args, name.lower().replace(" ", "_"), prompt_option(name, val, example, bool))

    # Step 4: Confirm
    print("\nReady to search with these settings?")
    print(f"  Pattern:      {pattern}")
    print(f"  Path:         {path}")
    print(f"  Fuzzy:        {'ON' if args.fuzzy else 'OFF'}")
    print(f"  Ignore case:  {'ON' if args.ignore_case else 'OFF'}")
    print(f"  Whole word:   {'ON' if args.word else 'OFF'}")
    print(f"  Context:      {args.context}")
    print(f"  Syntax aware: {'ON' if args.syntax_aware else 'OFF'}")
    print(f"  Include:      {' '.join(args.include)}")
    print(f"  Exclude:      {' '.join(args.exclude)}")
    print(f"  Max results:  {args.max_results}")
    print(f"  Color:        {'OFF' if args.no_color else 'ON'}")
    print("\nProceed? (Y/n)")
    if input().strip().lower() == "n":
        print("Search cancelled.")
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
        )
        print_results(results, color=not args.no_color, context=args.context)
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")

def replace_command(args):
    """Handle the 'replace' command (future)."""
    print(f"[CLI] Replace '{args.pattern}' with '{args.replacement}' in '{args.path}'")
    print(f"  Fuzzy: {args.fuzzy} | Ignore case: {args.ignore_case} | Preview: {args.preview}")
    # TODO: Implement replace logic

def export_command(args):
    """Handle the 'export' command (future)."""
    print(f"[CLI] Exporting results to {args.format} format")
    # TODO: Implement export logic

def main():
    parser = argparse.ArgumentParser(
        description="Greaper: Grep on Steroids — Fast, modern search for code and data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for a pattern in files.")
    search_parser.add_argument("pattern", nargs="?", help="Pattern to search for (regex or fuzzy)")
    search_parser.add_argument("path", nargs="?", default=".", help="Path to search (default: current directory)")
    search_parser.add_argument("-f", "--fuzzy", action="store_true", help="Use fuzzy search")
    search_parser.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    search_parser.add_argument("-w", "--word", action="store_true", help="Match whole words only")
    search_parser.add_argument("-C", "--context", type=int, default=0, help="Show N lines of context")
    search_parser.add_argument("--syntax-aware", action="store_true", help="Only match in comments/strings (syntax aware)")
    search_parser.add_argument("--include", nargs="*", default=["*"], help="Glob patterns to include (e.g. *.py *.md)")
    search_parser.add_argument("--exclude", nargs="*", default=[], help="Glob patterns to exclude (e.g. *.log *.tmp)")
    search_parser.add_argument("--max-results", type=int, default=1000, help="Maximum number of results")
    search_parser.add_argument("--no-color", action="store_true", help="Disable color output")
    search_parser.add_argument("--tui", action="store_true", help="Launch the Textual TUI interface")
    search_parser.set_defaults(func=search_command)

    # Replace command (future)
    replace_parser = subparsers.add_parser("replace", help="Replace a pattern in files.")
    replace_parser.add_argument("pattern", help="Pattern to search for")
    replace_parser.add_argument("replacement", help="Replacement text")
    replace_parser.add_argument("path", nargs="?", default=".", help="Path to search (default: current directory)")
    replace_parser.add_argument("-f", "--fuzzy", action="store_true", help="Use fuzzy search")
    replace_parser.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    replace_parser.add_argument("--preview", action="store_true", help="Preview changes before applying")
    replace_parser.set_defaults(func=replace_command)

    # Export command (future)
    export_parser = subparsers.add_parser("export", help="Export search results.")
    export_parser.add_argument("format", choices=["json", "csv", "md"], help="Export format")
    export_parser.set_defaults(func=export_command)

    args = parser.parse_args()

    if getattr(args, "tui", False) and args.command == "search":
        from .gui_textual import GreaperApp
        GreaperApp.from_cli_args(args).run()
    else:
        args.func(args)

if __name__ == "__main__":
    main()