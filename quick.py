import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getRotMat(euler):
    N, dim = euler.shape
    d = np.zeros((N,3,3))
    for i in range(0, N):
        ph = euler[i,0]
        th = euler[i,1]
        ps = euler[i,2]
        d[i,0,0] = np.cos(th)*np.cos(ph)
        d[i,0,1] = np.sin(ps)*np.cos(th) -np.cos(ph)*np.sin(ps)
        d[i,0,2] = np.cos(ps)*np.sin(th)*np.cos(ps) + np.sin(ph)*np.sin(ps)
        d[i,1,0] = np.cos(th)*np.sin(ps)
        d[i,1,1] = np.sin(ph)*np.cos(th)*np.sin(ps) + np.cos(th)*np.cos(ps)
        d[i,1,2] = np.cos(ph)*np.sin(th)*np.sin(ps) + np.sin(ph)*np.cos(ps)
        d[i,2,0] = -np.sin(th)
        d[i,2,1] = np.sin(th)*np.cos(th)
        d[i,2,2] = np.cos(ph)*np.cos(th)
    return d

def bdy2gnd(rotmat, vector):
    N, dim = vector.shape
    gnd_vec = np.zeros_like(vector)
    for i in range(0, N):
        gnd_vec[i,:] = np.matmul(rotmat[i,:,:],vector[i,:])
    return gnd_vec

def simpleSum(f):
    F = np.zeros_like(f)
    for i in range(1, len(f)):
        F[i] = F[i-1] + f[i-1]
    return F

def integral(f, dt):
    F = np.zeros_like(f)
    for i in range(1, len(f)):
        F[i] = F[i-1] + f[i-1]*dt[i-1]
    return F

bias = np.loadtxt('Data/0_accbias.txt')
data = np.loadtxt('Data/0_data.txt')

dt = data[:,1]/10**6  #seconds
gps = data[:,2:5]
gps = gps - gps[2,:]

euler = data[:,5:8]
rotmat = getRotMat(euler)
bias_gnd = np.matmul(rotmat[0,:,:],bias)
acc = data[:,11:14]
acc_gnd = bdy2gnd(rotmat, acc)
print acc_gnd.shape

acc_gnd = acc_gnd-bias_gnd
vel = integral(acc_gnd, dt)
pos = integral(vel, dt)

plt.figure()
plt.plot(simpleSum(dt), pos)

plt.figure()
plt.plot(simpleSum(dt), acc)
plt.show()
