"""Main application."""

from typing import ClassVar

from textual.app import App
from textual.binding import Binding

from ..screens.help import Help
from ..screens.main import Main


class TuiTyperTutor(App[None]):
    """Main Application."""

    TITLE = 'TUI Typer Tutor'

    BINDINGS: ClassVar[list[Binding]] = [  # type: ignore[assignment]
        Binding('ctrl+backslash', 'show_help', 'Help'),
    ]

    def on_mount(self) -> None:
        """Set up the application after the DOM is ready."""
        self.push_screen(Main())

    def action_show_help(self) -> None:
        """Action to display the help dialog."""
        self.push_screen(Help())
