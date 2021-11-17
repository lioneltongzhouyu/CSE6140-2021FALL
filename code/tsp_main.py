import sys, getopt
from local_search_2 import LocalSearch2OPT
from tsp import TSP

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"",["inst=", "alg=", "time=", "seed="])
    except getopt.GetoptError:
        print('tsp_main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff_in_seconds> [--seed <random_seed>]')
        sys.exit(2)
    
    # print(opts)
    file_name, alg, time, seed = None, None, None, 0
    for opt, arg in opts:
        if opt == '--inst':
            file_name = arg
        elif opt == '--alg':
            alg = arg
        elif opt == '--time':
            time = int(arg)
        elif opt == '--seed':
            seed = int(arg)
            
    if file_name and alg and time >= 0:
        print("inst: ", file_name, " alg: ", alg, " time: ", time, " seed: ", seed)
        tsp = TSP(file_name, time, seed)
        if alg == 'LS2':
            tsp = LocalSearch2OPT(file_name, time, seed)
        elif alg == 'LS1':
            pass
        elif alg == 'BnB':
            pass
        elif alg == 'Approx':
            pass
        
        tsp.main()
        print("solution: ", tsp.solution)
        print("quality: ", tsp.total_distance)
        print("trace: ", tsp.trace)
        
    else:
        print('Invalid input')
        print('tsp_main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff_in_seconds> [--seed <random_seed>]')
    

if __name__ == "__main__":
   main(sys.argv[1:])
