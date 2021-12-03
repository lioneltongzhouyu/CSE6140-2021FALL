import time
from math import dist
from tsp import TSP
import heapq

"""
Double Minimum Spanning Tree Algorithm
input:
    filename: name of the file containing the graph
    time: time limit for the algorithm
    begin: starting node
output:
    self.solution: list of nodes in the MST
    self.trace: time and possible result found by the algorithm
"""


class MST_APPROX(TSP):

    def __init__(self, file_name, time, begin):
        super(MST_APPROX, self).__init__(file_name, time)
        self.method = 'Approx'
        self.total_distance = 0
        self.begin = begin

    def MST_prim(self):
        n = len(self.nodes)
        self.adj_list = [[] for _ in range(n)]
        pq = []
        heapq.heappush(pq, (0, self.begin, -1))  # (distance, node, parent)
        visited = [False for _ in range(n)]
        while pq:
            _, node, parent = heapq.heappop(pq)
            if visited[node]:
                continue
            visited[node] = True
            if parent != -1:
                self.adj_list[parent].append(node)
            for v in range(n):
                if not visited[v]:
                    heapq.heappush(
                        pq, (self.distance_matrix[node][v], v, node))
            if all(visited):
                break

    def preorder(self, node):
        if not self.adj_list[node]:
            return [node]
        ret = [node]
        for v in self.adj_list[node]:
            ret += self.preorder(v)
        return ret

    def trace_MST(self):
        start_time = time.time()
        self.MST_prim()
        self.solution = self.preorder(self.begin) + [self.begin]
        for u, v in zip(self.solution[:-1], self.solution[1:]):
            self.total_distance += self.distance_matrix[u][v]
        self.trace.append(
            ("%.2f" % (time.time() - start_time), self.total_distance))

    def main(self):
        self.read_file(self.file_name)
        self.calc_distance_matrix()
        self.trace_MST()
        self.gen_outputs()


if __name__ == '__main__':
    ls2 = MST_APPROX('../data/Atlanta.tsp', 1, 1)
    ls2.main()
    print(ls2.solution, ls2.total_distance)
