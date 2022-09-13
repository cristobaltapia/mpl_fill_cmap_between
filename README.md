# mpl_fill_cmap_between

Create fill_between-like plots filled with any matplotlib's colormap.

## Install

```bash
pip install mpl_fill_cmap_between
```


## Examples

The function `fill_cmap_between` (and also the function `fill_cmap_between_x`) can be used in the following manner:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_fill_cmap_between import fill_cmap_between, fill_cmap_between_x

x = np.linspace(-10, 10, 50)
y = x**2 - 40

fig = plt.figure(figsize=(4.8, 2.0))
ax = fig.add_subplot(111)

fill_cmap_between(x, y * 0.1, 0, ax=ax, cmap="viridis", kw_line_1=dict(color="k"),
                  kw_line_2=dict(color="k", lw=0.5))
ax.set_aspect("equal")

fig.tight_layout()
fig.savefig("example.pdf", dpi=300)
```

![Example](examples/example.png)


The plot can also be rotated by an angle from a given origin:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_fill_cmap_between import fill_cmap_between, fill_cmap_between_x

x = np.linspace(0, 10, 50)
y = (x - 5)**2 - 10

fig = plt.figure(figsize=(4.8, 2.0))
ax = fig.add_subplot(111)

fill_cmap_between(x, y * 0.1, 0, ax=ax, cmap="viridis", kw_line_1=dict(color="k"),
                  kw_line_2=dict(color="k", lw=0.5), angle=40, origin=(10, 0))
ax.set_aspect("equal")
ax.grid(True, ls=":")

fig.tight_layout()
fig.savefig("example_02.png", dpi=300)
```

![Example](examples/example_02.png)
