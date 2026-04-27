# SPDX-FileCopyrightText: 2026-present Pavel M. Penev <pavpen@gmail.com>
#
# SPDX-License-Identifier: MIT

import logging

def setup_initial_logging():
    logging.basicConfig(
        datefmt="%Y-%m-%dT%H:%M:%S",
        format="%(asctime)s %(levelname)s <%(filename)s:%(lineno)d>: %(message)s",
        level=logging.INFO,
    )
