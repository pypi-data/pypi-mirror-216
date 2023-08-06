"""Typing Logic."""


from beartype import beartype
from pydantic import BaseModel, Field

from ..constants import DISPLAY_TO_TEXTUAL

BACKSPACE = 'backspace'
UNKNOWN = '�'


class AtEndOfExpectedError(Exception):
    """Reached end of the expected keys."""

    ...


class ExpectedKey(BaseModel):
    """Expected Key."""

    textual: str
    """Textual Key Name."""

    @property
    def text(self) -> str:
        """Displayed text."""
        return DISPLAY_TO_TEXTUAL.inverse.get(self.textual) or UNKNOWN


class TypedKey(ExpectedKey):
    """Typed Key."""

    expected: ExpectedKey | None
    """Store the expected key when typed and expected become out-of-sync."""

    @property
    def was_correct(self) -> bool:
        """If typed key matches expected."""
        return self.expected is not None and self.text == self.expected.text


class Keys(BaseModel):
    """Key Model."""

    expected: list[ExpectedKey] = Field(default_factory=list)
    """The expected keys for practice."""

    typed_all: list[TypedKey] = Field(default_factory=list)
    """Append-only list of typed keys."""

    typed: list[TypedKey] = Field(default_factory=list)
    """Only tracks non-deleted typed keys."""

    last_was_delete: bool = False
    """Indicate if last operation was a delete."""

    @beartype
    def store(self, *, key: TypedKey, is_delete: bool) -> None:
        """Store a new typed key."""
        self.typed_all.append(key)
        self.last_was_delete = is_delete
        if not is_delete:
            self.typed.append(key)
        elif self.typed:
            self.typed = self.typed[:-1]


@beartype
def on_keypress(textual: str, keys: Keys) -> None:
    """Process a key press."""
    is_delete = textual == BACKSPACE
    if not is_delete and len(keys.typed) == len(keys.expected):
        raise AtEndOfExpectedError
    expected = None if is_delete else keys.expected[len(keys.typed)]
    key = TypedKey(textual=textual, expected=expected)
    keys.store(key=key, is_delete=is_delete)
