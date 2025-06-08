import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Greaper: Grep on Steroids - Fast, modern search for code and data."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for a pattern in files.")
    search_parser.add_argument("pattern", help="Pattern to search for (regex or fuzzy)")
    search_parser.add_argument("path", nargs="?", default=".", help="Path to search (default: current directory)")
    search_parser.add_argument("-f", "--fuzzy", action="store_true", help="Use fuzzy search")
    search_parser.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    search_parser.add_argument("-w", "--word", action="store_true", help="Match whole words only")
    search_parser.add_argument("-C", "--context", type=int, default=0, help="Show N lines of context")
    search_parser.add_argument("--tui", action="store_true", help="Launch the Textual TUI interface")

    args = parser.parse_args()

    if args.command == "search":
        if args.tui:
            from .gui_textual import GreaperApp
            # Pass CLI args to TUI if you want (example below)
            GreaperApp.from_cli_args(args).run()
        else:
            print(f"[CLI] Searching for '{args.pattern}' in '{args.path}' (fuzzy={args.fuzzy}, ignore_case={args.ignore_case}, word={args.word}, context={args.context})")
            # Here you would call your core search logic
            print("[CLI] (Search logic not yet implemented)")

if __name__ == "__main__":
    main()