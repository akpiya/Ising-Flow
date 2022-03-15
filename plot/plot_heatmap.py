import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.style.use(['science',"no-latex"])
offsets = [0, 2, 4, 6, 8]
T = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
directory = "../data/heatmap/"
# PIV speed trends seem to be less speed than visually observed
#
def plot_heatmap(show):
    arr = np.genfromtxt(directory + "horizontal_speed_matrix_new.csv", delimiter=",")
    ax = plt.gca()
    #arr = np.vstack((arr, np.zeros((1, arr.shape[1])))) 
    x = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    y = [0, 2, 4, 6, 8, 10]
    X, Y = np.meshgrid(x, y)
    shw = plt.pcolor(X, Y, arr, cmap = "binary_r", edgecolors = 'k', shading = 'auto')
    
    #ax.set(xticklabels = [0, 1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10])
    #ax.set(yticklabels = [10, 8, 6, 4, 2, 0])
    ax.set_xticks([1, 3, 5, 7, 9])
    ax.set_yticks(y)
    #ax.set_xticklabels([1, 3, 5, 7, 9], rotation=90)
    #ax.set_yticklabels([10, 8, 6, 4, 2, 0])
    # ax.set_xticklabels(x)
    # ax.set_yticklabels(y)
    bar = plt.colorbar(shw)
    if show:
        plt.show()

def plot_heatmap_cut(show):
    arr = np.genfromtxt(directory + "horizontal_speed_matrix_new_cut.csv", delimiter=",")
    ax = plt.gca()
    #arr = np.vstack((arr, np.zeros((1, arr.shape[1])))) 
    x = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    y = [0, 2, 4, 6, 8, 10]
    X, Y = np.meshgrid(x, y)
    shw = plt.pcolor(X, Y, arr, cmap = "binary_r", edgecolors = 'k', shading = 'auto')
    
    #ax.set(xticklabels = [0, 1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10])
    #ax.set(yticklabels = [10, 8, 6, 4, 2, 0])
    ax.set_xticks([1, 3, 5, 7, 9])
    ax.set_yticks(y)
    #ax.set_xticklabels([1, 3, 5, 7, 9], rotation=90)
    #ax.set_yticklabels([10, 8, 6, 4, 2, 0])
    # ax.set_xticklabels(x)
    # ax.set_yticklabels(y)
    bar = plt.colorbar(shw)
    if show:
        plt.show()

def offset_err(show):
    err = np.genfromtxt(directory + "offset_err.csv", delimiter=",")
    arr = np.genfromtxt(directory + "horizontal_speed_matrix_new.csv", delimiter=',')
    x = [0, 2, 4, 6, 8, 10]
    y = arr[:, 3]
    plt.errorbar(x, y, err.transpose(), marker = "o")
    if show:
        plt.show()

def temperature_err(show):
    err = np.genfromtxt(directory + "temperature_err.csv", delimiter=",")
    arr = np.genfromtxt(directory + "horizontal_speed_matrix_new.csv", delimiter=",") 
    x = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    y = arr[1, :]
    plt.errorbar(x, y, err, marker = "o")
    if show:
        plt.show()

def color_mesh():
    arr = np.genfromtxt(directory + "horizontal_speed_matrix_new.csv", delimiter=",")
    shw = plt.pcolormesh(arr, cmap = 'copper')
    ax = plt.gca()

    ax.set_xticklabels = [0, 1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    ax.set_yticklabels = [12, 10, 8, 6, 4, 2, 0]
    plt.colorbar(shw)
    plt.show()

if __name__ == "__main__":
    show = True
    name = "../data/plots/heatmap.pdf"
    plot_heatmap_cut(show)

    if not show:
        plt.savefig(name)
    