import numpy as np

def load_data(filename,T):

    data_array = [T(line.strip()) for line in open(filename, 'r')]

    return data_array

def cal_coeff(data_array, interval):
    cnt = 0
    intervals = []
    for i in range(0,len(data_array)):
        cnt += 1
        if data_array[i] != 0:
            all_intv = cnt * interval
            intervals.append(all_intv)
            cnt = 0

    avg = np.mean(intervals)
    std_dev = np.std(intervals)
    coeff = std_dev / avg
    return coeff

def cal_fano(data_array, win_size, big_t, sample_rate):
    width = int(win_size / sample_rate)
    width_range = 0
    spike_count = []
    for i in range(0, int(big_t / win_size)):
        cnt = 0
        for j in range(width_range, width_range + width):
            if data_array[j] == 1:
                 cnt += 1
        spike_count.append(cnt)
        width_range += width

    avg = np.mean(spike_count)
    var = np.var(spike_count)
    fano = var / avg

    return fano

Hz=1.0
sec=1.0
min=60*sec
ms=0.001

big_t=20*min
win_size = [10*ms, 50*ms, 100*ms]
sample_rate = 2 * ms

spikes=load_data("rho.dat",int)

coeff = cal_coeff(spikes, sample_rate)
print("Coefficient: ", coeff)

print("Fano factor [10, 50, 100]ms")
fano_10ms = cal_fano(spikes, win_size[0], big_t, sample_rate)
print(fano_10ms)
fano_50ms = cal_fano(spikes, win_size[1], big_t, sample_rate)
print(fano_50ms)
fano_100ms = cal_fano(spikes, win_size[2], big_t, sample_rate)
print(fano_100ms)