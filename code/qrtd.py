from tqdm import tqdm
import matplotlib.pyplot as plt
from local_search_2 import LocalSearch2OPT
from sa import SimulatedAnnealing

K = 50
TIME = 100

optimal = {
    'Atlanta': 2003763,
    'Berlin': 7542,
    'Nyc': 1555060,
    'Champaign': 52643
}

def process_data(p = 0, city = 'Berlin'):
    k = K
    file_name =  city
    # file_name = 'Champaign'
    method = 'LS1'
    time_limit = TIME
    seed = 0
    all_data = []
    for i in range(k):
        all_data.append([])
        with open('../output/{}_{}_{}_{}.trace'.format(file_name, method, time_limit, seed), 'r') as f:
            lines = f.readlines()
            for line in lines:
                runtime, quality = line.strip().split(',')
                all_data[i].append((float(runtime), int(quality)))
                # print(runtime, quality)
        seed = i + 1

    # print(all_data)
    
    probability = p
    runtime_list = []
    for i in range(k):
        data = all_data[i]
        for runtime, quality in data:
            if (quality - optimal[file_name] ) / optimal[file_name] <= probability:
                runtime_list.append(runtime)
                # print(runtime, p)
                break
            
    runtime_list.sort()
    # print(runtime_list, len(runtime_list), p)
    return runtime_list
                

def draw_plot(runtime_list0, runtime_list2, runtime_list4, runtime_list6, runtime_list8, city = 'Berlin'):
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
    
    plt.figure()
    
    plt.plot(x0, y0, label="opt", linewidth=2)
    plt.plot(x2, y2, label="2%", linewidth=2)
    plt.plot(x4, y4, label="4%", linewidth=2)
    plt.plot(x6, y6, label="6%", linewidth=2)
    plt.plot(x8, y8, label="8%", linewidth=2)
    
    # plt.xlim((0, 100))
    plt.xscale('log')
    plt.legend() 
    plt.grid()
    plt.xlabel('run-time[CPU sec]')
    plt.ylabel('P(solve)')
    plt.show()
    plt.savefig("qrtd{}.png".format(city))
    
    
def draw_boxplot(city):
    k = K
    file_name = city
    method = 'LS2'
    time_limit = TIME
    seed = 1
    data = []
    for i in range(k):
        seed = i + 1

        with open('../output/{}_{}_{}_{}.trace'.format(file_name, method, time_limit, seed), 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            runtime = last_line.strip().split(',')[0]
            data.append(float(runtime))
    
    plt.figure()
    plt.title('Boxplot of runtime')

    plt.xlabel(city)
    plt.ylabel('run-time[CPU sec]')
    plt.boxplot(data)
    plt.savefig("boxplot_{}.png".format(city))
    # print(data)

def draw_quality_box(city, val, label):
    method = 'SA'
    fig, ax = plt.subplots()
    ax.boxplot(val)
    ax.set_xticklabels(label)
    plt.title('{} {}'.format(city, method))
    plt.xlabel('Solution Quality')
    plt.ylabel('Solving time')
    plt.savefig("quality_boxplot_{}_{}.png".format(city, method))
    plt.show()

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
    
    # run_tsp('Berlin')
    # run_tsp('Champaign')
    # runtime_list0 = process_data(0, 'Berlin')
    # runtime_list2 = process_data(0.02)
    # runtime_list4 = process_data(0.04)
    # runtime_list6 = process_data(0.06)
    # runtime_list8 = process_data(0.08)
    
    # draw_plot(runtime_list0, runtime_list2, runtime_list4, runtime_list6, runtime_list8, 'Berlin')
    
    
    # runtime_list0 = process_data(0, 'Champaign')
    # runtime_list2 = process_data(0.02, 'Champaign')
    # runtime_list4 = process_data(0.04, 'Champaign')
    # runtime_list6 = process_data(0.06, 'Champaign')
    # runtime_list8 = process_data(0.08, 'Champaign')
    
    # draw_plot(runtime_list0, runtime_list2, runtime_list4, runtime_list6, runtime_list8, city='Champaign')
    
    
    
    # draw_boxplot('Berlin')
    # draw_boxplot('Champaign')

    # box plot
    runtime_list2 = process_data(0.002)
    runtime_list4 = process_data(0.008)
    runtime_list6 = process_data(0.02)
    runtime_list8 = process_data(0.05)
    draw_quality_box("Berlin", [runtime_list2, runtime_list4, runtime_list6, runtime_list8],
    ['0.5%','0.8%','2%','5%'])

    runtime_list2 = process_data(0.002, 'Champaign')
    runtime_list4 = process_data(0.008, 'Champaign')
    runtime_list6 = process_data(0.02, 'Champaign')
    runtime_list8 = process_data(0.05, 'Champaign')
    
    draw_quality_box("Champaign", [runtime_list2, runtime_list4, runtime_list6, runtime_list8],
    ['0.2%','0.8%','2%','5%'])
        
    