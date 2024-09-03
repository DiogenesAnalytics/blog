"""Themes for matplotlib."""

import matplotlib.pyplot as plt


def set_dark_theme() -> None:
    """Apply a dark theme to matplotlib with custom background colors."""
    # set the style to a dark theme
    plt.style.use("dark_background")

    # match website background
    plt.rcParams["figure.facecolor"] = "#181818"
    plt.rcParams["axes.facecolor"] = "#181818"
    plt.rcParams["axes.edgecolor"] = "#181818"
