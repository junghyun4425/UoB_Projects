import random as rnd
import numpy as np

def get_spike_train(rate,big_t,tau_ref):

    if 1<=rate*tau_ref:
        print("firing rate not possible given refractory period f/p")
        return []


    exp_rate=rate/(1-tau_ref*rate)

    spike_train=[]

    t=rnd.expovariate(exp_rate)

    while t< big_t:
        spike_train.append(t)
        t+=tau_ref+rnd.expovariate(exp_rate)

    return spike_train

def cal_coeff(spike_train):
    diff = []
    for i in range(len(spike_train) - 1):
        diff.append(spike_train[i + 1] - spike_train[i])

    avg = np.mean(diff)
    std_dev = np.std(diff)
    coeff = std_dev / avg

    return coeff

def cal_fano(spike_train, win_size, big_t):
    spike_count = np.zeros(int(big_t / win_size))
    for j in range(len(spike_train)):
        k = int(spike_train[j] / win_size)
        spike_count[k] += 1
    avg = np.mean(spike_count)
    var = np.var(spike_count)
    fano = var / avg

    return fano

Hz=1.0
sec=1.0
ms=0.001

rate=35.0 *Hz
tau_ref=0*ms

big_t=1000*sec
win_size = [10*ms, 50*ms, 100*ms]

print("Refractory period = 0")
spike_train = get_spike_train(rate, big_t, tau_ref)
coeff = cal_coeff(spike_train)
print("Coefficient: ", coeff)

print("Fano factor [10, 50, 100]ms")
fano_10ms = cal_fano(spike_train, win_size[0], big_t)
print(fano_10ms)
fano_50ms = cal_fano(spike_train, win_size[1], big_t)
print(fano_50ms)
fano_100ms = cal_fano(spike_train, win_size[2], big_t)
print(fano_100ms)

print("Refractory period = 5")
tau_ref = 5 * ms
spike_train = get_spike_train(rate, big_t, tau_ref)
coeff = cal_coeff(spike_train)
print("Coefficient: ", coeff)

print("Fano factor [10, 50, 100]ms")
fano_10ms = cal_fano(spike_train, win_size[0], big_t)
print(fano_10ms)
fano_50ms = cal_fano(spike_train, win_size[1], big_t)
print(fano_50ms)
fano_100ms = cal_fano(spike_train, win_size[2], big_t)
print(fano_100ms)