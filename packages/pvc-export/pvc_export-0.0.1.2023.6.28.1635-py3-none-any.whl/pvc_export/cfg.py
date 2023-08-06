"""
Provide the main app settings container as a dictionary `cfg`.
Declare all fields that will be recognized in it.
The dict also serves as a prototype for saving a YAML user config.
Later, values loaded from a user config will only be applied
if they are present in `cfg` and of the same type.

To apply a YAML user config on top of this `cfg` dict later,
a custom config.update_dict() function is used. The function processes only dicts.
If a top level key in `cfg` is not of the dict type, like 'colors' here,
keep it compatible with copy.deepcopy(), and better keep its 'depth' less than or equal 1.
That is, if a key's value is a list, its elements should better be of a plain type, like int, str, bool, etc.
The same applies to the lists in dicts. Although pyyaml lib is used to load a user config,
prefer JSON compatible types; i.e. for containers, use dicts and lists not tuples or sets.

Only `config.py` imports the `cfg` dict directly from here.
"""

# HEADER is placed at the top of the YAML user config generated in config.create_config()
HEADER = f"""
# PVC-Export YAML configuration file.
# General format examples: https://pyyaml.org/wiki/PyYAML
# Recognised fields: see '{__file__}' in the package.
\n"""[1:]

#
# THE MAIN SETTINGS CONTAINER
#
cfg = {
    # The top level sub-containers are:
    # export: dict
    # fig: dict
    # colors: list
    # 1: dict
}

#
# EXPORT PARAMETERS
#
cfg['export'] = {}

# A filename 'template' where to save the generated figure image and *.csv files.
# A proper suffix will be applied by the respective export function.
# The path can be absolute or relative.
# When not provided, it is deduced from other settings, see `config.set_export_path()`
cfg['export']['path'] = ''

# file suffix for saving the figure image with Pillow.Image.save()
cfg['export']['type'] = ''

# A set of hexadecimal color values to pick from when assigning colors to plots.
# if the 'colors' list is not provided by a user config,
# it gets the default set of colors for plots from config.COLORS
cfg['colors'] = []

#
# FIGURE PARAMETERS
#
cfg['fig'] = {}

# The dpi is also preserved on saving the generated mpl figure
cfg['fig']['dpi'] = 150

# Figure [width, height] in mm.
# The height given above will be reserved for the plot area.
# The initial figure height will be set higher, to make enough space for titles.
# After adding all plots, the remaining empty white borders around the figure
# will be replaced with the padding given below.
cfg['fig']['size'] = [125, 55]

# The size of the padding in pixels.
# The padding replaces white borders around the figure after its rendering is completed.
cfg['fig']['padding'] = 15

# axes.xlim as [xmin, xmax]
cfg['fig']['xrange'] = []

# axes.ylim as [ymin, ymax]
cfg['fig']['yrange'] = []

#
# PLOT PARAMETERS
#
# The top level keys of integer type describe each plot/curve style,
# only one such key is present here, i.e. `1` below, the others are generated using it as a template
# and saved in a user config if requested. The keys also sets the order of the plot/curve appearance
# in the figure legend and title/description; i.e. lower numbers appear at the top.
# Each PVC file to load gets own param set collected under a key like `1` here,
# and the path to the file itself is provided therein.
cfg[1] = {}

# The PVC file with spec data to load. Env vars, like $HOME, are expanded.
# Globs expansion is not supported to maintain the idea of 'one file - one set of params'.
# The path can be absolute or relative.
# If a file name is given on command line, it replaces the value here or in user config.
# Also, if user config provides 2 file paths under keys 1 and 2 and one file is given on command line,
# key 1 gets the file from the command line and the file path in key 2 stays unchanged.
cfg[1]['file'] = ''

# The label to use in the plot legend and *.csv export headers.
# Keep empty to autofill from data.
cfg[1]['label'] = ''

# Text in the figure title corresponding to the file.
# Keep empty to autofill from data.
cfg[1]['title'] = ''

# Include or not the parent folder name in the title
# when the title is automatically generated from the file name.
cfg[1]['parent+'] = True

# Normalize or not the Y values by dividing the Y array by max(Y).
# Normalization is applied after 'yshift'-ing, if that is enabled.
# Note, 'yshift' (setting the level of 0 and thereby the value of max(Y))
# is not enforced in the normalization.
# i.e. `norm=True` might be not sensible with `yshift=0`
cfg[1]['norm'] = False

# [xmin_value, xmax_value]: use only data from xmin_value to xmax_value
# use all data when empty
cfg[1]['xrange'] = []

# [ymin_value, ymax_value]: use only data from ymin_value to ymax_value
# use all data when empty
cfg[1]['yrange'] = []

# Shift all Y by the given value if the value is of int or float.
# Positive values shift up, negative ones do down. The value of 0 shifts nowhere.
# If the value is 'min', shift down by min(Y).
# The 'yshift' is applied before 'norm'.
cfg[1]['yshift'] = 'min'

#
# RAW DATA LINE
#
# The original raw data are displayed as matplotlib.lines.Line2D
# Here is the line props container
cfg[1]['raw'] = {}

# Opacity
cfg[1]['raw']['alpha'] = 0.9

# Color as a hexadecimal value. Keep empty to autofill.
cfg[1]['raw']['color'] = ''

# matplotlib.lines.Line2D.set_linestyle
cfg[1]['raw']['linestyle'] = 'solid'

# matplotlib.lines.Line2D.set_linewidth
cfg[1]['raw']['linewidth'] = 0.25

# Do not plot the line if False
cfg[1]['raw']['show'] = False

#
# SMOOTHED LINE
#
# The raw data are smoothed with scipy.signal.savgol_filter(),
# and the smoothed line is displayed as matplotlib.lines.Line2D
# Here is the line props container
cfg[1]['smooth'] = {}

# Opacity
cfg[1]['smooth']['alpha'] = 0.667

# Color as a hexadecimal value. Keep empty to autofill.
cfg[1]['smooth']['color'] = ''

# See matplotlib.lines.Line2D.set_linestyle
cfg[1]['smooth']['linestyle'] = 'solid'

# matplotlib.lines.Line2D.set_linewidth
cfg[1]['smooth']['linewidth'] = 1.25

# Do not plot the line if False
cfg[1]['smooth']['show'] = True

#
# PEAKS SCATTER
#
# Peak positions are detected with scipy.signal.scipy_signal_find_peaks(),
# and plotted as a scatter plot, see matplotlib.pyplot.scatter
# Here is the plot props container
cfg[1]['peaks'] = {}

# Opacity
cfg[1]['peaks']['alpha'] = 0.9

# Color as a hexadecimal value. Keep empty to autofill.
cfg[1]['peaks']['color'] = ''

# size of marker edges
cfg[1]['peaks']['linewidth'] = 1.5

# marker size in points**2 (typographic point = 1/72 in.)
cfg[1]['peaks']['size'] = 20

# marker style
# See matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
cfg[1]['peaks']['style'] = 'D'

# do not plot it if False
cfg[1]['peaks']['show'] = True

if __name__ == '__main__':
    pass
