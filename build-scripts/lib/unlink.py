# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def str_with_first_capitalized(value: str) -> str:
    if len(value) < 1:
        return value

    return f"{value[0].upper()}{value[1:]}"


def rmfile(path: Path, description: str) -> None:
    if not path.exists():
        logger.info("%s (%r) not found.  Skipping.", str_with_first_capitalized(description), path)
    else:
        logger.info("Deleting %s %r.", description, path)
        path.unlink()


def rmdir(path: Path, description: str) -> None:
    if not path.exists():
        logger.info("%s (%r) not found.  Skipping.", str_with_first_capitalized(description), path)
    else:
        logger.info("Deleting %s %r.", description, path)
        shutil.rmtree(path)
