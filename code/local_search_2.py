import time
import random
from math import dist
from tsp import TSP


# local search 2: hill climbing with 2-opt exchange
class LocalSearch2OPT(TSP):

    def __init__(self, file_name, time, seed=0):
        super(LocalSearch2OPT, self).__init__(file_name, time, seed)
        self.method = 'LS2'
        self.distance_matrix = None
        
    # calculate distance between every 2 nodes
    def calc_distanca_matrix(self):
        n = len(self.nodes)
        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                distance = round(dist(self.nodes[i], self.nodes[j]))
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

    # initial solution
    def init_solution(self):
        # r = random.random
        random.seed(self.seed)
        self.solution = self.generate_solution([i for i in range(len(self.nodes))])
        self.total_distance = self.calc_total_distance(self.solution)
    
    # generate solution randomly
    def generate_solution(self, prev_solution):
        solution = prev_solution[:]
        random.shuffle(solution)
        return solution

    # calculate the total distance of current solution
    def calc_total_distance(self, route):
        total_distance = 0
        for i in range(0, len(route)):
            edge = route[i - 1], route[i]
            total_distance += self.distance_matrix[edge[0]][edge[1]]
        return total_distance

    # core algorithm of hill climbing with 2-opt exchange
    def opt_2(self):
        start_time = time.time()
        route = self.solution[:]
        total_distance = self.total_distance
        not_improved = 0
        max_not_improved = 100
        
        while not_improved < max_not_improved:
            # implement 2-opt exchange to find a better route
            new_route, new_total_distance = self.search_neighbors(route, total_distance)
            time_cost = time.time() - start_time  
            if time_cost > self.time:
                return

            if new_total_distance < total_distance:
                route = new_route
                total_distance = new_total_distance
                # update optimal solution
                if new_total_distance < self.total_distance:
                    self.trace.append(
                        ("%.2f" % time_cost, new_total_distance))
                    self.total_distance = new_total_distance
                    self.solution = new_route[:]
                    not_improved = 0
            # restart hill climbing if quality not improved
            else: 
                route = self.generate_solution(route)
                total_distance = self.calc_total_distance(route)
                not_improved += 1
                
    # 2-opt exchange search
    def search_neighbors(self, route, quality):
        n = len(route)
        best_route = route[:]
        best_quality = quality
        
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                new_route = route[:]
                new_route[i:j+1] = reversed(route[i:j+1])
                new_total_distance = self.calc_total_distance(new_route)
                if new_total_distance < best_quality:
                    best_quality = new_total_distance
                    best_route = new_route
        
        return best_route, best_quality
        
    def main(self):
        self.read_file(self.file_name)
        self.calc_distanca_matrix()
        self.init_solution()
        self.opt_2()
        self.gen_outputs()


if __name__ == '__main__':
    ls2 = LocalSearch2OPT('Atlanta', 20, 2)
    ls2.main()
    print(ls2.nodes, ls2.seed, ls2.solution, ls2.total_distance)
