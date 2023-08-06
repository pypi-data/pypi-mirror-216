"""Load Seed Data."""

import random

from beartype import beartype

from ..constants import DISPLAY_TO_TEXTUAL
from .typing import ExpectedKey


@beartype
def load_seed_data(seed_text: str) -> list[ExpectedKey]:
    """Load Seed Data in Vim format."""
    grouped_keys = [
        [ExpectedKey(textual=DISPLAY_TO_TEXTUAL[token]) for token in line.rstrip()]
        for line in seed_text.split('\n')
        if line.strip()
    ]
    random.shuffle(grouped_keys)  # noqa: DUO102
    return [_k for _keys in grouped_keys for _k in _keys]
