from textual.app import App, ComposeResult
from textual.widgets import Header


class RorqualApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
