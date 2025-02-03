import numpy as np
import matplotlib.pyplot as plt

G = 1
L = 10
    
N = 100
a, b = 0, 100
E = (b-a)/N
nbrPart = 1

def verlet(x0,vx0,y0,vy0):
    x = np.zeros(N)
    y = np.zeros(N)
    x[0] = x0
    x[1] = x0 - E*vx0
    y[0] = y0
    y[1] = y0 - E*vy0
    for i in range(2,N-1) :
        x[i+1] = 2*x[i]-x[i-1]+E*E*f(x[i],a + i*E)
        y[i+1] = 2*y[i]-y[i-1]+E*E*g(y[i],a + i*E)
        #Boundry Condition : (rebondi)
        if x[i+1] > L : 
            x[i] = 2* L - x[i]
            x[i+1] = 2*x[i]-(2* L - x[i-1])+E*E*f(x[i],a + i*E)
        elif x[i+1] < 0 : 
            x[i] = - x[i]
            x[i+1] = 2*x[i]-(- x[i-1])+E*E*f(x[i],a + i*E)
        if y[i+1] > L : 
            y[i] = 2* L - y[i]
            y[i+1] = 2*y[i]-(2* L - y[i-1])+E*E*g(y[i],a + i*E)
        elif y[i+1] < 0 : 
            y[i] = - y[i]
            y[i+1] = 2*y[i]-(- y[i-1])+E*E*g(y[i],a + i*E)
    return [x,y]

def f(x,t) :
    return 0
def g(x,t) : 
    return -G

part = []
for i in range(nbrPart) :
    theta = np.random.uniform(0, np.pi*2)
    v = np.random.uniform(0,1)
    
    x0, vx0 = np.random.uniform(0,L) , v*np.cos(theta)
    y0, vy0 = np.random.uniform(0,L)  , v*np.sin(theta)
    
    [x,y] = verlet(x0, vx0, y0, vy0)
    part.append([x,y])
