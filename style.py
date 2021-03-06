"""style.py
Contains standard style for figures.
"""
import os
from matplotlib.colors import colorConverter
from matplotlib import rcParams
try:
    import seaborn as sns
    sns.set(style='ticks', palette='Set1') 
    sns.despine()
except:
    print('seaborn not installed')

save_fig    = True
plot_style  = ["pdf", "print", "presentation", "poster"][3]

# Figure size
# Only specify height in inch. Width is calculated from golden ratio.
height = 3.4   # inch
linewidth  = 1.0
cross_size = 9 # pt, size of cross markers

# Choose parameters for pdf or print
if plot_style == "pdf":
    figure_path = os.path.join(".", "figures")
    axes_color = "#bdbdbd" 
    text_color = "#636363"
    # Font
    latex_preamble      = [r'\usepackage[cmbright]{sfmath}']
    rcParams['text.latex.preamble'] = latex_preamble
    font_family         = 'sans-serif'
elif plot_style == "print":
    figure_path = os.path.join(".", "figures")
    axes_color = "#959595" 
    text_color = "#363636"
    # Font
    latex_preamble      = [r'\usepackage[T1,small,euler-digits]{eulervm}']
    font_family         = 'serif'
elif plot_style == "presentation":
    figure_path = os.path.join("..", "presentation", "figures")
    axes_color = "#959595" 
    text_color = "#363636"
    # Font
    latex_preamble      = [r'\usepackage[cmbright]{sfmath}']
    rcParams['text.latex.preamble'] = latex_preamble
    font_family         = 'sans-serif'
elif plot_style == "poster":
    figure_path = os.path.join("..", "poster", "figures") 
    axes_color = "#959595" 
    text_color = "#363636"
    # Font
    latex_preamble      = [r'\usepackage[cmbright]{sfmath}']
    rcParams['text.latex.preamble'] = latex_preamble
    font_family         = 'sans-serif'
    # Figure size
    #        cm  / 2.54 cm * 1.0 inch  
    height = 9.5 / 2.54     # inch
    linewidth  = 0.8
    cross_size = 9 # pt, size of cross markers

if not save_fig:
    height = 8.
    linewidth  = 2.0
    cross_size = 12 # pt, size of cross markers

# Figure size
from  scipy.constants import golden_ratio as gr
figsize  = (gr * height, 1. * height)

fontsize_labels         = 11    # pt, size used in latex document
fontsize_labels_axes    = fontsize_labels
fontsize_labels_title   = fontsize_labels
fontsize_plotlabel      = fontsize_labels       # for labeling plots with 'A', 'B', etc.
legend_ms  = 4  # scale of markers in legend


# Adapt the matplotlib.rc
rcParams['figure.figsize']      = figsize
rcParams['text.usetex']         = True
rcParams['font.family']         = font_family
rcParams['font.serif']          = 'Palatino'
rcParams['font.sans-serif']     = 'cmbright'
rcParams['font.weight']         = "light"
rcParams['figure.autolayout']   = True
rcParams['font.size']           = fontsize_labels
rcParams['xtick.labelsize']     = fontsize_labels
rcParams['ytick.labelsize']     = fontsize_labels
rcParams['legend.fontsize']     = fontsize_labels
rcParams['axes.labelsize']      = fontsize_labels_axes
rcParams['axes.titlesize']      = fontsize_labels_title
rcParams['legend.markerscale']  = legend_ms
rcParams['text.color']          = text_color
rcParams['xtick.color']         = text_color
rcParams['ytick.color']         = text_color
rcParams['axes.labelcolor']     = text_color
rcParams['axes.edgecolor']      = axes_color
rcParams['axes.grid']           = False
rcParams['lines.linewidth']     = linewidth

tick_params = {
                ## TICKS
                # see http://matplotlib.org/api/axis_api.html#matplotlib.axis.Tick
                'xtick.major.size'     : 3,      # major tick size in points
                'xtick.minor.size'     : 2,      # minor tick size in points
                'xtick.major.width'    : 0.5,    # major tick width in points
                'xtick.minor.width'    : 0.5,    # minor tick width in points
                'xtick.major.pad'      : 4,      # distance to major tick label in points
                'xtick.minor.pad'      : 4,      # distance to the minor tick label in points
                'xtick.direction'      : 'out',    # direction: in, out, or inout
                
                'ytick.major.size'     : 3,      # major tick size in points
                'ytick.minor.size'     : 2,      # minor tick size in points
                'ytick.major.width'    : 0.5,    # major tick width in points
                'ytick.minor.width'    : 0.5,    # minor tick width in points
                'ytick.major.pad'      : 4,      # distance to major tick label in points
                'ytick.minor.pad'      : 4,      # distance to the minor tick label in points
                'ytick.direction'      : 'out'    # direction: in, out, or inout
                }
rcParams.update(tick_params)
                


def fixticks(ax):    
    ax.grid(False)      # Turn of grid (distracts!)
    # Set spines to color of axes
    for t in ax.xaxis.get_ticklines(): t.set_color(axes_color)
    for t in ax.yaxis.get_ticklines(): t.set_color(axes_color)
    # Remove top and right axes & spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')




# Colors are layered: two types a four layers
# Source: http://colorbrewer2.org/
colors =   [
            "#08519c",
            "#9ecae1",
            "#a63603",
            "#fdae6b",
            "#54278f",
            "#bcbddc",
            "#006d2c",
            "#a1d99b"
            ]

