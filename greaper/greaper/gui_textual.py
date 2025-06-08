from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, DataTable, Select, Checkbox
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events

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
        yield Header(show_clock=True)
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
            yield Static("Results:", id="results_label")
            yield DataTable(id="results_table")
        yield Footer()

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
            self.notify(f"[ERROR] Could not determine fuzzy backend: {e}", timeout=3)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search_btn":
            await self.perform_search()

    async def on_input_submitted(self, event: Input.Submitted):
        await self.perform_search()

    async def on_select_changed(self, event: Select.Changed):
        self.theme_name = event.value
        self._current_theme = THEMES[self.theme_name]
        self.update_theme()
        self.query_one(Header).styles.background = self._current_theme["background"]
        self.query_one(Header).styles.color = self._current_theme["primary"]
        self.query_one(Footer).styles.background = self._current_theme["background"]
        self.query_one(Footer).styles.color = self._current_theme["primary"]
        self.query_one("#results_label", Static).styles.color = self._current_theme["accent"]

    async def perform_search(self):
        from greaper.core import search_files

        pattern = self.query_one("#search_input", Input).value
        if not pattern:
            self.notify("Please enter a search pattern.", timeout=2)
            return

        case = self.query_one("#case_checkbox", Checkbox).value
        regex = self.query_one("#regex_checkbox", Checkbox).value
        fuzzy = self.query_one("#fuzzy_checkbox", Checkbox).value
        syntax_aware = self.query_one("#syntax_checkbox", Checkbox).value

        path = self.path if self.path else "."

        try:
            results = search_files(
                pattern=pattern,
                path=path,
                fuzzy=fuzzy,
                ignore_case=case,
                word=regex,
                context=self.context,
                include=self.include,
                exclude=self.exclude,
                max_results=self.max_results,
                syntax_aware=syntax_aware,
            )
        except Exception as e:
            self.notify(f"Search error: {e}", timeout=4)
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

if __name__ == "__main__":
    GreaperApp().run()