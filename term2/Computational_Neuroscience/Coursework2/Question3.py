from numpy import *
import numpy as np
import matplotlib.pyplot as plt

def load_data(filename,T):

    data_array = [T(line.strip()) for line in open(filename, 'r')]

    return data_array

def cal_STA(stim, data_array, width, sample_rate):
    time_bin = int(width / sample_rate)
    sta = np.zeros(time_bin)
    spike_times = np.nonzero(data_array)[0]
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

# See some of data
stimulus=load_data("stim.dat",float)
plt.figure()
plt.plot(stimulus[0:100])
spikes=load_data("rho.dat",int)
plt.figure()
plt.plot(spikes[0:100])

sample_rate = 2
width = 100

sta = cal_STA(stimulus, spikes, width, sample_rate)
time = np.arange(0, width / sample_rate)
print('STA: ', sta)

plt.figure()
plt.plot(time, sta)
plt.xlabel('Time (ms)')
plt.ylabel('Stimulus')
plt.title('STA')
plt.savefig('STA.png')
plt.show()