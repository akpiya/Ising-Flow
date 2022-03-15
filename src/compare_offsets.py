from Lattice import Lattice 
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    offset2 = Lattice((50, 50), False, 2)
    offset0 = Lattice((50,50), False, 0)
    T = np.linspace(1, 5, 10)
    warmups = 1000 
    measured = 2000 
    offset0.display_cycle = 200
    offset2.display_cycle = 200

    offset0.simulate_multi_process(T, warmups, measured, 4)
    offset2.simulate_multi_process(T, warmups, measured, 4)

    fig, axs = plt.subplots(2, 2)

    axs[0, 0].plot(offset0.temperature, offset0.energy)
    axs[0, 0].plot(offset2.temperature, offset2.energy, marker = "+")

    axs[1, 0].plot(offset0.temperature, offset0.magnetization)
    axs[1, 0].plot(offset2.temperature, offset2.magnetization, marker = "+")

    axs[0, 1].plot(offset0.temperature, offset0.specific_heat)
    axs[0, 1].plot(offset2.temperature, offset2.specific_heat, marker = "+")

    axs[1, 1].plot(offset0.temperature, offset0.susceptibility)
    axs[1, 1].plot(offset2.temperature, offset2.susceptibility, marker = "+")
    plt.show()