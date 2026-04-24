# /// script
# requires-python = ">=3.11"
# ///

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def rmdir(directory_path: Path) -> None:
    if not directory_path.exists():
        logger.info("Documentation build directory (%r) not found.  Skipping.", directory_path)
    else:
        logger.info("Deleting %r.", directory_path)
        shutil.rmtree(directory_path)


def main():
    logging.basicConfig(
        datefmt="%Y-%m-%dT%H:%M:%S",
        format="%(asctime)s %(levelname)s <%(filename)s:%(lineno)d>: %(message)s",
        level=logging.INFO,
    )

    project_dir = Path(__file__).parent.parent
    doc_dir = project_dir / "doc"
    doc_output_dir = doc_dir / "build"
    api_generated_sources_dir = doc_dir / "source" / "api" / "generated"

    for directory_path in [doc_output_dir, api_generated_sources_dir]:
        rmdir(directory_path)


if __name__ == "__main__":
    main()
