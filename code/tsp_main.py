# entry file of the whole project
# should be running in the following command:
# python3 tsp_main.py -inst <file_name> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]
import sys
import getopt
from local_search_2 import LocalSearch2OPT
from sa import SimulatedAnnealing
from mst import MST_APPROX
from tsp import TSP
from BnB import BnB


def main(argv):

    file_name, alg, time, seed = None, None, None, 0
    for i, arg in enumerate(argv):
        if arg == '-inst' and i + 1 < len(argv):
            file_name = argv[i + 1]
        elif arg == '-alg' and i + 1 < len(argv):
            alg = argv[i + 1]
        elif arg == '-time' and i + 1 < len(argv):
            time = int(argv[i + 1])
        elif arg == '-seed' and i + 1 < len(argv):
            seed = int(argv[i + 1])

    if file_name and alg and time >= 0:
        print("inst: ", file_name, " alg: ", alg,
              " time: ", time, " seed: ", seed)
        tsp = TSP(file_name, time, seed)
        if alg == 'LS2':
            tsp = LocalSearch2OPT(file_name, time, seed)
        elif alg == 'LS1':
            tsp = SimulatedAnnealing(file_name, time, seed)
        elif alg == 'BnB':
            tsp = BnB(file_name, time, seed)
        elif alg == 'Approx':
            tsp = MST_APPROX(file_name, time, seed)

        tsp.main()
        print("solution: ", tsp.solution)
        print("quality: ", tsp.total_distance)
        print("trace: ", tsp.trace)

    else:
        print('Invalid input')
        print(
            'tsp_main.py -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff_in_seconds> [-seed <random_seed>]')


if __name__ == "__main__":
    main(sys.argv[1:])
