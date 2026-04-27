# /// script
# requires-python = ">=3.11"
# ///

import logging
from pathlib import Path

from lib.logging import setup_initial_logging
from lib.unlink import rmdir, rmfile

logger = logging.getLogger(__name__)


def main():
    setup_initial_logging()

    project_dir = Path(__file__).parent.parent
    test_reports_dir = project_dir / "tests" / "reports"
    html_report_dir = test_reports_dir / "coverage-html"
    coverage_db_file = project_dir / ".coverage"

    rmdir(html_report_dir, "code coverage report directory")
    rmfile(coverage_db_file, "coverage execution data file")


if __name__ == "__main__":
    main()
