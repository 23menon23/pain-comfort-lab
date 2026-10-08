"""Shared chart colours and style, so every figure in the lab reads the same way."""

import matplotlib.pyplot as plt

COLORS = {
    'comfort': '#287baf',   # blue
    'pain': '#d45755',      # red
    'neutral': '#8a8a8a',   # gray, always drawn with an x marker
    'accent': '#6a3d9a',    # purple: our direction, the chosen layer
}
MARKERS = {'comfort': 'o', 'pain': 's', 'neutral': 'x'}


def use_lab_style():
    plt.rcParams.update({'figure.dpi': 110, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.alpha': 0.25, 'legend.frameon': False})
