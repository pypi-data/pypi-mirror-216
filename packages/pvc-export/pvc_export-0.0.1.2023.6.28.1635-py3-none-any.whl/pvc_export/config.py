"""
Provide `cfg` dict as a shared setting registry.
Other modules can import it, read and update its fields.

The default `cfg` dict is imported from `cfg.py`.

load_config():
    Update the default `cfg` dict with custom values from user config.
    The user config file path is obtained from CLI in main.main().

create_config():
    Save current `cfg` state in a YAML file.
    The file can be modified later and used as user config.
    The file path is obtained from CLI in main.main().

set_export_path():
    Set cfg['export']['path'] that will be a basis to construct
    export file names in data.export_*() and plot.export_*().

cfg1():
    return a 'deep copy' of `cfg[1]`.
    It is used to construct missing config entries.
"""

__all__ = ['cfg', 'cfg1', 'load_config', 'create_config', 'set_export_path']

import logging
from copy import deepcopy
from os.path import expandvars
from pathlib import Path
from pprint import pformat

from yaml import Dumper, Loader, dump, load

from .cfg import HEADER, cfg

log = logging.getLogger()

# The default color set to pick plot colors from
COLORS = [
    # https://gka.github.io/palettes/#/17|s|0000dd,00dddd,008800,dddd00,dd0000|ffffe0,ff005e,93003a|0|0
    '#0000dd', '#0037dd', '#006fdd', '#00a6dd', '#00dddd',
    '#00c8a6', '#00b36f', '#009d37', '#008800', '#379d00',
    '#6fb300', '#a6c800', '#dddd00', '#dda600', '#dd6f00',
    '#dd3700', '#dd0000'
]

# The default export file name base
# Later, it is appended with .peaks.csv, .csv, .png or other suffixes
EXPORT_FNAME = 'export'

# User config file path: updated, if user config file was loaded.
# It is used to set cfg:export:path if that was not set otherwise,
# see set_export_path()
_user_config = ''

# _cfg1 is used as input in cfg1(),
# it holds the default plot settings from cfg[1] in a serialized form.
# Note: fields 'label', 'title', 'color', if not empty,
# will not be auto-updated on data file loading.
# Therefore, it is better to not update `_cfg1` after the loading of a user config.
_cfg1 = dump(cfg[1], Dumper=Dumper, sort_keys=False, width=2147483647)


def cfg1() -> dict:
    """ Deserialize and return _cfg1, representing the default plot settings from cfg[1].
    It is used to populate cfg[1+n] in load_config() and data[i] in data.load_data_files()
    as a replacement for copy.deepcopy().
    """
    return load(_cfg1, Loader=Loader)


def update_dict(trg: dict, src: dict):
    """ Copy recursively only known keys:values from `src` into `trg`.
    Ignore values of irrelevant types.
    """
    if not isinstance(trg, dict) or not isinstance(src, dict):
        return

    for k in src.keys():
        if k not in trg.keys():
            continue

        if isinstance(src[k], dict) and isinstance(trg[k], dict):
            update_dict(trg[k], src[k])

        elif isinstance(src[k], list) and isinstance(trg[k], list):
            trg[k] = deepcopy(src[k])  # list(src[k]).copy()

        elif (isinstance(src[k], (bool, float, int, str)) and
              isinstance(trg[k], (bool, float, int, str))):
            trg[k] = src[k]

        elif src[k] is None:
            trg[k] = ''


