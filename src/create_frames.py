import numpy as np
import gif
import matplotlib.pyplot as plt
from random import random, randint
from Lattice import Lattice


def main():
	offsets = [10]
	T = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
	N = 100
	warmups = 1000
	measured = 8500

	for offset in offsets:
		lattice = Lattice((N, N), False, offset)
		lattice.display_cycle = 500
		lattice.save = True

		lattice.simulate_multi_process(T, warmups, measured,15)

if __name__ == "__main__":
	main()
