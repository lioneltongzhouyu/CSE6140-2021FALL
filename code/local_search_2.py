import random
import time
from math import dist
from tsp import TSP

# local search 2: 2-opt exchange
class LocalSearch2OPT(TSP):
    
    def __init__(self, file_name, time, seed = 0):
        super(LocalSearch2OPT, self).__init__(file_name, time, seed)
        self.method = 'LS2'
        self.distance_matrix = None
        
    # calculate distance between every 2 nodes
    def calc_distanca_matrix(self):
        n = len(self.nodes)
        self.distance_matrix = [[ 0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                distance = round(dist(self.nodes[i], self.nodes[j]))
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance
                
    # initial solution
    def init_solution(self):
        r = random.random
        random.seed(self.seed)
        self.solution = [i for i in range(len(self.nodes))]
        random.shuffle(self.solution, random = r)
        self.total_distance = self.calc_total_distance(self.solution)

    # calculate the total distance of current solution
    def calc_total_distance(self, route):
        total_distance = 0
        for i in range(0, len(route)):
            edge = route[i - 1], route[i]
            total_distance += self.distance_matrix[edge[0]][edge[1]]
        return total_distance      
        
    # core algorithm of 2-opt 
    def opt_2(self):
        n = len(self.nodes)
        start_time = time.time()
        improved = True
        while improved:
            improved = False
            prev_route = self.solution
            for i in range(0, n - 1):
                for j in range(i + 1, n):
                    new_route = prev_route[:]
                    new_route[i:j+1] = reversed(prev_route[i:j+1])
                    new_total_distance = self.calc_total_distance(new_route)
                    time_cost = time.time() - start_time
                    if time_cost > self.time:
                        return
                    if new_total_distance < self.total_distance:
                        self.trace.append(("%.2f" % time_cost, new_total_distance))
                        self.total_distance = new_total_distance
                        self.solution = new_route
                        improved = True
    
    def main(self):
        self.read_file(self.file_name)
        self.calc_distanca_matrix()
        self.init_solution()
        self.opt_2()
        self.gen_outputs()
    
if __name__ == '__main__':
    ls2 = LocalSearch2OPT('Atlanta', 1)
    ls2.main()
    print(ls2.nodes, ls2.seed, ls2.solution, ls2.total_distance)