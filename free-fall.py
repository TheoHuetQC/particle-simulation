import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 1

L  = 10
N = 1000
NbrPart = 5
temps = 10
E = temps/N

#pour l'aniamtion
save_frames = True  #Sauvegarde des images pour l'animation
animation_interval = 50   #Intervalle pour l'animation

def animate_trajectory(positions_for_animation, L): #Animation de la trajectoire
    fig, ax = plt.subplots(figsize=(6,6))
    scat = ax.scatter([], [], s=20) #, color='blue'
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_title("free-fall")
    
    def init():
        scat.set_offsets(np.empty((0, 2)))
        return (scat,)
    
    def update(frame_index):
        coords = positions_for_animation[frame_index]
        scat.set_offsets(coords)
        ax.set_title(f"Frame {frame_index}/{len(positions_for_animation)-1}")
        return (scat,)
    
    #print("Shape for animation:", positions_for_animation.shape)
    
    ani = animation.FuncAnimation(
        fig, update,
        frames=len(positions_for_animation),
        init_func=init,
        blit=True,
        interval=50
    )
    #ani.save("free-fall.mp4", writer="ffmpeg", fps=20)
    #plt.close(fig)
    plt.show()

def f(r,t) :
    fx = []
    fy = []
    for i in range(NbrPart) :
        f = 0
        g = 0
        fx.append(f)
        fy.append(g)
    return np.array([fx, fy])

positions_for_animation = []

#condition initial aléatoire
#r0
x0 = np.random.uniform(0, L, NbrPart)
y0 = np.random.uniform(0, L, NbrPart)

#v0
v = np.random.uniform(0, 1,NbrPart)
theta = np.random.uniform(0, np.pi*2, NbrPart)

position = np.array([x0, y0])
position_befor = np.array([position[0] - E * v *np.cos(theta), position[1] - E * v*np.sin(theta)])

#calcul des trajectoires avec Verlet
for i in range(2,N-1) :
    #Boundry Condition : 
    #periodic 
    position_test = 2 * position - position_befor + E * E * f(position, i * E)
    
    position_befor = position
    position = position_test%L
    #rebond sur la paroie :
    #pour x
    """
    position_test = 2 * position - position_befor + E * E #* f(position, i * E)
    
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
    """   

    # Animation
    if save_frames and (i % animation_interval == 0) :
        positions_for_animation.append(np.copy(position))
        
# Animation
if save_frames and len(positions_for_animation) > 1:
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)
"""
plt.figure()
for j in range(len(positions_for_animation)) :
    for i in range(NbrPart) :
        plt.scatter(positions_for_animation[j][0][i],positions_for_animation[j][1][i])
plt.show()"""