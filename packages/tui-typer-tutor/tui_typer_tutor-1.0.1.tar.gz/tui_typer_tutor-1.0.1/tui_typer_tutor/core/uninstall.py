"""Uninstall files managed by `ttt`."""

import shutil
from pathlib import Path

import platformdirs
from beartype import beartype
from corallium.log import logger

from .. import APP_NAME


@beartype
def get_cache_dir() -> Path:
    """Application cache directory."""
    return Path(platformdirs.user_cache_dir(APP_NAME))


@beartype
def uninstall() -> None:
    """Uninstall files managed by `ttt`."""
    cache_dir = get_cache_dir()
    if cache_dir.is_dir():
        logger.warning('Removing cache directory', cache_dir=cache_dir)
        for csv_file in cache_dir.glob('*.*'):
            logger.debug('Removing', name=csv_file.name, content=csv_file.read_text())
        shutil.rmtree(cache_dir)

    logger.warning(
        'All local files created by this tool have been removed. You can now pipx or pip uninstall this package',
    )
