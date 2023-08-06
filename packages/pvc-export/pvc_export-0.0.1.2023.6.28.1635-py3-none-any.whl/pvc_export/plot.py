"""
Create and export mpl figure.

Initially, create it with an increased YFigSize to make enough room for title,
so that it would not truncate the plot area.
Then use Pillow.Image.crop() to cut white spaces out.
Figure, plots, export parameters are taken from the imported `cfg`.
"""

__all__ = ['export_fig', 'make_fig']

import logging
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from matplotlib import rcParams
from matplotlib.figure import Axes, Figure
from matplotlib.markers import MarkerStyle
from matplotlib.pyplot import subplots, switch_backend

from .config import cfg
from .data import data
from .mplrc import MPLRC

log = logging.getLogger()

fig: Figure
ax: Axes
title = []

rcParams.update(MPLRC)

grid_props = {  # major is set in mplrc
    'minor': {
        'which': 'minor',
        'linewidth': 0.1,
        'alpha': 0.35,
    },
}


def make_fig():
    global fig, ax, title
    fsz = cfg['fig']['size'] if cfg['fig']['size'] else None
    fsz = (fsz[0] / 25.4, fsz[1] / 25.4 * 2) if fsz else None
    dpi = cfg['fig']['dpi'] if cfg['fig']['dpi'] else None
    # The same dpi will be used for saving, fig.canvas.draw()
    # will be used to generate and save the image, not fig.save()

    switch_backend('agg')
    fig, ax = subplots(1, 1, figsize=fsz, dpi=dpi)
    ax.set_position([0.1, 0.1, 0.8, 0.5 if fsz else 0.8])

    ax.grid(**grid_props['minor'])

    ax.set_xlabel('nm')
    ax.set_ylabel('AU')

    add_plots()
    add_peaks()
    adjust_axes()

    # if XY limits were set explicitly, follow the settings exactly.
    if cfg['fig']['xrange']:
        ax.set_xlim(*cfg['fig']['xrange'])
    if cfg['fig']['yrange']:
        ax.set_ylim(*cfg['fig']['yrange'])

    ax.legend()
    ax.set_title(label='\n'.join(title))  # , fontdict=fontdict


def adjust_axes():
    """ Extend XY limits about 1% beyond the span of the loaded data """
    global ax
    # X
    xmin, xmax = ax.get_xlim()
    xspan = xmax - xmin
    xmin = xmin - xspan * 0.01
    xmax = xmax + xspan * 0.01
    ax.set_xlim(xmin, xmax)
    # Y
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    ymin = ymin - yspan * 0.01
    ymax = ymax + yspan * 0.125
    ax.set_ylim(ymin, ymax)


def add_plots():
    """ Add only 'raw' and 'smooth' plots here """
    global ax, title
    for i in sorted(data.keys()):
        title += [f"{data[i]['label']}: {data[i]['title']}"]
        for plot in ('raw', 'smooth'):
            if data[i][plot]['show']:
                ax.plot(
                    *data[i][plot]['xy'],
                    alpha=data[i][plot]['alpha'],
                    color=data[i][plot]['color'],
                    linestyle=data[i][plot]['linestyle'],
                    linewidth=data[i][plot]['linewidth'],
                    label=f"{data[i]['label']}:{plot}",
                )


def add_peaks():
    """ Add 'peaks' plot with annotations """
    global ax
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    # ADD PEAK MARKERS
    for i in sorted(data.keys()):
        if data[i]['peaks']['show']:
            ax.scatter(
                *data[i]['peaks']['xy'],
                alpha=data[i]['peaks']['alpha'],
                c=data[i]['peaks']['color'],
                marker=MarkerStyle(data[i]['peaks']['style'], 'none'),
                s=data[i]['peaks']['size'],
                label=f"{data[i]['label']}:peaks",
            )
            # ADD PEAK ANNOTATIONS
            for x, y in zip(*data[i]['peaks']['xy']):
                ax.annotate(
                    f'{x:.0f} nm,\n{y:.3f} AU',
                    xy=(x, y + yspan * 0.02),
                    # xytext=(0, 0.01),
                    xycoords='data',
                    # textcoords='axes fraction',  # or 'offset pixels'
                    ha='left',  # center
                    va='bottom',
                    color=data[i]['peaks']['color'],
                    fontweight='500',
                )


def export_fig():
    """ Use Pillow to cut empty spaces and save the figure. refs:
    https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
    https://gist.github.com/thomastweets/c7680e41ed88452d3c63401bb35116ed
    https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil

    If cfg:fig:padding is set, remove white borders from the original figure and add the `padding`.

    :path: where to write figure image.
        if not provided, calculate from data[1]['file'] by replacing the extension.

    extension is taken from:
        1) cfg:export:path, 2) cfg:export:type, 3) 'png',
    """
    global fig

    # ToDo: check if the extension is supported by Pillow
    suffix = cfg['export']['type'].strip('.') if cfg['export']['type'] else 'png'
    path = Path(cfg['export']['path']).with_suffix(f'.{suffix}')

    # Render fig and pass it to Pillow.Image
    # fig.draw_without_rendering()
    fig.canvas.draw()
    rgba = np.asarray(fig.canvas.buffer_rgba())
    im = Image.fromarray(rgba)
    # im.show()

    # Adjust padding
    padding = cfg['fig']['padding']
    if padding:
        padding = np.asarray([-1 * padding, -1 * padding, padding, padding])
        im_ = im.convert('RGB')
        im_ = ImageOps.invert(im_)
        bbox = im_.getbbox()
        bbox = tuple(np.asarray(bbox) + padding)
        im = im.crop(bbox)

    log.info(f"Saving '{path}'")
    # Some file formats are not compatible with Image('RGBA')
    try:
        im.save(f'{path}')
    except Exception as expt:
        log.error(expt)
        log.info(f"Saving '{path}' without transparency")
        im.convert('RGB').save(f'{path}')


if __name__ == '__main__':
    pass
