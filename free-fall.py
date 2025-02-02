import numpy as np
import matplotlib.pyplot as plt

G = 1
    
N = 100
a, b = 0, 10
E = (b-a)/N
nbrPart = 50

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
    return [x,y]

def f(x,t) :
    return 0
def g(x,t) : 
    return -G

plt.figure()

ymax = 0
part = []
for i in range(nbrPart) :
    theta = np.random.uniform(0, np.pi/2)
    r = 0#np.random.uniform(0,1)
    vtheta = np.random.uniform(0, np.pi/2)
    v = np.random.uniform(0,1)
    
    x0, vx0 = r*np.cos(theta) , v*np.cos(vtheta)
    y0, vy0 = r*np.sin(theta) , v*np.sin(vtheta)
    
    [x,y] = verlet(x0, vx0,y0,vy0)

    if ymax < max(y) :
        ymax = max(y)
        
    plt.plot(x,y)
    
    part.append([x,y] ) #pour sauvegarder nos données dans un tableau


plt.ylim(0,ymax)
plt.xlim(0,2)


plt.show()