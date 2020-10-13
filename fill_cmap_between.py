from matplotlib.cm import get_cmap
from matplotlib.patches import Polygon
import numpy as np


def cmap_polygon(x1, y1, x2, y2, y0, c1, c2, ax, cmap):
    patch = Polygon([(x1, y1), (x2, y2), (x2, y0), (x1, y0)], facecolor='none')
    x_min = np.min([x1, x2])
    x_max = np.max([x1, x2])
    y_min = np.min([y0, y1, y2])
    y_max = np.max([y0, y1, y2])

    ax.add_patch(patch)
    im = gradient_image(ax, [x_min, x_max, y_min, y_max], direction=1, cmap_range=(c1, c2),
                        zorder=1, cmap=cmap)

    im.set_clip_path(patch)


def cmap_polygon_x(x1, y1, x2, y2, x0, c1, c2, ax, cmap):
    patch = Polygon([(x1, y1), (x2, y2), (x0, y2), (x0, y1)], facecolor='none', zorder=10)
    x_min = np.min([x1, x0, x2])
    x_max = np.max([x1, x0, x2])
    y_min = np.min([y1, y2])
    y_max = np.max([y1, y2])

    ax.add_patch(patch)
    im = gradient_image(ax, [x_min, x_max, y_min, y_max], direction=0, cmap_range=(c1, c2),
                        zorder=1, cmap=cmap)
    im.set_clip_path(patch)


def fill_cmap_between_x(y, x, x0, ax, cmap=get_cmap("viridis"), c_min=None, c_max=None):
    """
    y : arraylike
        y-coordinates
    x : arraylike
        x-coordinates
    x0 : float or arraylike (default: 0)
    ax : `obj`:Axes
        Matplotlib axes object
    c_min : float
        Minimum value for the colormap
    c_max : float
        Maximum value for the colormap

    """
    N = float(x.size)

    if c_min is None:
        c_min = np.min(y)

    if c_max is None:
        c_max = np.max(y)

    for n, (xi, yi) in enumerate(zip(x, y)):
        if n + 1 == N: continue

        # Define the color range for the current polygon
        c_i = xi / (c_max - c_min) - c_min / (c_max - c_min)
        c_ii = x[n + 1] / (c_max - c_min) - c_min / (c_max - c_min)
        # Add colored polygon
        cmap_polygon_x(xi, yi, x[n + 1], y[n + 1], x0, c_i, c_ii, ax, cmap)

    ax.plot(x, y, color="k")  # Plot so the axes scale correctly
    ax.plot([x0, x0], [y[0], y[-1]], color='k', lw=0.5)

    return ax

def fill_cmap_between(x, y, y0, ax, cmap=get_cmap("viridis"), c_min=None, c_max=None):
    """
    x : arraylike
        x-coordinates
    y : arraylike
        y-coordinates
    y0 : float or arraylike (default: 0)
    ax : `obj`:Axes
        Matplotlib axes object
    c_min : float
        Minimum value for the colormap
    c_max : float
        Maximum value for the colormap

    """
    N = float(x.size)

    if c_min is None:
        c_min = np.min(y)

    if c_max is None:
        c_max = np.max(y)

    for n, (xi, yi) in enumerate(zip(x, y)):
        if n + 1 == N: continue

        # Define the color range for the current polygon
        c_i = yi / (c_max - c_min) - c_min / (c_max - c_min)
        c_ii = y[n + 1] / (c_max - c_min) - c_min / (c_max - c_min)
        # Add colored polygon
        cmap_polygon(xi, yi, x[n + 1], y[n + 1], y0, c_i, c_ii, ax, cmap)

    ax.plot(x, y, color="k")
    ax.plot([x[0], x[-1]], [y0, y0], color='k', lw=0.5)

    return ax


def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Taken from:
        https://matplotlib.org/devdocs/gallery/lines_bars_and_markers/gradient_bar.html#sphx-glr-gallery-lines-bars-and-markers-gradient-bar-py

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]], [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, interpolation='bicubic', vmin=0, vmax=1, **kwargs)

    return im
