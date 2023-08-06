"""The main screen."""

import math
import sys
from contextlib import suppress
from os import get_terminal_size
from typing import ClassVar

from beartype import beartype
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.css.query import NoMatches
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Footer, Header, Label

from ..core.config import get_config
from ..core.metrics import SessionMetrics, append_csv
from ..core.seed_data import load_seed_data
from ..core.typing import UNKNOWN, AtEndOfExpectedError, Keys, on_keypress

MAX_CHARS = math.floor(0.80 * get_terminal_size()[0])
"""Determine maximum characters that can fit in 80% of the terminal width."""

CHAR_OFFSET = math.floor(0.40 * MAX_CHARS)
"""Offset to keep the next characters visible."""


class Main(Screen[None]):
    """The main screen for the application."""

    DEFAULT_CSS: ClassVar[str] = """
    Screen {
        background: #1b2b34;
    }

    #left-pad {
        width: 10%;
    }
    #content {
        width: 80%;
        align: center middle;
    }

    .tutor-container {
        content-align-horizontal: left;
        height: 2;
    }
    #text-container {
        color: #7e8993;
    }
    #typed-container .error {
        color: #ec5f67;
    }
    #typed-container .success {
        color: #99c794;
    }
    #typed-unknown {
        color: #b69855;
    }
    """

    BINDINGS: ClassVar[list[Binding]] = [  # type: ignore[assignment]
        Binding('ctrl+q', 'save_and_quit', 'Save and Quit'),
    ]

    keys: Keys
    metrics: SessionMetrics

    def action_save_and_quit(self) -> None:
        """Save and quit."""
        append_csv(self.metrics.end_session(self.keys))
        # TODO: Print out or display a success message on completion!
        sys.exit(0)

    def compose(self) -> ComposeResult:
        """Layout."""
        yield Header()
        with Horizontal():
            yield Vertical(id='left-pad')
            # FYI: ^^ couldn't get 'center' alignment to work
            with Vertical(id='content'):
                yield Horizontal(id='text-container', classes='tutor-container')
                yield Horizontal(id='typed-container', classes='tutor-container')
                yield Label(id='typed-unknown', classes='warning')
        yield Footer()

    def on_mount(self) -> None:
        """On widget mount."""
        # TODO: Support more customization
        seed_file = get_config().seed_file
        self.keys = Keys(expected=load_seed_data(seed_text=seed_file.read_text()))
        self.metrics = SessionMetrics.from_filename(filename=seed_file.name)
        cont = self.query_one('#text-container', Horizontal)
        for key in self.keys.expected:  # FYI: Mounts all expected keys and crops
            cont.mount(Label(key.text, classes='text'))

    @beartype
    def on_key(self, event: Key) -> None:  # noqa: CAC001
        """Capture all key presses and show in the typed input."""
        try:
            on_keypress(event.key, self.keys)
        except AtEndOfExpectedError:
            self.action_save_and_quit()

        width = len(self.keys.typed)
        if self.keys.last_was_delete:
            with suppress(NoMatches):
                self.query('Label.typed').last().remove()
        elif width:
            cursor_width = MAX_CHARS - CHAR_OFFSET
            if width >= cursor_width:
                self.query('Label.typed').first().remove()
                self.query('Label.text').first().remove()
            # Choose the class
            color_class = 'success'
            display_text = self.keys.typed[-1].text
            if not self.keys.typed[-1].was_correct:
                color_class = 'error'
                # Ensure that invisible characters are displayed
                display_text = display_text.strip() or '█'
            typed_label = Label(display_text, classes=f'typed {color_class}')
            self.query_one('#typed-container', Horizontal).mount(typed_label)
            textual_unknown = event.key if display_text == UNKNOWN else ''
            self.query_one('#typed-unknown', Label).update(textual_unknown)
