"""tui_typer_tutor."""

__version__ = '1.0.1'
__pkg_name__ = 'tui_typer_tutor'

# ====== Above is the recommended code from calcipy_template and may be updated on new releases ======

import logging

from corallium.log import configure_logger, get_logger, logger

APP_NAME = 'tui-typer-tutor'
configure_logger(log_level=logging.DEBUG)
