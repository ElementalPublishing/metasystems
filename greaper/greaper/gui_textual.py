from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, DataTable, Select, Checkbox
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events
from textual.screen import ModalScreen

from greaper.utils import list_utilities, run_utility, get_utility_doc
from greaper.themes import THEMES
from greaper.integraton import hf_summarize_code
import os

class GreaperHeader(Static):
    def __init__(self, theme_name, **kwargs):
        super().__init__("", **kwargs)
        self.theme_name = theme_name

    def update_header(self, theme_name):
        self.theme_name = theme_name
        self.update(f"🐶 Greaper — {self.theme_name} Mode")

    def on_mount(self):
        self.update_header(self.theme_name)

class GreaperFooter(Static):
    def compose(self):
        yield Static("", id="footer_text")  # Empty footer or add your own message

class UtilitiesModal(ModalScreen):
    def __init__(self, utils_list):
        super().__init__()
        self.utils_list = utils_list

    def compose(self):
        yield Static("Select a utility to run:", id="utils_label")
        for util in self.utils_list:
            doc = get_utility_doc(util)
            label = f"{util} - {doc.strip().splitlines()[0] if doc else ''}"
            yield Button(label, id=f"util_{util}")
        yield Button("Cancel", id="util_cancel")

    async def on_button_pressed(self, event):
        if event.button.id == "util_cancel":
            await self.app.pop_screen()
            return
        util_name = event.button.id.replace("util_", "")
        await self.app.pop_screen()
        self.app.run_utility_from_tui(util_name)

