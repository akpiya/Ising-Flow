import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob

plt.style.use(['science',"no-latex"])

directory = "../data/image_frames/"
prefix = "vec_piv_FFT_"
suffix = "_med_thrhld_repl.vec"


def find_speed(t, offset):
    name = "GifOffset=" + str(offset) + "_T=" + ("%.2f" % t) 
    num_files = files(directory + name + "/")
    horizontal = 0
    vertical = 0
    retx = []
    rety = []

    for i in range(num_files):
        filename = directory + name + "/" + prefix + "{:03d}".format(i) + suffix
        vx, vy = average_speed_file(filename)
        horizontal += vx
        vertical += vy
        retx.append(abs(vx * 100 / 380))
        rety.append((vy * 100 / 380))
    horizontal /= num_files
    vertical /= num_files
    return retx, rety

def files(temp):
    counter = len(glob.glob1(temp, "*repl.vec"))
    return counter

def average_speed_file(filename):
    df = pd.read_csv(filename, sep = "\t")
    #df = df.dropna()
    df = df.replace(['     nan'], '0.0000')
    #print(df['u'])
    #df = df.astype(np.float64)
    return df['u'].mean(), df['v'].mean()


x, y = find_speed(2.25, 2)
plt.hist(y)
plt.show()
np.savetxt("../data/vx.csv",x,delimiter="\t")
np.savetxt("../data/vy.csv",y,delimiter="\t")
# plt.hist(x,bins=15,density=True)
# plt.show()