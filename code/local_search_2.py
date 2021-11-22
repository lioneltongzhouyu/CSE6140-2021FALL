import time
from tsp import TSP


# local search 2: 2-opt exchange
class LocalSearch2OPT(TSP):

    def __init__(self, file_name, time, seed=0):
        super(LocalSearch2OPT, self).__init__(file_name, time, seed)
        self.method = 'LS2'
        self.distance_matrix = None

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
                        self.trace.append(
                            ("%.2f" % time_cost, new_total_distance))
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
