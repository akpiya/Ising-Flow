import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from Lattice import Lattice

plt.style.use(['science',"no-latex"])

offset = 2
t = 2.25

fig = plt.figure(figsize=(8, 5), frameon=False)

directory = "/Users/Akash/Documents/Projects/AcceptU/Ising Model/data/image_frames/"
name = "GifOffset=" + str(offset) + "_T=" + str(t)
prefix = "vec_piv_FFT_"
suffix = "_med_thrhld_repl"
total = 0
v_x = []
v_y = []
for file in range(249):
	filename = directory + name + "/" + prefix + "{:03d}".format(file) + suffix + ".vec"
	df = pd.read_csv(filename, sep = "\t")
	df = df.replace(['     nan'], '0.0000')
	df = df.astype(np.float64)
	n = len(df['u'])
	v_x.append((df['u'].sum()/n) * 100 / 380)
	v_y.append(df['v'].sum()/n)
	total += 1
# ax[1, 0].xlim(right=0)
# ax[1, 0].xlim(left=-1)
plt.subplot(223)
plt.xlim(right=0)
plt.xlim(left=-1)
plt.ylim(bottom=0)
plt.ylim(top=5)
plt.xticks([-1, -0.5, 0])
plt.yticks([1, 3, 5])
plt.xlabel("Vx (sites/sweep)")
plt.ylabel("Probability")
plt.hist(v_x, density=True, bins = 20)


directory = "/Users/Akash/Documents/Projects/AcceptU/Ising Model/data/image_frames/"
name = "_GifOffset=" + str(offset) + "_T=" + str(t)
prefix = "vec_piv_FFT_"
suffix = "_med_thrhld_repl"
total = 0
v_x = []
v_y = []
for file in range(249):
	filename = directory + name + "/" + prefix + "{:03d}".format(file) + suffix + ".vec"
	df = pd.read_csv(filename, sep = "\t")
	df = df.replace(['     nan'], '0.0000')
	df = df.astype(np.float64)
	n = len(df['u'])
	v_x.append((df['u'].sum()/n) * 100 / 380)
	v_y.append(df['v'].sum()/n)
	total += 1
# ax[1, 1].xlim(right=0)
# ax[1, 1].xlim(left=-1)
plt.subplot(224)
plt.xlim(right=0)
plt.xlim(left=-1)
plt.ylim(bottom=0)
plt.ylim(top=5)
plt.xticks([-1, -0.5, 0])
plt.yticks([1, 3, 5])
plt.xlabel("Vx (sites/sweep)")
plt.ylabel("Probability")
plt.hist(v_x, density=True, bins=20)

lattice = Lattice((100,100), False, offset)
lattice.load_source("../data/lastframes/", offset, t)

plt.subplot(221)
plt.imshow(lattice.grid, cmap="gray")
plt.xticks([])
plt.yticks([])

plt.subplot(222)
plt.imshow(lattice.grid, cmap="gray_r")
plt.xticks([])
plt.yticks([])

plt.savefig("../data/Figures/inverted_figure/fourbyfour.pdf", dpi=1000)