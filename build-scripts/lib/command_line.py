# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

"""Wraps Python a standard library functions like `subprocess.run` with a
limited API in order to provide more informative failure messages (such as
including standard output, and error)

This assumes that executed commands produce a reasonably small amout of
standard output, and standard error output.
"""

import subprocess
from os import PathLike
from typing import overload

type StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]  # stable


@overload
def run(
    command: list[str], *, check: bool = True, encoding: str, cwd: StrOrBytesPath | None = None
) -> subprocess.CompletedProcess[str]: ...


@overload
def run(
    command: list[str], *, check: bool = True, encoding: None, cwd: StrOrBytesPath | None = None
) -> subprocess.CompletedProcess[bytes]: ...


def run(command: list[str], *, check: bool = True, encoding: str | None = None, cwd: StrOrBytesPath | None = None):
    """Executes a given command line, capturing standard output, and standard
    error content

    Assumes that this content is reasonably small (e.g., fits in memory).

    Also, a user would have no indication of progress while the command is
    running.  So, in an interactive application, the command should complete
    reasonably quickly.
    """

    execution_result = subprocess.run(command, capture_output=True, check=False, encoding=encoding, cwd=cwd)

    if check:
        exit_code = execution_result.returncode
        if exit_code != 0:
            e = subprocess.CalledProcessError(
                returncode=exit_code, cmd=command, output=execution_result.stdout, stderr=execution_result.stderr
            )
            e.add_note(f"stdout: {execution_result.stdout!r}")
            e.add_note(f"stderr: {execution_result.stderr!r}")
            raise e

    return execution_result
