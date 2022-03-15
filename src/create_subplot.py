import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Lattice import Lattice

offset = 2
t = 2.25
lattice = Lattice((100,100), False, offset)
lattice.load_source("../data/lastframes/", offset, t)
ax = plt.gca()

ax.set(yticklabels = [])
ax.set(xticklabels = [])
plt.imshow(lattice.grid, cmap = "gray")

plt.savefig("../data/Figures/inverted_figure/norm_frame.png", dpi=700)