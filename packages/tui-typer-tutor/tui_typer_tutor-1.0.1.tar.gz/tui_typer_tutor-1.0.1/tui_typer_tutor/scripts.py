"""Start the command line program."""

import argparse
import sys
from pathlib import Path

from beartype import beartype

from . import __version__
from .app.ttt import TuiTyperTutor
from .core.config import get_config
from .core.uninstall import uninstall


@beartype
def parse_ttt_args(argv: list[str]) -> argparse.Namespace:
    """Parse custom CLI arguments for ttt."""
    parser = argparse.ArgumentParser(description='Practice Touch Typing')
    parser.add_argument('--seed-file', help='Optional path to seed file used for generating the prompt.')
    parser.add_argument(
        '-v', '--version', action='version',
        version=f'%(prog)s {__version__}', help="Show program's version number and exit.",
    )
    parser.add_argument(
        '--uninstall', action='store_true', help='Remove all files created by tui-typer-tutor.',
    )
    return parser.parse_args(argv)


@beartype
def start() -> None:  # pragma: no cover
    """CLI Entrypoint."""
    args = parse_ttt_args(sys.argv[1:])
    if args.uninstall:
        uninstall()
    else:
        config = get_config()
        if args.seed_file:
            config.seed_file = Path(args.seed_file)
        TuiTyperTutor().run()
