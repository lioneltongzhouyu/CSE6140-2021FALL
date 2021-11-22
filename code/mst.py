import time
from math import dist
from tsp import TSP
import heapq

# local search 2: 2-opt exchange


class MST_APPROX(TSP):

    def __init__(self, file_name, time, begin):
        super(MST_APPROX, self).__init__(file_name, time)
        self.method = 'MST_APPROX'
        self.total_distance = 0
        self.begin = begin

    def calc_distanca_matrix(self):
        n = len(self.nodes)
        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                distance = round(dist(self.nodes[i], self.nodes[j]))
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

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
        self.solution = self.preorder(self.begin) + [self.begin]
        for u, v in zip(self.solution[:-1], self.solution[1:]):
            self.total_distance += self.distance_matrix[u][v]

    def main(self):
        self.read_file(self.file_name)
        self.calc_distanca_matrix()
        self.MST_prim()
        self.trace_MST()
        self.gen_outputs()


if __name__ == '__main__':
    for i in range(1, 6):
        ls2 = MST_APPROX('Atlanta', 1, i)
        ls2.main()
        print(ls2.solution, ls2.total_distance)
