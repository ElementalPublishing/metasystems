from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, DataTable, Select, Checkbox
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events

THEMES = {
    "Default": {
        "primary": "blue",
        "accent": "magenta",
        "background": "black",
        "highlight": "yellow",
    },
    "Solarized": {
        "primary": "#268bd2",
        "accent": "#b58900",
        "background": "#002b36",
        "highlight": "#859900",
    },
    "Monokai": {
        "primary": "#f92672",
        "accent": "#a6e22e",
        "background": "#272822",
        "highlight": "#fd971f",
    },
}

class GreaperApp(App):
    CSS_PATH = "greaper_theme.css"  # This line makes greaper_theme.css the default theme

    BINDINGS = [("q", "quit", "Quit"), ("ctrl+c", "quit", "Quit")]  # Add easy exit bindings

    search_results = reactive([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_name = "Default"
        self.theme = THEMES[self.theme_name]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            with Horizontal():
                yield Input(placeholder="Enter search pattern...", id="search_input")
                yield Button("Search", id="search_btn", variant="primary")
                yield Select(list(THEMES.keys()), prompt="Theme", id="theme_select")
                yield Checkbox("Case Insensitive", id="case_checkbox")
                yield Checkbox("Regex", id="regex_checkbox")
                yield Checkbox("Fuzzy", id="fuzzy_checkbox")
            yield Static("Results:", id="results_label")
            yield DataTable(id="results_table")
        yield Footer()

    async def on_mount(self):
        self.update_theme()
        self.query_one("#results_table", DataTable).add_columns("File", "Line", "Match")

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search_btn":
            await self.perform_search()

    async def on_input_submitted(self, event: Input.Submitted):
        await self.perform_search()

    async def on_select_changed(self, event: Select.Changed):
        self.theme_name = event.value
        self.theme = THEMES[self.theme_name]
        self.update_theme()

    async def perform_search(self):
        # Placeholder: Replace with actual search logic
        pattern = self.query_one("#search_input", Input).value
        case = self.query_one("#case_checkbox", Checkbox).value
        regex = self.query_one("#regex_checkbox", Checkbox).value
        fuzzy = self.query_one("#fuzzy_checkbox", Checkbox).value

        # Dummy results for demonstration
        results = [
            ("file1.txt", 10, f"Found '{pattern}' here"),
            ("file2.py", 42, f"Another '{pattern}' match"),
        ]
        self.search_results = results
        table = self.query_one("#results_table", DataTable)
        table.clear()
        for row in results:
            table.add_row(*map(str, row))

    def update_theme(self):
        theme = self.theme
        self.styles.background = theme["background"]
        self.styles.primary = theme["primary"]
        self.styles.accent = theme["accent"]
        # You can expand this to set widget-specific styles

    async def action_quit(self) -> None:
        await self.shutdown()

    async def on_key(self, event: events.Key):
        if event.key in ("ctrl+c", "q"):
            await self.action_quit()

if __name__ == "__main__":
    GreaperApp().run()