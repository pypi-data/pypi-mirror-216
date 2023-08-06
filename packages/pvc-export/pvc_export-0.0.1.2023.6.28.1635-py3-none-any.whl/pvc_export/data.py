"""
Provide `data` dict as a container for shared data and data presentation attributes.
plot.py is intended to import `data` and use it to create matplotlib.Figure

export_csv():
    export raw and smoothed spectra into a tab-separated table as a .csv file

export_peaks():
    export maxima in smoothed spectra into a tab-separated table as a .peaks.csv file

is_data_ready():
    test if `data` is not empty

load_data_files():
    load PVC files specified on command line and/or in user config,
    extract XY spectral points from them, populate the `data` dict with the XY data.
"""

__all__ = ['data', 'export_csv', 'export_peaks', 'is_data_ready', 'load_data_files']

import logging
from os.path import commonpath, expandvars, join
from pathlib import Path
from pprint import pformat
from sys import float_info

import numpy as np
from scipy.signal import find_peaks, savgol_filter
from yaml import Dumper, Loader, dump, load

from .config import cfg, cfg1

log = logging.getLogger()

# The main container for XY data and data presentation attributes.
data = {}


def is_data_ready() -> bool:
    """ Use it in main.main() to check if any data were loaded """
    log.debug(f'len(data)={len(data)}')
    return bool(data)


def get_files() -> list:
    """ List already loaded files.
    Used to avoid loading of the same file twice and to calculate the common path."""
    return [data[i]['file'] for i in data.keys()]


def get_cfg_data_files_count() -> int:
    """ Count only on integer-like keys in `cfg` (i.e. skip 'fig', etc) """
    count = 0
    for k in cfg.keys():
        if isinstance(k, int):
            count += 1
    return count


def get_smooth(i):
    """ Populate `data[i]['smooth']` from `data[i]['raw']`
    :param i: top level key in `data` that is currently populated """
    global data
    x, y = data[i]['raw']['xy']
    data[i]['smooth']['xy'] = x, savgol_filter(y, window_length=9, polyorder=3)


def get_peaks(i, thres=0.01):
    """ Find the positions of local Y maxima.
    Save the corresponding XY values in data[i]['peaks'].
    :param i: top level key in `data` that is currently populated.
    :param thres: a fraction of overall Y-amplitude, 0.01 works for implen data
    """
    global data
    x, y = data[i]['smooth']['xy']
    prom = thres * (max(y) - min(y))
    idxs, _ = find_peaks(y, prominence=prom)  # width=10, distance=10
    data[i]['peaks']['xy'] = x[idxs], y[idxs]


def get_xy(i, line):
    """ Create an X, Y tuple at data[i]['raw']['xy'] applying
    Y-shift and Y-normalization as well as X and Y range limits.
    :param i: top key in `data` that is currently populated.
    :param line: a linear array of the interleaving x and y values.
    """
    global data
    # xy = np.array(tuple(map(float, line)))
    xy = np.array(line, dtype=np.float32)
    xy = xy.reshape((int(xy.size / 2), 2))
    log.debug(f"xy[{i}].shape: {xy.shape} in '{data[i]['file']}'")

    if isinstance(data[i]['yshift'], str) and data[i]['yshift'].casefold() == 'min'.casefold():
        xy[:, 1] = xy[:, 1] - xy[:, 1].min()

    if isinstance(data[i]['yshift'], (int, float)):
        xy[:, 1] = xy[:, 1] + data[i]['yshift']

    if data[i]['norm']:
        xy[:, 1] = xy[:, 1] / xy[:, 1].max()

    xmin, xmax, ymin, ymax = None, None, None, None
    if data[i]['xrange']:
        xmin, xmax = data[i]['xrange']
    if data[i]['yrange']:
        ymin, ymax = data[i]['yrange']
    if not xmin:
        xmin = 0.0
    if not xmax:
        xmax = float_info.max
    if not ymin:
        ymin = float_info.min
    if not ymax:
        ymax = float_info.max
    xy = xy[xmin < xy[:, 0]]
    xy = xy[xy[:, 0] < xmax]
    xy = xy[ymin < xy[:, 1]]
    xy = xy[xy[:, 1] < ymax]
    data[i]['raw']['xy'] = xy[:, 0], xy[:, 1]


