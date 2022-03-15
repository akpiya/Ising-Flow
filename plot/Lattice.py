import numpy as np
import gif
import matplotlib.pyplot as plt
from random import random, randint
from math import exp
from multiprocessing import Pool

class Lattice():

    def __init__(self,size,isRandom, offset):

        self.grid = np.ones(size)
        if isRandom:
            grid = np.random.rand(size[0], size[1])
            grid[grid < 0.5] = -1
            grid[grid >= 0.5] = 1
            self.grid = grid

        self.N = size[0] * size[1]
        self.size = size
        self.energy = []
        self.magnetization = []
        self.specific_heat = []
        self.susceptibility = []
        self.correlation = []
        self.starting_correlation_from_warmup = 0; #starts correlation x sweeps after warmup
        self.temperature = []
        self.correlation_distance = min(size[0] // 2, 10)
        self.correlations_per_sweep = 0 #number of correlations per sweep
        self.gif_sweep = -1 #number of sweeps after warmup for recording gifs
        self.gif_temperature = -1
        self.frames = [] #for gif saving
        self.offset = offset
        self.display_cycle = -1 #display status every x sweeps
        self.processes = 1 #number of processes running
        self.save = False
        
    def load_source(self, directory, offset, t): #constructor from a preloaded file.
        filename = directory + "Offset=" + str(offset) + "_T=" + ("%.2f" % t) + ".csv"
        latt = np.genfromtxt(filename, delimiter=",")
        self.__init__(latt.shape, False, offset)
        self.grid = latt
        
    def reset_grid(self):
        self.grid = np.ones(self.size)

    def sweeps(self, t, warmup_sweeps, total_sweeps):
        energy_sweep = []
        magnetization_sweep = []
        temperature_correlation = {}
        for i in range(total_sweeps):
            for _ in range(self.N):
                x, y = self.random_point()
                self.monte_carlo(x, y, t) 
            if (self.gif_sweep != -1 and t == self.gif_temperature and i > warmup_sweeps + self.gif_sweep):
                self.frames.append(self.plot()) 
            
            if i % self.display_cycle == 0 and self.display_cycle != -1:
                self.display_sweep(t, i)
            if i > warmup_sweeps:
                energy_sweep.append(self.total_energy())
                magnetization_sweep.append(self.total_magnetization())
            
            corr_data = {}
            if i >= self.starting_correlation_from_warmup + warmup_sweeps:
                for _ in range(self.correlations_per_sweep):
                    vals = self.correlation_sweep(self.random_point()[0], self.random_point()[1], self.correlation_distance)
                    for key in vals:
                        if key in corr_data:
                            corr_data[key] += vals[key]
                        else:
                            corr_data[key] = vals[key]

                for key in corr_data:
                    corr_data[key] /= self.correlations_per_sweep

                    if key in temperature_correlation:
                        temperature_correlation[key] += corr_data[key]
                    else:
                        temperature_correlation[key] = corr_data[key]

        for key in temperature_correlation:
            temperature_correlation[key] /= (total_sweeps - (self.starting_correlation_from_warmup + warmup_sweeps)) 
        
        if self.processes == 1:
            self.measure_statistics(t, energy_sweep, magnetization_sweep, temperature_correlation)
        else:
            return t, energy_sweep, magnetization_sweep, temperature_correlation, np.copy(self.grid)
        
        self.reset_grid()

    def monte_carlo(self, i, j, t):
        this_spin = self.spin_at(i,j)
        e_old = -1 * self.interaction(i, j)
        e_proposed = self.interaction(i, j)
        e_flip = e_proposed - e_old

        if e_flip < 0:
            this_spin *= -1
        else:
            r = random()
            if r <= exp(-1 * e_flip / t):
                this_spin *= -1
        self.grid[i, j] = this_spin
        
    def display_start(self, T, warmup_sweeps, measured_sweeps):
        ret = "\n\n****** Starting Simulation ******"
        ret += "\nOffset = "+str(self.offset)
        ret += "\nTemperature from " + str(T[0]) + " to " + str(T[-1]) + " for " + str(len(T)) + " points."
        ret += "\nStarting Correlations from Warm-up: " + str(self.starting_correlation_from_warmup)
        ret += "\nCorrelations per Sweep: " + str(self.correlations_per_sweep)
        ret += "\nExporting Gif after N Warmups: " + str(self.gif_sweep)
        ret += "\nDisplay Every N Sweep: " + str(self.display_cycle)
        print(ret)

    # The main method that gets called
    def simulate_single_process(self, T, warmup_sweeps, measured_sweeps):
        self.processes = 1
        self.display_start(T, warmup_sweeps, measured_sweeps)
        for t in T:
            self.sweeps(t, warmup_sweeps, warmup_sweeps + measured_sweeps)

    def simulate_multi_process(self, T, warmup_sweeps, measured_sweeps, num_processes):
        self.processes = num_processes
        self.display_start(T, warmup_sweeps, measured_sweeps)
        pool = Pool(processes = self.processes)
        results = pool.starmap(self.sweeps, [(t, warmup_sweeps, warmup_sweeps + measured_sweeps) for t in T])
        for i in range(len(results)):
            self.measure_statistics(results[i][0], results[i][1], results[i][2], results[i][3])
            #results[i][4].tofile("Offset="+str(self.offset)+"_T="+str(T[i])+".csv", sep=",")
            if self.save:
                temp = "%.2f" % T[i]
                np.savetxt("Offset="+str(self.offset)+"_T=" + temp +".csv", results[i][4], delimiter = ",")
   
    def interaction(self, i, j):
        return self.spin_at(i, j) * (self.spin_at(i,j + self.offset - 1)
                                    + self.spin_at(i+1, j + self.offset) 
                                    + self.spin_at(i-1, j + self.offset) 
                                    + self.spin_at(i, j + self.offset + 1))
    def export_gif(self, Name):
        gif.save(self.frames,Name+"="+str(self.offset)+"_T="+("%.2f"%self.gif_temperature)+".gif",duration = 60,unit="s",between="startend")

    def random_point(self):
        return randint(0, self.grid.shape[0] - 1), randint(0, self.grid.shape[1] - 1)

    def display_sweep(self, t, sweep):
        print("N="+str(self.grid.shape[0])+" T="+str(t)+" Sweep="+str(sweep))

    def total_energy(self):
        total = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                total += -1 * self.interaction(i, j)
        if self.offset == 0:
            return total / 2
        return total # shouldn't we not divide by 2 on the custom interaction? We don't recount the same interaction
    
    def total_magnetization(self):
        return abs(self.grid.sum())

    def correlation_sweep(self, i, j, dist):
        correlation = {}
        counts = {}

        for r in range(-dist,dist+1):
            for c in range(-dist,dist+1):
                if r == 0 and c == 0 :
                    continue
                distance = np.sqrt(r ** 2 + c ** 2)
                if distance in correlation:
                    correlation[distance]  += self.spin_at(i, j) * self.spin_at(i+r, j+c)
                    counts[distance] += 1
                else:
                    correlation[distance] = self.spin_at(i, j) * self.spin_at(i+r, j+c)
                    counts[distance] = 1
        ret = {}
        for key in sorted(correlation):
            ret[key] = correlation[key] / counts[key]
        return ret 

    def divide_list_by_scalar(self, array, scalar):
        temp = []
        for i in range(len(array)):
            temp.append(array[i] / scalar)
        return temp

    def spin_at(self, i, j):
        row = (i) % self.grid.shape[0]
        col = (j) % self.grid.shape[1]
        return self.grid[row, col]

    @gif.frame
    def plot(self):
        ax = plt.gca()
        ax.set(yticklabels = [])
        ax.set(xticklabels = [])
        
        if abs(self.grid.sum()) == self.grid.shape[0] * self.grid.shape[1]:
            cpy = np.ndarray(shape=(self.grid.shape[0], self.grid.shape[1], 3), dtype=int)
            for i in range(self.grid.shape[0]):
                for j in range(self.grid.shape[1]):
                    if (self.grid[i, j] == 1):
                        cpy[i, j] = np.array([255,255,255])
                    else:
                        cpy[i, j] = np.array([0,0,0])
            plt.imshow(cpy)
        else:
            plt.imshow(self.grid, cmap = "gray")
        

    def show_state(self):
        plt.imshow(self.grid,cmap = "gray")
        ax = plt.gca()
        plt.show()
    
    def save_state(self, directory, offset, temperature):
        path = directory + "Offset="+str(offset) + "_T="+str(temperature)+".csv"
        np.savetxt(path, self.grid, delimiter=",")
        
    def measure_statistics(self, t, energy_sweep, magnetization_sweep, correl):
       self.energy.append(np.mean(self.divide_list_by_scalar(energy_sweep, self.N)))
       self.magnetization.append(np.mean(self.divide_list_by_scalar(magnetization_sweep, self.N)))
       self.specific_heat.append( np.var(energy_sweep) / (t * t * self.N))
       self.susceptibility.append( np.var(magnetization_sweep ) / (t * self.N))
       self.correlation.append(correl)
       self.temperature.append(t)
