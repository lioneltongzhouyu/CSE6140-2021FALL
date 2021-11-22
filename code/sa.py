import random
import time
from tsp import TSP
import math


# local search 1: simulated annealing
class SimulatedAnnealing(TSP):

    def __init__(self, file_name, time, seed=0):
        super(SimulatedAnnealing, self).__init__(file_name, time, seed)
        self.method = 'LS1'
        self.distance_matrix = None
        self.temperature = 500000
        self.iter = 0
        self.ALPHA = 0.998
        self.STOPPING_TEMP = 1e-5
        self.MAX_ITER = 10000

    # calculate the acceptance criterion
    def metropolis(self, route):
        return math.exp(-abs(self.calc_total_distance(route) - self.total_distance) / self.temperature)

    # generate and evaluate the random successor
    def successor(self):
        n = len(self.nodes)
        random_successor = list(self.solution)
        i, j = random.sample(range(0, n), 2)
        random_successor[i:j + 1] = reversed(random_successor[i: j + 1])
        route_distance = self.calc_total_distance(random_successor)
        if route_distance < self.total_distance or random.random() < self.metropolis(random_successor):
            self.total_distance = route_distance
            self.solution = random_successor
        self.temperature = self.ALPHA * self.temperature
        self.iter += 1

    # core function
    def simulated_anneal(self):
        start_time = time.time()
        self.init_solution()
        while (self.temperature > self.STOPPING_TEMP) and (self.iter < self.MAX_ITER) \
                and (time.time() - start_time) < self.time:
            self.successor()

    def main(self):
        self.read_file(self.file_name)
        self.calc_distanca_matrix()
        self.simulated_anneal()
        self.gen_outputs()


if __name__ == '__main__':
    ls1 = SimulatedAnnealing('Atlanta', 10, 4)
    ls1.main()
    print(ls1.total_distance)