def load_file(i):
    """ XY spec scan data in `data[i]['file']` are on the line started with '$PXY '.
    Find the line, pass it to get_xy() for the further processing.
    :param i: top level key in `data` that is currently populated.
    """
    try:
        # the file existence was tested in load_data_files()
        with open(data[i]['file']) as fin:
            for line in fin:
                if line[:5] == '$PXY ':
                    get_xy(i=i, line=line.split()[4:])
                    return
    except (Exception,) as expt:
        log.error(expt)


def expand_files(files: list) -> list:
    """ Support globs expansion.
    Globs expansion creates lists, use them to extend/update the initial files list.
    Also, as it's implemented (in py 3.10) only with relative paths, do not expand absolute path.
    Globs withing an absolute path will be treated literally,
    and ignored later, if the corresponding files do not exist.
    """
    if not files:
        return []
    out = []
    for f in files:
        log.debug(f"Collecting file '{f}'")
        ef = expandvars(f)
        if Path(ef).is_absolute():
            out += [ef]
            continue
        try:
            for p in Path().glob(ef):
                out += [str(p)]
        except (Exception,) as expt:
            log.exception(expt)
            log.error(f"Could not expand '{ef}'")
            out += [ef]
    log.debug(f'Collected files:\n{pformat(out, indent=2)}')
    return sorted(out)


def load_data_files(files: list):
    """ Get file names  from the parameter `files` and 'file' fields from `cfg`,
    expand env variables in the names, expand globs in relative names.
    Check if the named files exist and of the appropriate type, try to load data from them.
    Create entries in `data`, with one top-level integer-like key per one successfully loaded file.
    Populate each of them (i.e. each `data[i]`) with the loaded data and the corresponding `cfg[i]` props.

    If `files` is empty, use 'file' fields from `cfg`,
    if those are empty, do not add new entries to `data`.

    For each i, `files[i]` overrides `cfg[i]['file']`, i.e.
    if cli_name.pvc comes from command line parameters and loaded user config file already has entries
        1: file: cfg_name1.pvc,...
        2: file: cfg_name2.pvc,...
    then 'cli_name.pvc' will be loaded as data[1] and 'cfg_name2.pvc' as data[2].

    `cfg` is to be prepared in advance with config.load_config(), f.i. in main.main()

    :param files: is expected to take `args.files` presenting list of data file paths provided via CLI
    """
    global data

    files_ = expand_files(files)

    data_len = max(len(files_), get_cfg_data_files_count())

    # Start with 1 to support natural numbering in `cfg`
    for i in range(1, data_len + 1):
        file = cfg[i]['file'] if i in cfg.keys() else ''

        # Override the cfg[i]['file'] value
        # with the corresponding one from command line if that is present
        if i - 1 < len(files_):
            file = files_[i - 1]
        if not file:
            continue

        path = Path(expandvars(file)).resolve()
        if (not path.is_file() or
                not path.exists() or
                (path.suffix.casefold() != '.pvc'.casefold()) or
                file in get_files()):
            continue

        # Prepare data[i] and cfg[i] trees (to accept data loaded from file)
        if i in cfg.keys():
            data[i] = load(dump(cfg[i], Dumper=Dumper, sort_keys=False), Loader=Loader)
        else:
            data[i] = cfg1()

        data[i]['file'] = file

        if not data[i]['label']:
            data[i]['label'] = f'{i}'

        if not data[i]['title']:
            data[i]['title'] = join(path.parent.name, path.stem) if data[i]['parent+'] else f'{path.stem}'

        cfg[i] = load(dump(data[i], Dumper=Dumper, sort_keys=False, width=2147483647), Loader=Loader)

        load_file(i)
        if 'xy' not in data[i]['raw'].keys():
            del data[i]
            continue

        get_smooth(i)

        get_peaks(i)

        # end reading xy data from input files

    # Update curves colors
    if len(data) > 0:
        set_colors()
        set_export_path_from_data()

    log.debug(f'Loaded data:\n{pformat(data, indent=2, depth=3)}')
    # End load_data_files()


