import random
import time
from tsp import TSP
import math
import numpy as np


# File for local search 1 simulated annealing.
# The BnB class is for main SA algorithm. Main function is the solve() function. When created, BnB class could take
# input of the file path, the time to stop and seed.
# This algorithm adopted reheating to escape local optimum
class SimulatedAnnealing(TSP):

    def __init__(self, file_name, time, seed=0):
        super(SimulatedAnnealing, self).__init__(file_name, time, seed)
        self.method = 'LS1'
        self.distance_matrix = None
        self.temperature = 10000
        self.ALPHA = 0.95
        self.total_distance = None
        self.attemps = 0
        self.changes = 0
        self.iter = 0
        self.start_time = 0
        self.first = True

    # calculate the acceptance criterion
    def metropolis(self, dist1, dist2):
        if self.temperature < 1e-25:
            return 0
        return math.exp(-abs(dist1 - dist2) / self.temperature)

    # generate a random neighbor
    def random_neighbor(self):
        random_successor = list(self.solution)
        n = len(random_successor)
        ln = random.randint(1, n - 1)
        i = random.randint(1, n - ln)
        random_successor[i:i + ln] = reversed(random_successor[i: i + ln])
        return random_successor

    # neighbor size related parameters setting
    def para(self):
        vertices = len(self.nodes)
        self.attemps = 50 * vertices
        self.changes = 5 * vertices

    # random neighbor search
    def search(self, route, distance):
        na = 0
        nc = 0
        n = len(self.nodes)
        current_route = route[:]
        current_distance = distance
        # stops searching until maximum searches or accepting times are reached
        while nc < self.changes and na < self.attemps:
            random_successor = current_route[:]
            length = random.randint(1, n - 1)
            i = random.randint(1, n - length)
            random_successor[i:i +
                             length] = reversed(random_successor[i: i + length])
            route_distance = self.calc_total_distance(random_successor)
            # initial temperature setting
            if self.first:
                self.temperature = (-abs(route_distance -
                                    current_distance)/np.log(0.9))
                self.first = False
            self.temperature = self.temperature * self.ALPHA
            if route_distance < current_distance or random.random() < self.metropolis(route_distance, current_distance):
                current_distance = route_distance
                current_route = random_successor
                nc += 1
                if current_distance < self.total_distance:
                    self.trace.append(
                        ("%.2f" % (time.time() - self.start_time), current_distance))
                    self.total_distance = current_distance
                    self.solution = current_route[:]
            na += 1
        return current_route, current_distance

    # main funciton of simulated annealing, reheat process is included
    def simulated_anneal(self):
        self.start_time = time.time()
        not_improved = 0
        max_iter_reheat = 5000
        prev_dist = self.total_distance
        prev_route = self.solution[:]
        # stop criterion setting, including maximum iterations and reheating times
        while not_improved < max_iter_reheat and self.iter < 1e6:
            time_diff = time.time() - self.start_time
            new_route, new_distance = self.search(prev_route, prev_dist)
            self.iter += 1
            # running time constrains
            if time_diff > self.time:
                break
            if new_distance != prev_dist:
                prev_route = new_route
                prev_dist = new_distance
                if prev_dist < self.total_distance:
                    not_improved = 0
            else:
                # reheat when no better solution is found in one search 
                random.shuffle(prev_route)
                prev_dist = self.calc_total_distance(prev_route)
                self.first = True
                not_improved += 1

    def main(self):
        self.read_file(self.file_name)
        self.calc_distance_matrix()
        self.para()
        self.init_solution()
        self.simulated_anneal()
        self.gen_outputs()


if __name__ == '__main__':
    ls1 = SimulatedAnnealing('../data/Atlanta.tsp', 5)
    ls1.main()
    print(ls1.total_distance)
