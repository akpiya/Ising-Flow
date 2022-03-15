import os
import glob
import pandas as pd
import numpy as np

directory = "/Users/Akash/Documents/Projects/AcceptU/Ising Model/data/image_frames/"
prefix = "vec_piv_FFT_"
suffix = "_med_thrhld_repl.vec"

def files(temp):
    counter = len(glob.glob1(temp, "*repl.vec"))
    return counter

def average_speed_file(filename):
    df = pd.read_csv(filename, sep = "\t")
    df = df.replace(['     nan'], '0.0000')
    df = df.astype(np.float64)
    return df['u'].mean(), df['v'].mean()

def find_speed(t, offset):
    name = "GifOffset=" + str(offset) + "_T=" + ("%.2f" % t) 
    num_files = files(directory + name + "/")
    horizontal = 0
    vertical = 0
    for i in range(num_files):
        filename = directory + name + "/" + prefix + "{:03d}".format(i) + suffix
        vx, vy = average_speed_file(filename)
        horizontal += vx
        vertical += vy
    horizontal /= num_files
    vertical /= num_files
    return horizontal, vertical

if __name__ == "__main__":
    destination = directory + "../heatmap/"
    offsets = [0, 2, 4, 6, 8, 10]
    T = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    #T is along the horizontal axis
    #offsets are along the vertical axis
    horizontal_speed = []
    vertical_speed = []
    offset_err = []
    temperature_err = []
    for offset in offsets: 
        temp_x = []
        temp_y = []
        for t in T:
            print("Offset="+str(offset) + " Temperature="+("%.2f" % t))
            vx, vy = find_speed(t, offset)
            temp_x.append(abs(vx) * 100 / 380)
            temp_y.append(abs(vy) * 100 / 380)
            if (offset == 2):
                temperature_err.append(np.std(temp_x))
        horizontal_speed.append(temp_x)
        vertical_speed.append(temp_y)
        offset_err.append(np.std(temp_x))

    # horizontal_speed = horizontal_speed[::-1]
    # vertical_speed = vertical_speed[::-1]
    np.savetxt(destination+"horizontal_speed_matrix_new.csv", np.array(horizontal_speed), delimiter=',')
    np.savetxt(destination+"vertical_speed_matrix_new.csv", np.array(vertical_speed), delimiter=',')
    np.savetxt(destination+"offset_err.csv", np.array(offset_err), delimiter=',')
    np.savetxt(destination+"temperature_err.csv", np.array(temperature_err), delimiter=",")