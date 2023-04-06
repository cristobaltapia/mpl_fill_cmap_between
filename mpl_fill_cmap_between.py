from matplotlib.cm import get_cmap
from matplotlib.patches import Polygon
import numpy as np
from matplotlib.collections import QuadMesh
from numpy import cos, sin


def fill_cmap_between_x(y, x, x0, ax, alpha=None, cmap=None, vmin=None, vmax=None,
                        kw_line_1=None, kw_line_2=None, **kwargs):
    """
    y : arraylike
        y-coordinates
    x : arraylike
        x-coordinates
    x0 : float or arraylike (default: 0)
    ax : `obj`:Axes
        Matplotlib axes object
    alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).
    cmap : str or `~matplotlib.colors.Colormap`, optional
            A Colormap instance or registered colormap name. The colormap
            maps the *C* values to colors. Defaults to :rc:`image.cmap`.
    vmin, vmax : scalar, optional, default: None
            The colorbar range. If *None*, suitable min/max values are
            automatically chosen by the `~.Normalize` instance (defaults to
            the respective min/max values of *C* in case of the default linear
            scaling).
    kw_line_1 : dict
            Properties passsed to the line
    kw_line_2 : dict
            Properties passsed to the line at x0

    """
    if kw_line_1 is None:
        kw_line_1 = dict(color='none')
    if kw_line_2 is None:
        kw_line_2 = dict(color='none')

    x0 = np.ones(len(x)) * x0

    # Generate Quad mesh coordinates
    coords_x = np.empty((2 * x.size), dtype=x.dtype)
    coords_y = np.empty((2 * y.size), dtype=y.dtype)
    coords_x[0::2] = x0
    coords_x[1::2] = x
    coords_y[0::2] = y
    coords_y[1::2] = y

    coords = np.column_stack((coords_x, coords_y))

    Nx = x.size

    # Values for the colormap
    vals = np.empty((2 * Nx))
    vals[0::2] = x - x0
    vals[1::2] = x - x0

    collection = QuadMesh(1, Nx - 1, coordinates=coords, shading="gouraud", **kwargs)

    collection.set_array(vals)
    collection.set_alpha(alpha)
    collection.set_clim(vmin, vmax)
    collection.set_cmap(cmap)
    collection.autoscale_None()

    ax.add_collection(collection)

    ax.plot(x, y, **kw_line_1)
    ax.plot([x0, x0], [y[0], y[-1]], **kw_line_2)

    return ax


def fill_cmap_between(x, y, y0, ax, alpha=None, cmap=None, vmin=None, vmax=None,
                      kw_line_1=None, kw_line_2=None, angle=None, origin=None, **kwargs):
    """
    x : arraylike
            x-coordinates
    y : arraylike
            y-coordinates
    y0 : float or arraylike (default: 0)
    ax : `obj`:Axes
            Matplotlib axes object
    alpha : scalar, optional, default: None
            The alpha blending value, between 0 (transparent) and 1 (opaque).
    cmap : str or `~matplotlib.colors.Colormap`, optional
            A Colormap instance or registered colormap name. The colormap
            maps the *C* values to colors. Defaults to :rc:`image.cmap`.
    vmin, vmax : scalar, optional, default: None
            The colorbar range. If *None*, suitable min/max values are
            automatically chosen by the `~.Normalize` instance (defaults to
            the respective min/max values of *C* in case of the default linear
            scaling).
    kw_line_1 : dict
            Properties passsed to the line
    kw_line_2 : dict
            Properties passsed to the line at y0

    """
    if kw_line_1 is None:
        kw_line_1 = dict(color='none')
    if kw_line_2 is None:
        kw_line_2 = dict(color='none')

    if angle is not None:
        a = np.deg2rad(angle)
        if origin is None:
            origin = np.array([0, 0])

        ux = origin[0]
        uy = origin[1]

        rot = np.array([
            [cos(a), -sin(a), ux],
            [sin(a), cos(a), uy],
            [0, 0, 1],
        ])

    y0 = np.ones(len(y)) * y0
    x0 = x[:]

    # Generate Quad mesh coordinates
    coords_x = np.empty((2 * x.size), dtype=x.dtype)
    coords_y = np.empty((2 * y.size), dtype=y.dtype)
    coords_z = np.ones((2 * y.size), dtype=y.dtype)
    coords_x[0::2] = x
    coords_x[1::2] = x
    coords_y[0::2] = y0
    coords_y[1::2] = y

    coords = np.row_stack((coords_x, coords_y, coords_z))

    if angle is not None:
        coords = rot @ coords

    Nx = x.size
    w, h = 1, Nx - 1

    coords = coords.T[:, :2]
    coords = np.asarray(coords, np.float64).reshape((h + 1, w + 1, 2))

    # Values for the colormap
    vals = np.empty((2 * Nx))
    vals[0::2] = y - y0
    vals[1::2] = y - y0

    collection = QuadMesh(coordinates=coords, shading="gouraud", **kwargs)

    collection.set_array(vals)
    collection.set_alpha(alpha)
    collection.set_clim(vmin, vmax)
    collection.set_cmap(cmap)
    collection.autoscale_None()

    ax.add_collection(collection)

    if angle is not None:
        z = np.ones(len(x))
        x0, y0, _ = rot @ np.row_stack((x, y0, z))
        x, y, _ = rot @ np.row_stack((x, y, z))

    ax.plot(x, y, **kw_line_1)
    ax.plot(x0, y0, **kw_line_2)

    return ax
