import matplotlib.pyplot as plt
import os 
import numpy as np
# from scipy.interpolate import make_interp_spline


optimal = {
    'Berlin': 7542,
    'Champaign': 52643
}

def data(time, city='Champaign', method='LS1'):
    command = 'time={} city={} method={} ./run_tsp.sh'.format(time, city, method)
    os.system(command)
    seed = 0
    quality = []
    while seed < 50:
        with open('../output/{}_{}_{}_{}.trace'.format(city, method, time, seed), 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            quality.append((int(last_line.strip().split(',')[1]) - optimal[city])/ (optimal[city]) * 100)
            seed += 1
    return np.asarray(quality)


def plot(arr0, arr1, arr2, arr3, arr4):
    all_data = np.stack((arr0, arr1, arr2, arr3, arr4))
    max_quality = np.amax(all_data)
    threshold = np.arange(0, max_quality, 0.5)
    meet0, meet1, meet2, meet3, meet4 = [],[],[],[],[]
    for i in range(len(threshold)):
        meet0.append(len(arr0[arr0 < threshold[i]])/50)
        meet1.append(len(arr1[arr1 < threshold[i]])/50)
        meet2.append(len(arr2[arr2 < threshold[i]])/50)
        meet3.append(len(arr3[arr3 < threshold[i]])/50)
        meet4.append(len(arr4[arr4 < threshold[i]])/50)
    plt.plot(threshold, meet0, label='0.1s')
    plt.plot(threshold, meet1, label='0.3s')
    plt.plot(threshold, meet2, label='1s')
    plt.plot(threshold, meet3, label='3.2s')
    plt.plot(threshold, meet4, label='10s')
    plt.legend()
    plt.xlabel("realative solution quality[%]")
    plt.ylabel('P(solve)')
    plt.show()
    plt.savefig('sqd.png')


if __name__ == '__main__':
    arr0 = data(0.1)
    arr1 = data(0.3)
    arr2 = data(1.0)
    arr3 = data(3.2)
    arr4 = data(10.0)
    plot(arr0, arr1, arr2, arr3, arr4)