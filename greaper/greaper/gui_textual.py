from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, DataTable, Select, Checkbox
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events
from textual.screen import ModalScreen

THEMES = {
    "John Wick": {
        "primary": "#00bfff",      # neon blue
        "accent": "#ff0080",       # neon magenta
        "background": "#181a20",   # deep dark
        "highlight": "#ffd700",    # gold
        "table_header": "#00bfff",
        "table_row": "#e0e0e0",
        "table_alt_row": "#23272e",
        "table_match": "#ffd700",
    },
    "Default": {
        "primary": "blue",
        "accent": "magenta",
        "background": "black",
        "highlight": "yellow",
        "table_header": "blue",
        "table_row": "white",
        "table_alt_row": "grey23",
        "table_match": "yellow",
    },
    "Solarized": {
        "primary": "#268bd2",
        "accent": "#b58900",
        "background": "#002b36",
        "highlight": "#859900",
        "table_header": "#268bd2",
        "table_row": "#eee8d5",
        "table_alt_row": "#073642",
        "table_match": "#b58900",
    },
    "Monokai": {
        "primary": "#f92672",
        "accent": "#a6e22e",
        "background": "#272822",
        "highlight": "#fd971f",
        "table_header": "#f92672",
        "table_row": "#f8f8f2",
        "table_alt_row": "#49483e",
        "table_match": "#fd971f",
    },
}

class GreaperHeader(Static):
    DEFAULT_CSS = """
    GreaperHeader {
        height: 3;
        background: #16161e;
        color: #00bfff;
        text-style: bold;
        content-align: center middle;
        border-bottom: solid #ff0080;
    }
    """
    def compose(self):
        yield Static("🐶 Greaper — John Wick Mode", id="header_title")

class GreaperFooter(Static):
    DEFAULT_CSS = """
    GreaperFooter {
        height: 2;
        background: #16161e;
        color: #ff0080;
        content-align: center middle;
        border-top: solid #00bfff;
    }
    """
    def compose(self):
        yield Static("Type 'exit' to quit | Theme: John Wick", id="footer_text")

class GreaperApp(App):
    CSS_PATH = "greaper_theme.css"
    BINDINGS = [("q", "quit", "Quit"), ("ctrl+c", "quit", "Quit")]
    search_results = reactive([])

    def __init__(
        self,
        pattern=None,
        path=".",
        fuzzy=False,
        ignore_case=False,
        word=False,
        context=0,
        syntax_aware=False,
        include=None,
        exclude=None,
        max_results=1000,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.path = path
        self.fuzzy = fuzzy
        self.ignore_case = ignore_case
        self.word = word
        self.context = context
        self.syntax_aware = syntax_aware
        self.include = include if include is not None else ["*"]
        self.exclude = exclude if exclude is not None else []
        self.max_results = max_results
        self.theme_name = "John Wick"
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
        yield GreaperHeader()
        with Container():
            with Horizontal():
                yield Input(placeholder="Enter search pattern...", id="search_input")
                yield Button("Search", id="search_btn", variant="primary")
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
            yield Static("Results:", id="results_label")
            yield DataTable(id="results_table")
        yield GreaperFooter()

    async def on_mount(self):
        self.update_theme()
        self.query_one("#theme_select", Select).value = self.theme_name
        table = self.query_one("#results_table", DataTable)
        table.add_columns("File", "Line", "Match", "Context Before", "Context After")
        table.zebra_stripes = True

        # Show which fuzzy backend is being used
        try:
            from greaper.algorithms import fuzzy
            backend = getattr(fuzzy.levenshtein, "__module__", "")
            if "cython_ext" in backend:
                self.notify("[INFO] Using Cython-accelerated fuzzy backend.", timeout=3)
            else:
                self.notify("[INFO] Using pure Python fuzzy backend.", timeout=3)
        except Exception as e:
            await self.push_screen(ErrorModal(f"[ERROR] Could not determine fuzzy backend: {e}"))

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search_btn":
            await self.perform_search()

    async def on_input_submitted(self, event: Input.Submitted):
        await self.perform_search()

    async def on_select_changed(self, event: Select.Changed):
        if event.select.id == "theme_select":
            self.theme_name = event.value
            self._current_theme = THEMES[self.theme_name]
            self.update_theme()
            self.query_one(GreaperHeader).styles.background = self._current_theme["background"]
            self.query_one(GreaperHeader).styles.color = self._current_theme["primary"]
            self.query_one(GreaperFooter).styles.background = self._current_theme["background"]
            self.query_one(GreaperFooter).styles.color = self._current_theme["accent"]
            self.query_one("#results_label", Static).styles.color = self._current_theme["accent"]

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

        path = self.path if self.path else "."

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
                regex=regex,  # Only if your backend supports it!
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
            row_style = self._current_theme["table_alt_row"] if alt else self._current_theme["table_row"]
            table.add_row(
                str(file),
                str(line),
                f"[{self._current_theme['table_match']}]{match}[/{self._current_theme['table_match']}]",
                before_text,
                after_text
            )
            alt = not alt

    def update_theme(self):
        theme = self._current_theme
        self.styles.background = theme["background"]
        # Add more widget style updates here if needed

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

if __name__ == "__main__":
    GreaperApp().run()