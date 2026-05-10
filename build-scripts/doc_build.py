# /// script
# requires-python = ">=3.11"
# ///

import logging
import sys
from pathlib import Path

from lib import command_line
from lib.logging import setup_initial_logging

logger = logging.getLogger(__name__)


def main():
    setup_initial_logging()

    project_dir = Path(__file__).parent.parent

    logger.info("Ensuring the version file corresponds to the current commit, and tags.")
    command_result = command_line.run(["hatch", "version"], encoding="utf-8", cwd=project_dir)
    logger.info("Version file created.  Command stdout: %r, stderr: %r.", command_result.stdout, command_result.stderr)

    logger.info("Building documentation.")
    command_result = command_line.run(
        ["sphinx-build", "-M", "html", "doc/source", "doc/build"], encoding="utf-8", cwd=project_dir
    )
    sys.stdout.write(command_result.stdout)
    sys.stderr.write(command_result.stderr)


if __name__ == "__main__":
    main()