class GreaperApp(App):
    CSS_PATH = "greaper_theme.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+t", "swap_theme", "Swap Theme"),
    ]
    search_results = reactive([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_names = list(THEMES.keys())
        self.theme_index = 0
        self.theme_name = self.theme_names[self.theme_index]
        self._current_theme = THEMES[self.theme_name]

    @classmethod
    def from_cli_args(cls, args):
        return cls(
            pattern=getattr(args, "pattern", None),
            path=getattr(args, "path", "."),
            fuzzy=getattr(args, "fuzzy", False),
            ignore_case=getattr(args, "ignore_case", False),
            word=getattr(args, "word", False),
            context=getattr(args, "context", 0),
            syntax_aware=getattr(args, "syntax_aware", False),
            include=getattr(args, "include", ["*"]),
            exclude=getattr(args, "exclude", []),
            max_results=getattr(args, "max_results", 1000),
        )

    def compose(self) -> ComposeResult:
        yield GreaperHeader(self.theme_name, id="header")
        with Container(id="main-container"):
            with Horizontal(id="search-bar"):
                yield Input(placeholder="Enter search pattern...", id="search_input")
                yield Button("Search", id="search_btn", classes="primary")
                yield Button("Utilities", id="utilities_btn")
                yield Button("Summarize Code", id="summarize_btn")
                yield Select(
                    [(theme, theme) for theme in THEMES.keys()],
                    prompt="Theme",
                    id="theme_select",
                    value=self.theme_name
                )
                yield Checkbox("Case Insensitive", id="case_checkbox")
                yield Checkbox("Regex", id="regex_checkbox")
                yield Checkbox("Fuzzy", id="fuzzy_checkbox")
                yield Checkbox("Syntax Aware", id="syntax_checkbox")
                yield Checkbox("Whole Word", id="wholeword_checkbox")
                yield Input(placeholder="Context lines (e.g. 2)", id="context_input")
                yield Input(placeholder="Include globs (e.g. *.py *.md)", id="include_input")
                yield Input(placeholder="Exclude globs (e.g. *.log *.tmp)", id="exclude_input")
                yield Input(placeholder="Max results (e.g. 1000)", id="maxresults_input")
                yield Select(
                    [("All", "all"), ("Comment", "comment"), ("String", "string"), ("Code", "code"), ("Mixed", "mixed")],
                    prompt="Syntax Mode",
                    id="syntaxmode_select",
                    value="all"
                )
            # Load and display the banner
            banner_path = os.path.join(os.path.dirname(__file__), "..", "banner.txt")
            if os.path.exists(banner_path):
                with open(banner_path, "r", encoding="utf-8") as f:
                    banner = f.read()
                yield AnimatedBanner(banner, id="banner_art")
            yield Static("Results:", id="results_label")
            yield DataTable(id="results_table")
        yield GreaperFooter(id="footer")

    async def on_mount(self):
        self.apply_theme()
        self.query_one("#theme_select", Select).value = self.theme_name
        table = self.query_one("#results_table", DataTable)
        table.add_columns("File", "Line", "Match", "Context Before", "Context After")
        table.zebra_stripes = True
        self.query_one("#search_input", Input).focus()
        try:
            from greaper.algorithms import fuzzy
            backend = getattr(fuzzy.levenshtein, "__module__", "")
            if "cython_ext" in backend:
                self.notify("[INFO] Using Cython-accelerated fuzzy backend.", timeout=8)
            else:
                self.notify("[INFO] Using pure Python fuzzy backend.", timeout=8)
        except Exception as e:
            self.push_screen(ErrorModal(f"[ERROR] Could not determine fuzzy backend: {e}"))
        self.notify("Change mode: Ctrl+T", timeout=4)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search_btn":
            await self.perform_search()
        elif event.button.id == "utilities_btn":
            utils_list = list_utilities()
            await self.push_screen(UtilitiesModal(utils_list))
        elif event.button.id == "summarize_btn":
            table = self.query_one("#results_table", DataTable)
            # 1. If a row is selected, summarize that code snippet
            if table.row_count and table.cursor_row is not None:
                selected_row = table.get_row(table.cursor_row)
                code_snippet = selected_row[2] if len(selected_row) > 2 else ""
                if code_snippet.strip():
                    self.notify("Summarizing selected code...", timeout=2)
                    try:
                        summary = hf_summarize_code(code_snippet)
                        await self.push_screen(ErrorModal(f"Summary:\n{summary}"))
                    except Exception as e:
                        await self.push_screen(ErrorModal(f"Summarization error: {e}"))
                    return
            # 2. If no selection, prompt for file path and summarize file
            code_path = await self.prompt("No search result selected. Enter path to code file to summarize (or leave blank to batch summarize all results):")
            if code_path and os.path.isfile(code_path):
                try:
                    with open(code_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    self.notify("Summarizing file...", timeout=2)
                    summary = hf_summarize_code(code)
                    await self.push_screen(ErrorModal(f"Summary for {os.path.basename(code_path)}:\n{summary}"))
                except Exception as e:
                    await self.push_screen(ErrorModal(f"Summarization error: {e}"))
                return
            # 3. If no file path, batch summarize all results in the table
            if table.row_count:
                self.notify("Batch summarizing all search results...", timeout=2)
                summaries = []
                for idx in range(table.row_count):
                    row = table.get_row(idx)
                    code_snippet = row[2] if len(row) > 2 else ""
                    if code_snippet.strip():
                        try:
                            summary = hf_summarize_code(code_snippet)
                        except Exception as e:
                            summary = f"[Error: {e}]"
                        summaries.append(f"File: {row[0]}, Line: {row[1]}\nSummary: {summary}\n")
                if summaries:
                    await self.push_screen(ErrorModal("Batch Summaries:\n\n" + "\n".join(summaries)))
                else:
                    self.notify("No code snippets to summarize in results.", timeout=2)
            else:
                self.notify("No search results or file provided to summarize.", timeout=2)

    def run_utility_from_tui(self, util_name):
        try:
            output = run_utility(util_name)
            self.notify(f"Utility '{util_name}' ran successfully.", timeout=3)
            if output:
                self.push_screen(ErrorModal(str(output)))
        except Exception as e:
            self.push_screen(ErrorModal(f"Utility error: {e}"))

    async def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip().lower()
        if value == "exit":
            await self.action_quit()
            return
        if value == "back":
            table = self.query_one("#results_table", DataTable)
            table.clear()
            self.query_one("#search_input", Input).focus()
            return
        await self.perform_search()

    async def on_select_changed(self, event: Select.Changed):
        if event.select.id == "theme_select":
            self.theme_name = event.value
            self.theme_index = self.theme_names.index(self.theme_name)
            self._current_theme = THEMES[self.theme_name]
            self.apply_theme()
            self.notify(f"Theme switched to {self.theme_name}", timeout=2)

    async def action_swap_theme(self):
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        self.theme_name = self.theme_names[self.theme_index]
        self._current_theme = THEMES[self.theme_name]
        self.apply_theme()
        self.query_one("#theme_select", Select).value = self.theme_name
        self.notify(f"Theme switched to {self.theme_name}", timeout=2)

    def apply_theme(self):
        theme = self._current_theme
        header = self.query_one("#header", GreaperHeader)
        header.update_header(self.theme_name)
        footer = self.query_one("#footer", GreaperFooter)
        footer.styles.background = theme.get("--footer-bg", "#16161e")
        footer.styles.color = theme.get("--footer-fg", "#ff0080")
        main = self.query_one("#main-container", Container)
        main.styles.background = theme.get("--background", "#1a1b26")
        try:
            banner = self.query_one("#banner_art", Static)
            banner.styles.color = theme.get("--banner-art", "#bb9af7")
        except Exception:
            pass
        try:
            results_label = self.query_one("#results_label", Static)
            results_label.styles.color = theme.get("--results-label", "#e0af68")
        except Exception:
            pass
        try:
            table = self.query_one("#results_table", DataTable)
            table.styles.background = theme.get("--background", "#1a1b26")
            table.styles.color = theme.get("--foreground", "#c0caf5")
        except Exception:
            pass
        # Add more widgets here as needed

    async def perform_search(self):
        from greaper.core import search_files

        pattern = self.query_one("#search_input", Input).value
        if not pattern:
            await self.push_screen(ErrorModal("Please enter a search pattern."))
            return

        case = self.query_one("#case_checkbox", Checkbox).value
        regex = self.query_one("#regex_checkbox", Checkbox).value
        fuzzy = self.query_one("#fuzzy_checkbox", Checkbox).value
        syntax_aware = self.query_one("#syntax_checkbox", Checkbox).value
        whole_word = self.query_one("#wholeword_checkbox", Checkbox).value

        path = self.path if hasattr(self, "path") and self.path else "."

        try:
            context = int(self.query_one("#context_input", Input).value)
        except ValueError:
            context = 0
        include = self.query_one("#include_input", Input).value.split() or ["*"]
        exclude = self.query_one("#exclude_input", Input).value.split() or []
        try:
            max_results = int(self.query_one("#maxresults_input", Input).value)
        except ValueError:
            max_results = 1000

        syntax_mode = self.query_one("#syntaxmode_select", Select).value

        try:
            results = search_files(
                pattern=pattern,
                path=path,
                fuzzy=fuzzy,
                ignore_case=case,
                word=whole_word,
                context=context,
                include=include,
                exclude=exclude,
                max_results=max_results,
                syntax_aware=syntax_aware,
                syntax_mode=syntax_mode,
                regex=regex,
            )
        except Exception as e:
            await self.push_screen(ErrorModal(f"Search error: {e}"))
            return

        self.search_results = results
        table = self.query_one("#results_table", DataTable)
        table.clear()
        alt = False
        for file, line, match, before, after in results:
            before_text = "\n".join(before) if before else ""
            after_text = "\n".join(after) if after else ""
            table.add_row(
                str(file),
                str(line),
                match,
                before_text,
                after_text
            )
            alt = not alt

    async def action_quit(self) -> None:
        await self.shutdown()

    async def on_key(self, event: events.Key):
        if event.key in ("ctrl+c", "q"):
            await self.action_quit()

class ErrorModal(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        yield Static(self.message, id="error_message")
        yield Button("Close", id="close_error")

    async def on_button_pressed(self, event):
        if event.button.id == "close_error":
            await self.app.pop_screen()

class AnimatedBanner(Static):
    banner_text = reactive("")

    def __init__(self, full_text, **kwargs):
        super().__init__("", **kwargs)
        self.full_text = full_text

    async def on_mount(self):
        for i in range(1, len(self.full_text) + 1):
            self.banner_text = self.full_text[:i]
            self.update(self.banner_text)
            await self.sleep(0.01)  # Adjust speed here

        self.notify("Change mode: Ctrl+t", timeout=18)

if __name__ == "__main__":
    GreaperApp().run()