def load_config(file=None):
    """ Load user config from `file` and update `cfg` accordingly.

    Load `file` into a new dict `src`. The `file` does not have to represent a complete config.
    If `file` describes more than 1 plot, with cfg1() create new cfg[x] keys in `cfg` using cfg[1] as template,
    then update them from `src`. Thereby fields, missing in `file`, will be created with the default values.

    :param file: user config file path.
    """
    # _load_default_config()
    src = {}
    path = Path(expandvars(file)) if file else ''
    if path and path.exists() and path.is_file():
        log.debug(f'Loading config file {path.resolve()}')
        try:
            with open(path, 'r') as fin:
                src = load(fin, Loader)
        except (Exception,) as expt:
            log.error(expt)
        else:
            global _user_config
            log.debug(f'_user_config={path}')
            _user_config = f'{path}'
    if not src:
        log.debug(f"Could not load '{path}': the default config will be used")

    for k in src.keys():
        if k in cfg:
            if isinstance(cfg[k], dict) and isinstance(src[k], dict):
                update_dict(trg=cfg[k], src=src[k])
            else:
                cfg[k] = deepcopy(src[k])
        else:
            # create only integer-like top-level keys,
            # i.e. those holding settings for each of *.pvc files, one key per one file.
            try:
                i = int(k)
            except ValueError:
                continue
            if i > 1:
                cfg[i] = cfg1()
                update_dict(trg=cfg[i], src=src[k])

    if 'colors' in cfg.keys() and not cfg['colors']:
        cfg['colors'] = COLORS

    log.debug(f'Loaded config :\n{pformat(cfg, indent=2, depth=3, sort_dicts=False)}')


def save_config(file=None):
    """ Save current `cfg` state into the `file`.
    :param file: path to the file to create.
    """
    if not file:
        log.error(f"No file path to save current config was not provided")
        return
    path = Path(expandvars(file))
    if path.is_dir():
        log.error(f"Provided file path points to a directory: not overwriting")
        return
    path = path.with_suffix('.yaml')
    log.info(f"Saving config file: '{path.resolve()}'")
    try:
        with open(path, "w") as fout:
            fout.write(HEADER)
            dump(cfg, fout, Dumper, sort_keys=False, width=2147483647)
    except (Exception,) as expt:
        log.error(expt)
        log.error(f"Could not save config file: '{path}'")


def create_config(file=None):
    """
    Create user config in `file`.
    `main.main()` calls `set_export_path()` before this.
    `args.cc` is the default value for the `path`; normally, it is not empty if used.
    :param file: path to a user config file to create.
    """
    if file:
        ef = expandvars(file)
        try:
            eg = sorted(Path().glob(ef))
        except (OSError, Exception) as expt:
            log.error(expt)
            eg = []
        if eg:
            path = eg[0]
        else:
            path = ef
    else:
        path = cfg['export']['path']
    save_config(file=path)


def set_export_path(file=None):
    """
    Set `cfg['export']['path']` to `file`. If `file` is empty, guess.

    Priority to calculate the export path:
        1.  from command line, i.e. from the parameter `file`
            which might also be empty (`file=args.e` in `main.main()`),
        2.  from `cfg['export']['path']` that was loaded from config file
            this includes the 1st data file location
        3.  from user config file location
        4.  from `$HOME/Desktop` (or just `$HOME`) + `EXPORT_FNAME`
    Note:
        `main.main()` calls `data.load_data_files()` before this; that also amends `cfg['export']['path']`
        if that was empty and one or more data files were loaded.
    """
    if file:
        path = expandvars(file)
    elif cfg['export']['path']:
        # cfg:export:path gets data[1]['file'] on *.pvc loading if it was empty before
        path = expandvars(cfg['export']['path'])
    elif _user_config:
        path = Path(_user_config).stem
    else:
        dt = Path.home() / 'Desktop'
        path = dt if dt.exists() and dt.is_dir() else Path.home()
    path = Path(path)
    if path.is_dir():
        path = path / EXPORT_FNAME
    # appending a temporary suffix here simplifies later handling of file names with inner dots
    if not path.suffix:
        path = path.with_suffix('.~')
    elif path.suffix != '.~':
        path = path.with_suffix(f'{path.suffix}.~')
    log.debug(f"Setting export path: '{path.resolve()}'")
    cfg['export']['path'] = f'{path}'


if __name__ == '__main__':
    pass
