# /// script
# requires-python = ">=3.11"
# ///

import logging
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Final

from lib.logging import setup_initial_logging

HATCH_PATH: Final[str] = "hatch"

logger = logging.getLogger(__name__)


def main():
    setup_initial_logging()

    project_dir = Path(__file__).parent.parent
    test_reports_dir = project_dir / "tests" / "reports"
    code_coverage_badge_path = test_reports_dir / "codecov-badge.svg"

    code_coverage_percentage_command = subprocess.run(
        [HATCH_PATH, "run", "test-coverage:coverage", "report", "--format=total"],
        cwd=project_dir,
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    exit_code = code_coverage_percentage_command.returncode
    if exit_code != 0:
        e = subprocess.CalledProcessError(
            returncode=exit_code,
            cmd=code_coverage_percentage_command.args,
            output=code_coverage_percentage_command.stdout,
            stderr=code_coverage_percentage_command.stderr,
        )
        e.add_note(f"stdout: {code_coverage_percentage_command.stdout}")
        e.add_note(f"stderr: {code_coverage_percentage_command.stderr}")
        raise e
    code_coverage_percentage = code_coverage_percentage_command.stdout.strip()
    percentage = f"{code_coverage_percentage}%"

    url = f"https://badgen.net/badge/codecov/{urllib.parse.quote(percentage)}/green?icon=codecov"

    logger.info("Downloading code coverage badge %r to %r.", url, code_coverage_badge_path)

    urllib.request.urlretrieve(url=url, filename=code_coverage_badge_path)  # noqa: S310


if __name__ == "__main__":
    main()
