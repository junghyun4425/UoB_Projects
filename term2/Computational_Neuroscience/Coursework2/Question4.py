from numpy import *
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename,T):

    data_array = [T(line.strip()) for line in open(filename, 'r')]

    return data_array

def cal_STA(stim, data_array, width, sample_rate, interval, nec_adj):
    interval /= sample_rate
    time_bin = int(width / sample_rate)
    sta = np.zeros(time_bin)
    spike_tmp = np.nonzero(data_array)[0]
    spike_times=[]

    # necessarily adjacent case
    if nec_adj == 1:
        for i in range(0, len(spike_tmp)):
            index_s = spike_tmp[i] + interval
            if data_array[int(index_s)] != 0:
                check_s = data_array[int(spike_tmp[i]) + 1:int(spike_tmp[i] + interval)]
                if sum(check_s) == 0:
                    spike_times.append(spike_tmp[i])
    # not necessarily adjacent case
    else:
        for i in range(0, len(spike_tmp)):
            index_s = spike_tmp[i] + interval
            if data_array[int(index_s)] != 0:
                spike_times.append(spike_tmp[i])

    num = len(spike_times)
    for tau in range(0, time_bin):
        dist = 0
        windows = []
        for i in range(0, num):
            if spike_times[i] < tau:
                dist += 1
            windows.append(stim[spike_times[i] - tau])

        sta[tau] = sum(windows) / (num - dist)
    return sta

stimulus=load_data("stim.dat",float)
spikes=load_data("rho.dat",int)

sample_rate = 2
width = 100
interval = [2, 10, 20, 50]

sta_adj = []
sta_not_adj = []
for i in range(0, 4):
    sta_adj.append(cal_STA(stimulus, spikes, width, sample_rate, interval[i], 1))
    sta_not_adj.append(cal_STA(stimulus, spikes, width, sample_rate, interval[i], 0))
time = np.arange(0, width / sample_rate)

plt.figure()
plt.plot(time, sta_adj[0], label='2ms')
plt.plot(time, sta_adj[1], label='10ms')
plt.plot(time, sta_adj[2], label='20ms')
plt.plot(time, sta_adj[3], label='50ms')

plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Stimulus')
plt.title('STA (spikes are necessarily adjacent)')
plt.savefig('adjacent.png')

plt.figure()
plt.plot(time, sta_not_adj[0], label='2ms')
plt.plot(time, sta_not_adj[1], label='10ms')
plt.plot(time, sta_not_adj[2], label='20ms')
plt.plot(time, sta_not_adj[3], label='50ms')

plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Stimulus')
plt.title('STA (spikes are not necessarily adjacent)')
plt.savefig('notnecessarilyadjacent.png')
plt.show()
