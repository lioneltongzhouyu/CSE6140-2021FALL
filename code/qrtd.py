from tqdm import tqdm
import matplotlib.pyplot as plt
from local_search_2 import LocalSearch2OPT
from sa import SimulatedAnnealing

K = 50
TIME = 100

optimal = {
    'Atlanta': 2003763,
    'Berlin': 7542,
    'Nyc': 1555060
}
ATLANTA = 2003763
BERLIN = 7542
NYC = 1555060

def process_data(p = 0):
    k = K
    file_name = 'Berlin'
    method = 'LS2'
    time_limit = TIME
    seed = 1
    all_data = []
    for i in range(k):
        seed = i + 1
        all_data.append([])
        with open('../output/{}_{}_{}_{}.trace'.format(file_name, method, time_limit, seed), 'r') as f:
            lines = f.readlines()
            for line in lines:
                runtime, quality = line.strip().split(',')
                all_data[i].append((float(runtime), int(quality)))
                # print(runtime, quality)
    
    # print(all_data)
    
    probability = p
    runtime_list = []
    for i in range(k):
        data = all_data[i]
        for runtime, quality in data:
            if (quality - optimal[file_name] ) / optimal[file_name] <= probability:
                runtime_list.append(runtime)
                print(runtime, p)
                break
            
    runtime_list.sort()
    # print(runtime_list, len(runtime_list), p)
    return runtime_list
                

def draw_plot(runtime_list0, runtime_list2, runtime_list4, runtime_list6, runtime_list8):
    n = 50
    x0, x2, x4, x6, x8 = [],[],[],[],[]
    y0, y2, y4, y6, y8 = [],[],[],[],[]
    for i, runtime in enumerate(runtime_list0):
        y0.append((i+1)/n)
        x0.append(runtime)
    for i, runtime in enumerate(runtime_list2):
        y2.append((i+1)/n)
        x2.append(runtime)
    for i, runtime in enumerate(runtime_list4):
        y4.append((i+1)/n)
        x4.append(runtime)
    for i, runtime in enumerate(runtime_list6):
        y6.append((i+1)/n)
        x6.append(runtime)
    for i, runtime in enumerate(runtime_list8):
        y8.append((i+1)/n)
        x8.append(runtime)
    
    plt.plot(x0, y0, label="opt", linewidth=2)
    plt.plot(x2, y2, label="2%", linewidth=2)
    plt.plot(x4, y4, label="4%", linewidth=2)
    plt.plot(x6, y6, label="6%", linewidth=2)
    plt.plot(x8, y8, label="8%", linewidth=2)
    
    # plt.plot(x, It, label="I(t)", color="green", linewidth=2)
    # plt.plot(x, Rt, label="R(t)", color="red", linewidth=2)
    plt.legend() 
    plt.xlabel('run-time[CPU sec]')
    plt.ylabel('P(solve)')
    plt.show()
    plt.savefig("matplotlib.png")
    
    
def run_tsp(city):

    sum = 0
    for i in tqdm(range(1, 51)):
        
        # ls2 = SimulatedAnnealing('Berlin', 200, i)
        ls2 = LocalSearch2OPT(city, TIME, i)
        ls2.main()
        print(ls2.total_distance) 
        if (ls2.total_distance == optimal[city]):
            sum += 1  
        print(sum)
        


if __name__ == '__main__':
    
    run_tsp('Berlin')
    
    runtime_list0 = process_data(0)
    runtime_list2 = process_data(0.02)
    runtime_list4 = process_data(0.04)
    runtime_list6 = process_data(0.06)
    runtime_list8 = process_data(0.08)
    
    draw_plot(runtime_list0, runtime_list2, runtime_list4, runtime_list6, runtime_list8)
    
        
    