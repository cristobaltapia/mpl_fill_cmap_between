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
