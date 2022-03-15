from Lattice import Lattice
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    offsets = [10]
    T = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
    warmup = 0
    measured = 500
    
    for offset in offsets:
        for t in T:
            lattice = Lattice((100,100), False, offset)
            lattice.load_source("../data/lastframes/", offset, t)
            
            lattice.gif_temperature = t
            lattice.gif_sweep = 0
            lattice.display_cycle = 100
            
            lattice.simulate_single_process([t], warmup, measured)
            
            lattice.export_gif("../data/gifs3/GifOffset")

if __name__ == "__main__":
    main()
