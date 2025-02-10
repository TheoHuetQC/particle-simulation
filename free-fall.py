import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#constante physique
G = 1 #gravitation

#constante du probleme
L  = 10 #taille de la boite
NbrPart = 20 #nombre de particule

#constante de numérisation
N = 1000 #pour la precision de Verlet
temps = 10 #temps que l'on simule
E = temps/N #epsilon dans Verlet

#pour l'aniamtion
save_frames = True  #si on auvegarde l'animation
animation_interval = 5  #Intervalle pour l'animation

def animate_trajectory(positions_for_animation, L): #Animation des trajectoires de particule
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
        interval=50 #50ms -> 20fps
    )
    #ani.save("free-fall.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
    #plt.close(fig)
    plt.show()

def f(r,t) : #fonction dans l'équadiff r" = f(r,t)
    f = []
    for i in range(NbrPart) :
        #force appliqué sur chaque particule individuelement
        fx = 0 #composante x de la force
        fy = -G #   "      y      "
        f.append([fx,fy])
    return np.array(f)

#permet de stocker les positions que l'on souhaite utiliser pour l'animation
positions_for_animation = [] 

#init des positions
position = []
position_befor = []

for i in range(NbrPart) :
    #condition initial aléatoire pour chaque particule
    #r0
    r = np.random.uniform(0, L, 2)
    #v0
    v = np.random.normal(0, 1)
    theta = np.random.uniform(0, np.pi*2)

    #initialisation des premieres positions pour toute les particules
    position.append(r)
    position_befor.append([r[0] - E * v *np.cos(theta), r[1] - E * v*np.sin(theta)])

position = np.array(position)
position_befor = np.array(position_befor)

#calcul des trajectoires avec Verlet
for i in range(2,N-1) :
    position_test = np.array(2 * position - position_befor + E * E * f(position, i * E))
    position_befor = position

    #Boundry Condition :
    #periodic
    position = position_test%L

    #rebond sur la paroie :
    #pour x
    """
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

    # stock la position pour l'animation
    if save_frames and (i % animation_interval == 0) :
        positions_for_animation.append(np.copy(position))
        
# lance l'animation
if save_frames and len(positions_for_animation) > 1:
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)