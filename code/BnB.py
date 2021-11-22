import random
import time
from math import dist
from tsp import TSP
import heapq


class Node:
    def __init__(self, path):
        self.path = path
        self.bound = 0

    def compute_length(self, distance_matrix):
        distance = 0
        for i in range(len(self.path)-1):
            distance += distance_matrix[self.path[i]][self.path[i+1]]
        return distance

    def __lt__(self, other):
        if self.bound < other.bound:
            return True
        else:
            return False


class BnB(TSP):
    
    def __init__(self, file_name, time, seed = 0):
        super(BnB, self).__init__(file_name, time, seed)
        self.method = 'BnB'
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


    # calculate the total distance of current solution
    def calc_total_distance(self, route):
        total_distance = 0
        for i in range(0, len(route)):
            edge = route[i - 1], route[i]
            total_distance += self.distance_matrix[edge[0]][edge[1]]
        return total_distance


    def calculate_bound(self, node):
        total_distance = node.compute_length(self.distance_matrix)
        n = len(self.nodes)
        visited = node.path[:]
        last_visit = node.path[-1]
        for i in range(len(visited), n):
            temp_min = float('inf')
            temp_next = 0
            for j in range(n):
                if j not in visited:
                    if self.distance_matrix[j][last_visit] < temp_min:
                        temp_min = self.distance_matrix[j][last_visit]
                        temp_next = j
            total_distance += temp_min
            last_visit = temp_next
            visited.append(temp_next)
        total_distance += self.distance_matrix[last_visit][0]
        return total_distance, visited


    def solve(self):
        n = len(self.nodes)
        v = Node([0])
        self.total_distance, self.solution = self.calculate_bound(v)
        v.bound = self.total_distance
        q = []
        heapq.heappush(q, v)
        start_time = time.time()
        while q:
            temp = heapq.heappop(q)
            bound = temp.bound
            time_cost = time.time() - start_time
            if time_cost > self.time:
                return
            if bound <= self.total_distance:
                if len(temp.path) == n - 1:
                    for i in range(n):
                        if i not in temp.path:
                            temp.path.append(i)
                    if temp.compute_length(self.distance_matrix) + self.distance_matrix[temp.path[-1]][0] < self.total_distance:
                        self.solution = temp.path
                        self.total_distance = temp.compute_length(self.distance_matrix) + self.distance_matrix[temp.path[-1]][0]
                        self.trace.append(("%.2f" % time_cost, self.total_distance))
                else:
                    temp_path = temp.path[:]
                    for i in range(n):
                        if i not in temp.path:
                            temp_path.append(i)
                            new_node = Node(temp_path[:])
                            temp_bound, _ = self.calculate_bound(new_node)
                            if temp_bound <= self.total_distance:
                                new_node.bound = temp_bound
                                heapq.heappush(q, new_node)
                            temp_path.pop()

    
    def main(self):
        self.read_file(self.file_name)
        self.calc_distanca_matrix()
        self.solve()
        self.gen_outputs()
    
if __name__ == '__main__':
    ls2 = BnB('Atlanta', 1)
    ls2.main()
    print(ls2.nodes, ls2.seed, ls2.solution, ls2.total_distance)