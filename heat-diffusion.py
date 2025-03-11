import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

############################### paramètres ###############################

#constante physique :
D = 1 #coefficient de diffusion

#constante du problème :
L = 10
TEMPS = 100

#Boundry condition :
#a gauche
NEUMANN_LEFT = True # si le bord est adiabatique
THERMOSTAT_LEFT = False #on a un thermostat au bord
WALL_LEFT = False #on a une paroie qui laisse passer la chaleur
ALPHA_LEFT = 0.8 #coefficient de transmition du bord
T_LEFT = 5 #température du Thermostat
#a droite
NEUMANN_RIGHT = False
THERMOSTAT_RIGHT = False
WALL_RIGHT = True
ALPHA_RIGHT = 0.8
T_RIGHT = 0 

#constante de numérisation :
Nx = 100 #nombre de point de position
Nt = 1000*TEMPS #pas de temps
dx = L/Nx
dt = TEMPS/Nt
etha = D*dt/(dx*dx) #dans l'équation de diffusion

#pour l'aniamtion :
animation_interval = 100  #Intervalle pour l'animation (tout les combiens de step on sauvegarde les positions)
save_animation = False #si on sauvegarde l'animation sur la machine
save_frames = True  #si on fait une annimation

############################### fonctions ###############################

def animate_trajectory(positions_for_animation, L): #Animation des trajectoires de particule
    fig, ax = plt.subplots(figsize=(6,6))
    scat = ax.scatter([], [], s=20) #, color='blue'
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    #le titre depend des paramametres de depart
    title = "diffusion de Température"
    ax.set_title(title)
    
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
    if save_animation :
        ani.save("heat-diffusion.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
        plt.close(fig)
    else :
        plt.show()

def T(x) : #valeurs de la température au depart, on peut mettre nimporte quel fonctions meme discontinue...
    return np.cos(x) + np.sin(x + 2) + 2 

############################### main ###############################

#initialisation
positions_for_animation = []

u = np.zeros((Nt,Nx))
for i in range(Nx) : #condition initiale
    u[0, i] = T(i*dx)

#compute
for n in range(Nt-1) :
    positions = []
    for i in range(1,Nx-1) :
        #resoud la PDE
        u[n+1,i] = u[n,i] + etha * (u[n,i+1] - 2 * u[n,i] + u[n,i-1])
        positions.append([i*dx, u[n,i]]) #pour plot
    
    #boundry condition
    #a gauche
    if THERMOSTAT_LEFT : #Dirichlet condition (Thermostat au bord a température T_LEFT)
        u[n+1, 0] = T_LEFT
    elif NEUMANN_LEFT : #Neumann condition (la derivé au bord est 0 mur adiabatique)
        u[n+1, 0] = u[n+1, 1]
    elif WALL_LEFT : #on a un mur qui transmet de l'energie depuis l exterieur de la boite avec un coefficient alpha
        u[n+1, 0] = ALPHA_LEFT * (T_LEFT - u[n, 0]) * dx + u[n+1, 1]

    #a droite
    if THERMOSTAT_RIGHT : #Dirichlet condition (Thermostat au bord a température T_RIGHT)
        u[n+1, Nx-1] = T_RIGHT
    elif NEUMANN_RIGHT : #Neumann condition (la derivé au bord est 0 mur adiabatique)
        u[n+1, Nx-1] = u[n+1, Nx-2]
    elif WALL_RIGHT : #on a un mur qui transmet de l'energie depuis l exterieur de la boite avec un coefficient alpha
        u[n+1, Nx-1] = ALPHA_RIGHT * (T_RIGHT - u[n, Nx-1]) * dx + u[n+1, Nx-2]
    else : #condition periodique
        for i in [0,-1] :
            u[n+1,i] = u[n,i] + etha * (u[n,i+1] - 2 * u[n,i] + u[n,i-1])
        
    if n % animation_interval  == 0 : #on sauvegarde les positions pour les annimées tout les "animation_interval" pas 
        positions_for_animation.append(positions)

# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    animate_trajectory(positions_for_animation, L)
