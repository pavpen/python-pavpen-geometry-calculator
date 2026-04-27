# /// script
# requires-python = ">=3.11"
# ///

import logging
from pathlib import Path

from lib.logging import setup_initial_logging
from lib.unlink import rmdir

logger = logging.getLogger(__name__)


def main():
    setup_initial_logging()

    project_dir = Path(__file__).parent.parent
    doc_dir = project_dir / "doc"
    doc_output_dir = doc_dir / "build"

    rmdir(doc_output_dir, "documentation output directory")


if __name__ == "__main__":
    main()
