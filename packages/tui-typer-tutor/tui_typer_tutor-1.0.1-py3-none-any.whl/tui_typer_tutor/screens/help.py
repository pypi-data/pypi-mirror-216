"""The help screen."""

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Markdown

from ..core.uninstall import get_cache_dir

_HELP_TEXT = f"""
# Help

Type the displayed characters until complete. The session statistics are stored in `{get_cache_dir()}`

Tip: many terminals support adjusting font size with `<C->` and `<C+>`; reset zoom with `<C0>`

Press `ESC` to close.
"""


# PLANNED: Improve the Help Screen style
class Help(ModalScreen[None]):
    """Screen with the help dialog."""

    DEFAULT_CSS: ClassVar[str] = """
    Help {
        align: center middle;
    }

    #text {
        content-align: center middle;
        height: 50%;
        width: 50%;
    }
    """

    BINDINGS: ClassVar[list[Binding]] = [  # type: ignore[assignment]
        Binding('escape', 'close', 'Close'),
    ]

    def compose(self) -> ComposeResult:
        """Layout."""
        yield Markdown(_HELP_TEXT.strip(), id='text')

    def action_close(self) -> None:
        """Close the dialog."""
        self.dismiss()
