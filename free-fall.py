import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################### paramètres ###############################

#constante physique
G = 10 #gravitation
K = 0.5 #frottement
M = 1 #masse dune particule

#constante du probleme
L  = 10 #taille de la boite
NbrPart = 20 #nombre de particule

#Boundry condition :
REBOND = True #la particule rebondi sur les parroies True = oui, False = non (et les particules on des conditions aux bords periodique)

#constante de numérisation
N = 1000 #pour la precision de Verlet
temps = 10 #temps que l'on simule
E = temps/N #epsilon dans Verlet

#pour l'aniamtion
save_frames = True  #si on auvegarde l'animation
animation_interval = 5  #Intervalle pour l'animation

############################### fonctions ###############################

def animate_trajectory(positions_for_animation, L): #Animation des trajectoires de particule
    fig, ax = plt.subplots(figsize=(6,6))
    scat = ax.scatter([], [], s=20) #, color='blue'
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    title = "free-fall"
    title += " avec rebonds" if REBOND else " avec conditions periodiques aux bords"
    title += ", \nGravité" if (G != 0) else "\n"
    title += " et Frottement de l'aire." if (K != 0) else "."
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
    #ani.save("free-fall.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
    #plt.close(fig)
    plt.show()

def f(v, r ,t) : #fonction dans l'équadiff r" = f(v, r, t)
    f = []
    for i in range(NbrPart) :
        #force appliqué sur chaque particule individuelement ici F = P + f avec P = MG le poid et f = -K*vitesse les frottements du a l'aire
        fx = 0 - (K* v[i,0]) #composante x de la force
        fy = -(G * M) - (K* v[i,1]) #   "      y      "
        f.append([fx/ M,fy/ M])
    return np.array(f)

#init des positions
position = []
position_befor = []
positions_for_animation = [] #permet de stocker les positions que l'on souhaite utiliser pour l'animation

for i in range(NbrPart) :
    #condition initial aléatoire pour chaque particule
    #r0
    r = np.random.uniform(0, L, 2)
    #v0
    v = np.random.normal(0, 1)
    theta = np.random.uniform(0, np.pi*2)

    #initialisation des premieres positions pour toute les particules
    position.append(r)
    position_befor.append([r[0] - E * v *np.cos(theta), r[1] - E * v*np.sin(theta)]) #pour utiliser la methode de résolution d'equation diff de Verlet

position = np.array(position)
position_befor = np.array(position_befor)

#calcul des trajectoires avec Verlet
for j in range(2,N-1) :
    vitesses = (position - position_befor) / E #vitesse des particules
    position_test = 2 * position - position_befor + E * E * f(vitesses ,position, j * E) #calcule de la position d'apres avec Verlet
    position_befor = position #on conserve la position de la particule juste avant
    
    #Boundry Condition au choix :
    
    if REBOND : # rebond sur la paroie :
        for i in range(NbrPart):  # Pour chaque particule
            # Pour x
            if position_test[i][0] > L:  # Si la particule dépasse le bord droit
                position_test[i][0] = 2 * L - position_test[i][0]  # Inverser la position
                position_befor[i][0] = 2 * L - position_befor[i][0]  # Inverser la vitesse en x
            elif position_test[i][0] < 0:  # Si la particule dépasse le bord gauche
                position_test[i][0] = -position_test[i][0]  # Inverser la position
                position_befor[i][0] = -position_befor[i][0]  # Inverser la vitesse en x
            # Pour y
            if position_test[i][1] > L:  # Si la particule dépasse le bord supérieur
                position_test[i][1] = 2 * L - position_test[i][1]  # Inverser la position
                position_befor[i][1] = 2 * L - position_befor[i][1]  # Inverser la vitesse en y
            elif position_test[i][1] < 0:  # Si la particule dépasse le bord inférieur
                position_test[i][1] = -position_test[i][1]  # Inverser la position
                position_befor[i][1] = -position_befor[i][1]  # Inverser la vitesse en y
        position = np.array(position_test)
    else : #bords periodiques
        position = position_test%L #si x = L + 2 -> x = 2 pour rester dans la boite

    # stock la position pour l'animation
    if save_frames and (j % animation_interval == 0) : #pour ne pas stocker inutilement
        positions_for_animation.append(np.copy(position))
        
# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)
