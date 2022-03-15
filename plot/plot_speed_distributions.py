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
    ret = []
    for i in range(num_files):
        filename = directory + name + "/" + prefix + "{:03d}".format(i) + suffix
        vx, vy = average_speed_file(filename)
        horizontal += vx
        vertical += vy
        ret.append((vy * 100 / 380))
    horizontal /= num_files
    vertical /= num_files
    return ret

def files(temp):
    counter = len(glob.glob1(temp, "*repl.vec"))
    return counter

def average_speed_file(filename):
    df = pd.read_csv(filename, sep = "\t")
    df = df.replace(['     nan'], '0.0000')
    df = df.astype(np.float64)
    return df['u'].mean(), df['v'].mean()

def v_x(offset, t):
    #T is along the horizontal axis
    #offsets are along the vertical axis
    
    print("Offset="+str(offset) + " Temperature="+("%.2f" % t))
    ret =  find_speed(t, offset)
    df = pd.DataFrame(ret, columns=["Speed"])
    df.to_excel("../data/heatmap/vy_distribution.xlsx")
    plt.hist(ret, bins=15, density = True)
    #plt.show()

def plot_from_source(name):
    directory = "../data/heatmap/" + name
    df = pd.read_excel(directory)
    plt.hist(df["Speed"], bins=15, density = True)
    plt.show()

if __name__ == "__main__":
    #v_x(2, 2.25)
    plot_from_source("vy_distribution.xlsx")
    #plt.savefig("../data/plots/VxDistribution.pdf")
    