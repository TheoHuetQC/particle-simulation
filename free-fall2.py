import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 1

L  = 10
N = 1000
NbrPart = 5
E = 1/N

def f(x,t) :
    return np.array([0 ,-G])

#condition initial aléatoire
#r0
x0 = np.random.uniform(0, L, NbrPart)
y0 = np.random.uniform(0, L, NbrPart)
position = np.array([x0, y0]) 

#condition initial pour pouvoir appliquer Verlet sans vitesse
#v0
v = np.random.uniform(0, 1,NbrPart)
theta = np.random.uniform(0, np.pi*2, NbrPart)

position_befor = np.array([position[0] - E * v *np.cos(theta), position[1] - E * v*np.sin(theta)])

#pour l'aniamtion
positions_for_animation = [] 
t = []
save_frames = True  #Sauvegarde des images pour l'animation
animation_interval = 50   #Intervalle pour l'animation

#calcul des trajectoires avec Verlet
for i in range(2,N-1) :
    position_test = 2 * position - position_befor + E * E #* f(position, i * E)

    #Boundry Condition : (rebondi)
    #pour x
    if position_test[0] > L : 
        position_test[0], position_test[1] = 2 * L - position[0], position[1]
        position_test[0] = 2 * position_test[0] -(2 * L - position_befor[0])+ E * E #* f(position_test, i * E)
    elif position_test[0] < 0 :
        position_test[0], position_test[1] = - position[0], position[1]
        position_test[0] = 2 * position_test[0] - (- position_befor[0])+ E * E #* f(position_test, i * E)
    #pour y
    if position_test[1] > L : 
        position_test[1], position_test[0] = 2 * L - position[1], position[0]
        position_test[1] = 2 * position_test[1] -(2 * L - position_befor[1])+ E * E #* f(position_test, i * E)
    elif position_test[1] < 0 :
        position_test[1], position_test[0] = - position[1], position[0]
        position_test[1] = 2 * position_test[1] - (- position_befor[1])+ E * E #* f(position_test, i * E)
    
    position_befor = position
    position = position_test

    # Animation
    if save_frames and (i % animation_interval == 0) :
        positions_for_animation.append(np.copy(position))
        t.append(i)

plt.figure()
plt.plot(t,positions_for_animation)
plt.show()



"""


⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⣰⡟⢻⡆
⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣶⣦⣤⣴⡟⠀⠀⢿⣶⣤⣤⣴⠾⣿
⠀⠀⠀⢀⣴⠟⠋⠁⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿ ⠀
⠀⠀⢠⡿⠁⠀⢀⣀⣤⣤⣀⡀⠀⠀⠀⠀⠈⠛⠛⠀⠀⢶⡤⣿⣀⣀
⠀⢀⣿⠁⢠⡾⠛⠉⠀⠀⠉⠻⣦⣀⡴⠞⠛⠛⠛⠷⣦⣀⡾⡒⠤
⠀⢸⡇⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠘⠋⠀⠀⠀⠀⠀⠀⠘⣿
⠀⠸⣇⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿ ⠀⠀
⠀⠀⢻⡄⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟
⠀⠀⠈⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟
⠀⠀⠀⠀⠻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠋
⠀⠀⠀⠀⠀⠈⠻⣶⣄⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣶⣤⣀⣤⡾⠟

      JE T AIMEEEEEEEEEEEEEEE <3
"""