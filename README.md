# CSE6140/CX4140 Fall 2021 TSP Project

## 1 Overview

The Traveling Salesman Problem (TSP) arises in numerous applications such as vehicle routing,
circuit board drilling, VLSI design, robot control, X-ray crystallography, machine scheduling and
computational biology. In this project, 4 different algorithms are implemented
to solve the TSP problem.

## 2 Group Members

- Jia, Yuqi
- Wu, Shuyang
- Xu, Zihan
- Yu, Tongzhou


## 3 Algorithms

- Branch-and-Bound
- Construction Heuristics
- Local Search - Simulated Annealing
- Local Search - 2-opt Exchange & Hill Climbing


## 4 Usage

python3 tsp_main.py -inst <file_name> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]
    

## 5 Code Structure

- tsp_main.py: entry file
- tsp.py: base class that contains commen methods such as read_file, generate_outputs
- Bnb.py: child class that implments Branch-and-Bound algorithm
- mst.py: child class that implments Construction Heuristics algorithm
- sa.py: child class that implments Simulated Annealing algorithm
- local_search_2.py: tsp child class that implments 2-opt Exchange & Hill Climbing algorithm


