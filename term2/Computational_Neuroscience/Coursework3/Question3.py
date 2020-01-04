import matplotlib.pyplot as plt
import numpy as np

def euler(t,V0,Vt,Vr,Ie):
    Vs = [V0]
    cnt = 0
    for i in range(0, t - 1):
        if Vs[-1] <= Vt:
            V = Vs[-1] + ((El - Vs[-1] + Rm * Ie) / tau)
            Vs.append(V)
        else:
            Vs[-1] = Vr
            cnt += 1
    spike = cnt
    return spike

# milli second
t = 1000
tau = 10
El = -70
Vr = -70
V0 = -70
Vt = -40
Rm = pow(10, 10)
Ie_space = np.linspace(2.0,5.0,31) * pow(10, -9)

spikes = []
for Ie in Ie_space:
    spikes.append(euler(t,V0,Vt,Vr,Ie))

plt.figure()
plt.plot(Ie_space, spikes)
plt.xlabel("Ie (mA)")
plt.ylabel("Firing Rate")
plt.title("Firing rate of different electrode current")
plt.savefig('Question3_2.png')
plt.show()