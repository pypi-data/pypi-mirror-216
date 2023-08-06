"""
"""

__all__ = ['ap']

from argparse import ArgumentParser, RawDescriptionHelpFormatter

PROG = "pvc-export"

DESCRIPTION = None  # inconveniently appears between the 'Usage:...' line and the parameter descriptions section.

EPILOG = f"""

Examples:

    {PROG} *.pvc
        => from all found *.pvc files produce:
        export.png       - figure
        export.csv       - plot data
        export.peaks.csv - peaks data

    {PROG} *.pvc -e <name>
        => from all found *.pvc files produce:
        <name>.png       - figure
        <name>.csv       - plot data
        <name>.peaks.csv - peaks data

    {PROG} --cc "config"
        => create "config.yaml" template,
        do not export figure or data

    {PROG} *.pvc --cc "config"
        => create "config.yaml" listing inside all found *.pvc files with the default styles assigned,
        do not export figure or data

    {PROG} -c "config.yaml"
        => use "config.yaml" to save
        figure, plot data, and peaks data with the styles and locations defined inside "config.yaml"

    {PROG} *.pvc -c "config.yaml"
        => use "config.yaml" for styles and locations to save all found .pvc files
        <name>.png       - figure,
        <name>.csv       - plot data,
        <name>.peaks.csv - peaks data,
        where <name> is set in advance in CONFIG:export:path

In *.pvc file names, variables, like "$HOME", and globs, like "*", are expanded and "~" is not.
Globs are only expanded if a file path is not absolute.
"""

ap = ArgumentParser(
    prog=PROG, description=DESCRIPTION, epilog=EPILOG,
    formatter_class=RawDescriptionHelpFormatter
    )

ap.add_argument(
    'files', metavar='FILE', nargs='*',
    help='*.pvc files to load and export'
)

ap.add_argument(
    '-c', metavar='CONFIG', default='',
    help='load a custom config from the specified file CONFIG'
)

ap.add_argument(
    '--cc', metavar='NEW_CONFIG', default='',
    help='create and save a new custom config file NEW_CONFIG'
)

ap.add_argument(
    '-e', metavar='EXPORT_FILE_NAME', default='',
    help='base name for export files'
)

ap.add_argument('-l', metavar='LOG_FILE_NAME', default='', help='log file name')

ag = ap.add_mutually_exclusive_group()

ag.add_argument('-v', action='store_true', default=False, help='be verbose')

ag.add_argument('-q', action='store_true', default=False, help='be quiet')

if __name__ == '__main__':
    pass
