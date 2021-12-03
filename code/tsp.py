from math import dist
import random


class TSP(object):
    def __init__(self, file_name, time, seed=0):
        self.file_name = file_name
        self.location = ''
        self.method = ''
        # cutoff time
        self.time = time
        self.seed = seed
        # nodes data from tsp file
        self.nodes = []
        self.total_distance = float('inf')
        self.solution = []
        self.trace = []

    # read tsp file
    def read_file(self, file_name):
        self.location = file_name.split('/')[-1].split('.')[0]
        with open('{}'.format(file_name), 'r') as f:
            name = f.readline().strip().split()[1]
            comment = f.readline().strip().split()[1]
            dimension = f.readline().strip().split()[1]
            edge_weight_type = f.readline().strip().split()[1]
            f.readline()

            for i in range(int(dimension)):
                x, y = f.readline().strip().split()[1:]
                self.nodes.append([float(x), float(y)])

    # generate output files
    def gen_outputs(self):
        with open('../output/{}_{}_{}_{}.sol'.format(self.location, self.method, self.time, self.seed), 'w') as f:
            f.write(str(self.total_distance))
            f.write('\n')
            f.write(','.join(map(str, self.solution)))

        with open('../output/{}_{}_{}_{}.trace'.format(self.location, self.method, self.time, self.seed), 'w') as f:
            for time, quality in self.trace:
                f.write('{},{}\n'.format(time, quality))

    # calculate distance between every 2 nodes
    def calc_distance_matrix(self):
        n = len(self.nodes)
        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
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
        random.shuffle(self.solution, random=r)
        self.total_distance = self.calc_total_distance(self.solution)

    # calculate the total distance of current solution
    def calc_total_distance(self, route):
        total_distance = 0
        for i in range(0, len(route)):
            edge = route[i - 1], route[i]
            total_distance += self.distance_matrix[edge[0]][edge[1]]
        return total_distance

    # implement specific algorithm
    def main(self):
        pass
