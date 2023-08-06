"""
Provide the app default matplotlib settings.

https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/mpl-data/matplotlibrc
https://raw.githubusercontent.com/matplotlib/matplotlib/main/lib/matplotlib/mpl-data/matplotlibrc
See also: print(pprint.pformat(matplotlib.rcParams.keys()))
"""

__all__ = ['MPLRC']

MPLRC = {
    # FONT, FONTSIZE
    'font.size': 7.0,
    'font.family': ['Calibri', 'Roboto Condensed', 'DejaVu Sans', 'Roboto', 'Arial', 'sans-serif'],
    'axes.titlesize': 8.0,
    'axes.labelsize': 8.0,
    'axes.titleweight': 500,
    'axes.titlelocation': 'left',
    'xtick.labelsize': 8.0,
    'ytick.labelsize': 8.0,
    'legend.fontsize': 7.5,

    # 'patch.facecolor': 'white',

    'figure.constrained_layout.use': True,
    'figure.constrained_layout.h_pad': 5 / 72.0,
    'figure.constrained_layout.w_pad': 5 / 72.0,
    'figure.constrained_layout.hspace': 0.01,
    'figure.constrained_layout.wspace': 0.01,

    'figure.figsize': (125 / 25.4, 65 / 25.4),  # not used here
    'figure.dpi': 150,  # screen, # not used here
    'figure.edgecolor': 'white',
    'figure.facecolor': 'white',
    'figure.frameon': False,

    # 'figure.subplot.left': 0.05,
    # 'figure.subplot.right': 0.95,
    # 'figure.subplot.bottom': 0.06,
    # 'figure.subplot.top': 0.04,
    # 'figure.subplot.hspace': 0.01,
    # 'figure.subplot.wspace': 0.01,

    # 'savefig.bbox': 'tight',
    # 'savefig.directory': '',
    # 'savefig.dpi': 150,  # not used here
    # 'savefig.edgecolor': 'white',
    # 'savefig.facecolor': 'white',
    # 'savefig.format': 'png',
    # 'savefig.pad_inches': 0.1,
    # 'savefig.transparent': False,

    'lines.linewidth': 0.5,
    'axes.labelpad': 0.1,
    'axes.linewidth': 0.3,
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.titlepad': 5.0,  # in points
    # 'axes.titley': 1.0,  # fraction of the plot height
    'axes.xmargin': 0.01,
    'axes.ymargin': 0.01,

    'axes.grid': True,
    'axes.grid.which': 'both',
    'grid.linewidth': 0.1,
    'grid.alpha': 0.75,

    # TICKS
    'xtick.top': 'False',
    'xtick.bottom': 'True',
    'xtick.labeltop': 'False',
    'xtick.labelbottom': 'True',

    'xtick.direction': 'in',
    'xtick.major.pad': 1.5,
    'xtick.major.size': 2.5,
    'xtick.major.width': 0.3,
    'xtick.minor.pad': 1.4,
    'xtick.minor.size': 1.5,
    'xtick.minor.visible': True,
    'xtick.minor.width': 0.2,

    'ytick.direction': 'in',
    'ytick.major.pad': 1.5,
    'ytick.major.size': 2.5,
    'ytick.major.width': 0.3,
    'ytick.minor.pad': 1.4,
    'ytick.minor.size': 1.5,
    'ytick.minor.visible': True,
    'ytick.minor.width': 0.2,

    # LEGEND
    'legend.frameon': False,
    'legend.framealpha': 0.5,
    'legend.edgecolor': '#e0e0e0',
    'legend.borderpad': 0.2,
    'legend.labelspacing': 0.2,
    'legend.handlelength': 2.0,
    'legend.handleheight': 0.7,
    'legend.handletextpad': 0.5,
    'legend.borderaxespad': 0.2,
    'legend.columnspacing': 1.0,
}

if __name__ == '__main__':
    pass