def set_colors():
    """ From cfg['colors'] extract a subset with the size of len(data)
    Assign colors from the subset to the loaded curves.
    """
    step = max(1.0, (len(cfg['colors']) - 1) / max(1, len(data) - 1))
    idxs_colors = [int(i * step) for i in range(len(data))]

    colors = np.array(cfg['colors']).take(idxs_colors, mode='wrap')
    log.debug(f'selected color ids={idxs_colors}')
    log.debug(f'colors={pformat(colors, indent=2)}')

    for i in sorted(data.keys()):
        for prop in ('peaks', 'raw', 'smooth'):
            if not data[i][prop]['color']:
                data[i][prop]['color'] = f'{colors[i - 1]}'
            if not cfg[i][prop]['color']:
                cfg[i][prop]['color'] = f'{colors[i - 1]}'


def get_common_path() -> Path:
    try:
        out = commonpath(get_files())
    except ValueError:
        out = ''
    return Path(out)


def set_export_path_from_data():
    """ If the export path is not yet set (by the user config file entry),
    fill it in from the 1st loaded data file path.
    Call to `config.set_export_path()` in `main.main()` will later amend the path.
    """
    if not cfg['export']['path']:
        path = ''
        if len(data) == 1 and 1 in data.keys():
            path = Path(data[1]['file']).with_suffix('.~')
        elif len(data) > 1 and 1 in data.keys() and get_common_path() == Path(data[1]['file']).parent:
            path = Path(data[1]['file']).parent  # default name will be added in cfg.set_export_path()
        if path:
            log.debug(f"Setting export path from data[1]:'{path}'")
            cfg['export']['path'] = f'{path}'


def export_csv():
    """ Export `data[i]['raw']['xy']` and `data[i]['smooth']['xy']`
    as TAB-separated columns x_raw, y_raw, x_smooth, y_smooth
    into a file specified in cfg['export']['path'] with the appended suffix '.csv'
    """
    if not data:
        return

    csvf = Path(cfg['export']['path']).with_suffix('.csv')

    # PREPARE 2-ROW HEADER: 1st - 'labels', 2nd - measurement units
    header = ''
    for i in sorted(data.keys()):
        label = data[i]['label']
        header += f'{label}\t\t\t\t'
    header += '\n' + 'nm\tAU\tsmooth,nm\tsmooth,AU\t' * len(data.keys()) + '\n'

    # PREPARE xy-data COLUMNS
    out = ''
    # get numbers of rows in data[i] (i.e. xy-points in each spectrum i)
    lengths = dict(
        [(i, len(data[i]['raw']['xy'][0])) for i in sorted(data.keys())]
    )
    if not lengths:
        return
    for j in range(max(lengths.values())):
        for i in sorted(data.keys()):
            if j >= lengths[i]:
                out += '\t' * 4
                continue
            out += f"{data[i]['raw']['xy'][0][j]}\t"
            out += f"{data[i]['raw']['xy'][1][j]:.5f}\t"
            out += f"{data[i]['smooth']['xy'][0][j]}\t"
            out += f"{data[i]['smooth']['xy'][1][j]:.5f}\t"
        out += '\n'  # for every j, not i

    log.info(f'Saving {csvf}')
    with open(csvf, 'w') as fout:
        fout.write(header)
        fout.write(out)


def export_peaks():
    """ Export `data[i]['peaks']['xy']` as tab-separated columns x, y
    into a file specified in cfg['export']['path'] with the appended suffix '.peaks.csv'
    """
    if not data:
        return

    ptf = Path(cfg['export']['path']).with_suffix('.csv')
    ptf = ptf.with_stem(f'{ptf.stem}.peaks')

    # PREPARE 2-ROW HEADER: 1st - 'labels', 2nd - measurement units
    header = ''
    for i in sorted(data.keys()):
        label = data[i]['label']
        header += f'{label}\t\t'
    header += '\n' + f'nm\tAU\t' * len(data.keys()) + '\n'

    out = ''
    lengths = dict(
        [(i, len(data[i]['peaks']['xy'][0])) for i in sorted(data.keys())]
    )
    if not lengths:
        return
    for j in range(max(lengths.values())):
        for i in sorted(data.keys()):
            if j >= lengths[i]:
                out += '\t' * 2
                continue
            out += f"{data[i]['peaks']['xy'][0][j]}\t"
            out += f"{data[i]['peaks']['xy'][1][j]:.5f}\t"
        out += '\n'  # for every j, not i

    log.info(f'Saving {ptf}')
    with open(ptf, 'w') as fout:
        fout.write(header)
        fout.write(out)


if __name__ == '__main__':
    pass
