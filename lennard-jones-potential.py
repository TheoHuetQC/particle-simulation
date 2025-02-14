import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################### paramètres ###############################

#constante physique
SIGMA = 1 #distance at which the particle-particle potential energy V is zero
EPS = 1 #depth of the potential well
G = 0 #gravitation
K = 0 #frottement
M = 1 #masse dune particule
E = 0.5 #coefficient d'élasticité des rebonds, 1 si choque élastique (0 < E <= 1)

#constante du problème
L  = 10 #taille de la boite
NbrPart = 20 #nombre de particule

#Boundry condition :
REBOND = False #la particule rebondi sur les parroies True = oui, False = non (et les particules on des conditions aux bords periodique)

#constante de numérisation
N = 1000 #pour la precision de Verlet
TEMPS = 10 #temps que l'on simule
EPSILON = TEMPS/N #epsilon dans Verlet

#pour l'aniamtion
save_frames = True  #si on fait une annimation
save_animation = False #si on sauvegarde l'animation sur la machine
animation_interval = 5  #Intervalle pour l'animation (tout les combiens de step on sauvegarde les positions)

############################### fonctions ###############################

def animate_trajectory(positions_for_animation, L): #Animation des trajectoires de particule
    fig, ax = plt.subplots(figsize=(6,6))
    scat = ax.scatter([], [], s=20) #, color='blue'
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    #le titre depend des paramametres de depart
    title = "Potentiel de Lennard-Jones"
    title += " avec rebonds" if REBOND else " avec conditions periodiques aux bords"
    title += ", (N = " + str(NbrPart) + ")"
    title += ", \nGravité (G = " + str(G) + ")" if (G != 0) else "\n"
    title += ", coefficient d'Elasticité (E = " + str(E) + ")" if (E != 1 and REBOND) else ""
    title += "\n et Frottements fluide/particules (K = "+ str(K) +")" if (K != 0) else ""
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
        ani.save("lennard-jones.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
        plt.close(fig)
    else :
        plt.show()

def force_LJ(r,rp) : #force de Lennard Jones entre la particule en position r et celle en position rp
    rij = r - rp
    norme2 = np.linalg.norm(rij) #calcule de la norme au carré
    return 48 * EPS *(SIGMA**12 * norme2**(-12)-1/2* SIGMA**6* norme2*(-6))* rij / norme2

def forces_LJ(r) : #je rempli un tableau NbrPart x NbrPart avec les Fij etant les forces de la particule i avec la particule j
    forces = []
    for i in range(NbrPart) :
        forces.append([])
        for j in range(NbrPart) :
            if i == j : #la particule n'interagie pas avec elle
                forces[i].append(np.zeros(2))
            elif i > j : #le cas i j est antysimetrique a celui j i
                forces[i].append(- forces[j][i])
            else : #on calcule la force
                forces[i].append(force_LJ(r[i],r[j]))
    return np.array(forces)

def f(v, r ,t) : #fonction dans l'équadiff r" = f(r', r, t)
    f = []
    for i in range(NbrPart) :
        #force appliqué sur chaque particule individuelement ici F = P + f avec P = MG le poid et f = -K*vitesse les frottements du a l'aire
        fx = 0 - (K* v[i,0]) - np.sum(forces_LJ(r)[i][0])#composante x de la force
        fy = -(G * M) - (K* v[i,1]) + np.sum(forces_LJ(r)[i][1]) #  " y    "
        f.append([fx/ M,fy/ M])
    return np.array(f)

############################### main ###############################

#init des positions
position = []
position_before = []
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
    position_before.append([r[0] - EPSILON * v *np.cos(theta), r[1] - EPSILON * v*np.sin(theta)]) #pour utiliser la methode de résolution d'equation diff de Verlet

position = np.array(position)
position_before = np.array(position_before)

#calcul des trajectoires avec Verlet
for j in range(2,N-1) :
    vitesses = (position - position_before) / EPSILON #vitesse des particules
    position_test = 2 * position - position_before + EPSILON * EPSILON * f(vitesses ,position, j * EPSILON) #calcule de la position d'apres avec Verlet
    position_before = position #on conserve la position de la particule juste avant
    
    #Boundry Condition au choix :
    
    if REBOND : # rebond sur la paroie :
        for i in range(NbrPart):  # Pour chaque particule
            # Pour x
            if position_test[i][0] > L:  # Si la particule dépasse le bord droit
                position_test[i][0] = (1 + E) * L - E * position_test[i][0]  # Inverser la position
                position_before[i][0] = 2 * L - position_before[i][0]  # Inverser la vitesse en x
            elif position_test[i][0] < 0:  # Si la particule dépasse le bord gauche
                position_test[i][0] = - E * position_test[i][0] # Inverser la position
                position_before[i][0] = - position_before[i][0]  # Inverser la vitesse en x
            # Pour y
            if position_test[i][1] > L:  # Si la particule dépasse le bord supérieur
                position_test[i][1] = (1 + E) * L - E * position_test[i][1]  # Inverser la position
                position_before[i][1] = 2 * L - position_before[i][1]  # Inverser la vitesse en y
            elif position_test[i][1] < 0:  # Si la particule dépasse le bord inférieur
                position_test[i][1] = - E * position_test[i][1]  # Inverser la position
                position_before[i][1] = - position_before[i][1]  # Inverser la vitesse en y
        position = np.array(position_test)
    else : #bords periodiques
        position = position_test%L #si par exemple x = L + 2 -> x = 2 pour rester dans la boite

    # stock la position pour l'animation
    if save_frames and (j % animation_interval == 0) : #pour ne pas stocker inutilement
        positions_for_animation.append(np.copy(position))
        
# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)
