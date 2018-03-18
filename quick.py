import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def integral(f, dt):
    F = np.zeros_like(f)
    for i in range(1, len(f)):
        F[i] = F[i-1] + f[i-1]*dt[i-1]
    return F

bias = np.loadtxt('Data/0_accbias.txt')
data = np.loadtxt('Data/0_data.txt')

dt = data[:,1]/10**6
gps = data[:,2:5]
gps = gps - gps[2,:]

acc = data[:,11:14] - bias
vel = integral(acc, dt)
pos = integral(vel, dt)

plt.figure
plt.plot(pos)
plt.show()

print gps
