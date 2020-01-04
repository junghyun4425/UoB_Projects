import matplotlib.pyplot as plt
import random
import numpy as np

def synapse():
    Vs1 = [V01]
    Vs2 = [V02]
    s1 = [0]
    s2 = [0]
    for i in range(0, t - 1):
        ds1 = -(s1[i] / tau_s)
        ds2 = -(s2[i] / tau_s)
        s1.append(s1[i] + ds1)
        s2.append(s1[i] + ds2)

        N1 = (El - Vs1[i] + RI + Rg * (Es - Vs1[i]) * s1[i]) / tau_m
        N2 = (El - Vs2[i] + RI + Rg * (Es - Vs2[i]) * s2[i]) / tau_m
        Vs1.append(Vs1[i] + N1)
        Vs2.append(Vs2[i] + N2)

        if Vs1[i + 1] >= Vt:
            Vs1[i + 1] = Vr
            s2[i + 1] += P
        if Vs2[i + 1] >= Vt:
            Vs2[i + 1] = Vr
            s1[i + 1] += P
    return Vs1, Vs2

t = 1000
tau_m = 20
tau_s = 10
El = -70
Vr = -80
Vt = -54
RI = 18
Rg = 0.15
Es = -80
P = 0.5
V01 = random.randint(-80, -54)
V02 = random.randint(-80, -54)

Vs1,Vs2 = synapse()
ts = np.linspace(0, 999, 1000)

plt.figure()
plt.plot(ts,Vs1,label='Neuron1')
plt.plot(ts,Vs2,label='Neuron2')
plt.xlabel("t (ms)")
plt.ylabel("V (mV)")
plt.title("Inhibitory with Es = -80mV")
plt.legend(loc=2)
plt.savefig('Question2_-80.png')

Es = 0
Vs1, Vs2 = synapse()
plt.figure()
plt.plot(ts,Vs1,label='Neuron1')
plt.plot(ts,Vs2,label='Neuron2')
plt.xlabel("t (ms)")
plt.ylabel("V (mV)")
plt.title("Excitatory with Es = 0mV")
plt.legend(loc=2)
plt.savefig('Question2_0.png')
plt.show()