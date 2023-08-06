"""Display Character to Textual Key Map."""

from string import ascii_letters, digits

from bidict import bidict

_special_keys = {
    "'": 'apostrophe',
    ' ': 'space',
    '!': 'exclamation_mark',
    '"': 'quotation_mark',
    '#': 'number_sign',
    '$': 'dollar_sign',
    '%': 'percent_sign',
    '&': 'ampersand',
    '(': 'left_parenthesis',
    ')': 'right_parenthesis',
    '*': 'asterisk',
    '+': 'plus',
    ',': 'comma',
    '-': 'minus',
    '.': 'full_stop',
    '/': 'slash',
    ':': 'colon',
    ';': 'semicolon',
    '<': 'less_than_sign',
    '=': 'equals_sign',
    '>': 'greater_than_sign',
    '?': 'question_mark',
    '@': 'at',
    '[': 'left_square_bracket',
    '\\': 'backslash',
    ']': 'right_square_bracket',
    '^': 'circumflex_accent',
    '_': 'underscore',
    '`': 'grave_accent',
    '{': 'left_curly_bracket',
    '|': 'vertical_line',
    '}': 'right_curly_bracket',
    '~': 'tilde',
    '⏎': 'enter',
    '␛': 'escape',
}

DISPLAY_TO_TEXTUAL = bidict({
    **_special_keys,
    **dict(zip(ascii_letters, ascii_letters, strict=True)),
    **dict(zip(digits, digits, strict=True)),
})
"""Bi-directional mapping of Display Characters to Textual Bindings."""
