class TSP(object):
    def __init__(self, file_name, time, seed = 0):
        self.file_name = file_name
        # cutoff time
        self.time = time
        self.seed = seed
        # nodes data from tsp file
        self.nodes = []
        self.total_distance = float('inf')
        self.solution = []

    # read tsp file
    def read_file(self, file_name):
        with open('../data/{}.tsp'.format(file_name), 'r') as f:
            name = f.readline().strip().split()[1] 
            comment = f.readline().strip().split()[1] 
            dimension = f.readline().strip().split()[1] 
            edge_weight_type = f.readline().strip().split()[1] 
            f.readline()

            for i in range(int(dimension)):
                x, y = f.readline().strip().split()[1:]
                self.nodes.append([float(x), float(y)])

    # implement specific algorithm
    def main(self):
        pass