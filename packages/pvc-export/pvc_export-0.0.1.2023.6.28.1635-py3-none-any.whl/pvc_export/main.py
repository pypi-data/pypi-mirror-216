"""
Provide the main app entry point.
"""

__all__ = ['main', 'set_logger']

import logging
import sys
from pathlib import Path
from pprint import pformat

from .cli import ap
from .config import create_config, load_config, set_export_path
from .data import export_csv, export_peaks, is_data_ready, load_data_files
from .plot import export_fig, make_fig

log = logging.getLogger()


def set_logger(q=False, v=False, logfile=None):
    """ Prepare logger.
    :param q: be quiet
    :param v: be verbose
    :param logfile: file path to send messages to. If None, use STDOUT.
    """
    level = logging.DEBUG if v else logging.CRITICAL+1 if q else logging.INFO
    fmt = '{levelname:6} {filename}:{lineno} {funcName}()\n{message}\n'
    logging.basicConfig(filename=logfile, filemode='w', format=fmt, style='{', level=level, force=True)
    # mpl dumps too many messages when a simple root logger
    # is used like here (via BasicConfig) and the level == DEBUG, hide them.
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    logging.getLogger('PIL').setLevel(logging.ERROR)


def main():
    """ The app entry point.
    Process cli arguments, populate shared vars in the intended order and follow the default workflow.
    """
    args = ap.parse_args()
    set_logger(q=args.q, v=args.v, logfile=args.l)
    log.debug(f'args: {pformat(args)}')
    log.debug(f"Started in dir: '{Path().cwd()}'")

    load_config(file=args.c)
    load_data_files(files=args.files)
    set_export_path(file=args.e)

    if args.cc:
        create_config(file=args.cc)
        return

    if not is_data_ready():
        if log.level <= logging.CRITICAL:
            ap.print_help()
            return 'Warning: No data loaded'
        return 1

    make_fig()
    export_fig()
    export_csv()
    export_peaks()


if __name__ == '__main__':
    sys.exit(main())
