
"""bioticDETR package main.

Launch point for command line use.
The root logger is configured with stream (info) and file (debug) handlers.

Usage:
    python -m bioticDETR

See package README for introduction.

"""


import logging

from absTools.execute import package_main_exec
from absTools.logs import LoggerCfg

import bioticDETR


logger = logging.getLogger(__name__)
"""Module logger."""


# Configure root logging
log_cfg = LoggerCfg('bioticDETRApp')


def main():
    logger.warning("Command line use is not implemented, "
                   "import bioticDETR package and use as a library")

    # raise SystemExit(1)


if __name__ == "__main__":
    package_main_exec(main)
