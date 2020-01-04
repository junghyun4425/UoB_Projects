import matplotlib.pyplot as plt
import numpy as np

def euler(t,Vt,Vr):
    Vs = [Vr]
    for i in range(0, t - 1):
        if Vs[-1] <= Vt:
            V = Vs[-1] + ((El - Vs[-1] + Rm * Ie) / tau)
        else:
            V = Vr
        Vs.append(V)
    return Vs

# milli second
t = 1000
tau = 10
El = -70
Vr = -70
Vt = -40
Rm = pow(10, 10)
Ie = 3.1*pow(10, -9)


Vs = euler(t,Vt,Vr)
ts = np.linspace(0, 999, 1000)

plt.xlabel("t (ms)")
plt.ylabel("V (mV)")
plt.title("Leaky Integrate and Fire model")
plt.plot(ts, Vs)
plt.savefig('Question1.png')
plt.show()
