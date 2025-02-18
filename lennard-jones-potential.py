import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################### paramètres ###############################

#constante physique :
SIGMA = 1 #distance at which the particle-particle potential energy V is zero
EPS = 1 #depth of the potential well
G = 0 #gravitation
K = 0 #frottement
M = 1 #masse dune particule
E = 1 #coefficient d'élasticité des rebonds, 1 si choque élastique (0 < E <= 1)
T = 2 # Temperature

#constante du problème :
L  = 10 #taille de la boite
NbrPart = 100 #nombre de particule
D = 2 #dimention du probléme

#Boundry condition :
REBOND = False #la particule rebondi sur les parroies True = oui, False = non (et les particules on des conditions aux bords periodique)

#constante de numérisation :
N = 5000 #pour la precision de Verlet
TEMPS = 1 #temps que l'on simule
EPSILON = TEMPS/N #epsilon dans Verlet
THERMALISATION_TIME = 5000

#pour l'aniamtion :
save_frames = True  #si on fait une annimation
save_animation = True #si on sauvegarde l'animation sur la machine
animation_interval = 5  #Intervalle pour l'animation (tout les combiens de step on sauvegarde les positions)

############################### fonctions ###############################

def animate_trajectory(positions_for_animation, L): #Animation des trajectoires de particule
    fig, ax = plt.subplots(figsize=(6,6))
    scat = ax.scatter([], [], s=20) #, color='blue'
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    #le titre depend des paramametres de depart
    title = "Potentiel de Lennard-Jones\n"
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

def init_lattice() : 
    position, position_before = [], []
    part_side = int(np.sqrt(NbrPart))
    spacing = L
    if part_side**2 < NbrPart :  #Si le nombre de particules n'est pas un carré parfait
        part_side += 1
    spacing = L/part_side
    for i in range(part_side) :
        for j in range(part_side) :
            if len(position) < NbrPart: 
                x = (i + 0.5) * spacing
                y = (j + 0.5) * spacing
                position.append([x, y])
    vx = np.random.normal(0.0, np.sqrt(T), NbrPart)  #Vitesses selon x
    vy = np.random.normal(0.0, np.sqrt(T), NbrPart)
    vx -= np.mean(vx) #Centrage des vitesses
    vy -= np.mean(vy)
    v = np.column_stack((vx, vy))
    position_before = position - EPSILON * v #pour utiliser la methode de résolution d'equation diff de Verlet
    position, position_before = thermalisation(np.array(position), np.array(position_before)) #on thermalise notre systeme
    return position, position_before

def simulate(position, position_before, j) :
    vitesses = (position - position_before) / EPSILON #vitesse des particules
    position_test = 2 * position - position_before + EPSILON * EPSILON * f(vitesses ,position, j * EPSILON) #calcule de la position d'apres avec Verlet
    position_before = position #on conserve la position de la particule juste avant
    
    #Boundry Condition au choix :
    
    if REBOND : # rebond sur la paroie :
        for i in range(NbrPart):  # Pour chaque particule
            j = 0
            for d in range(D) :
                while position_test[i][d] > L or position_test[i][d] < 0 :
                    if position_test[i][d] > L:  # Si la particule dépasse le bord supérieur
                        position_test[i][d] = (1 + E) * L - E * position_test[i][d]  # Inverser la position
                        position_before[i][d] = 2 * L - position_before[i][d]  # Inverser la vitesse 
                    elif position_test[i][d] < 0:  # Si la particule dépasse le bord inférieur
                        position_test[i][d] = - E * position_test[i][d]  # Inverser la position
                        position_before[i][d] = - position_before[i][d]  # Inverser la vitesse
                    j += 1
                    if j > 10 :
                        break
        position = np.array(position_test)
        
    else : #bords periodiques
        position = position_test%L #si par exemple x = L + 2 -> x = 2 pour rester dans la boite
    return position, position_before

def thermalisation(position, position_before) :
    for t in range(THERMALISATION_TIME) :
        position, position_before = simulate(position, position_before, t)
    return position, position_before

def lennardJ(ri,rj) : #force de Lennard Jones entre la particule en position r et celle en position rp
    rij = ri - rj
    if not(REBOND) :
        for d in range(D):
            if rij[d] >  L/2 :
                rij[d] -= L
            elif rij[d] < - L/2 :
                rij[d] += L
    norme = np.linalg.norm(rij) #calcule de la norme au carré
    return 48 * EPS *(SIGMA**12 * norme**(-12)-1/2* SIGMA**6* norme*(-6))* rij / norme**2

def gravity() : #force de gravité
    gravity_forces = [0,-G * M] #on peut mettre M[i] si on a un tableau de particule avec plusieur masse
    return gravity_forces

def friction(v) : # force frottements fluides
    friction_forces = - K * v
    return friction_forces
    
def f(v, r ,t) : #fonction dans l'équadiff r" = f(r', r, t)
    forces = []
    interaction_forces_matrix = []
    interaction_forces = []
    for i in range(NbrPart) : #je rempli un tableau NbrPart * NbrPart avec les Fij etant les forces de la particule i interagisant avec la particule j
        interaction_forces_matrix.append([])
        for j in range(NbrPart) :
            if i == j : #la particule n'interagie pas avec elle
                force_LJ = np.zeros(D)
            elif i > j : #le cas i j est antysimetrique a celui j i
                force_LJ = - interaction_forces_matrix[j][i]
            else : #on calcule la force
                force_LJ = lennardJ(r[i],r[j])
            interaction_forces_matrix[i].append(force_LJ) #+ d autre force d interaction si besoin
        interaction_forces.append(np.sum(interaction_forces_matrix[i],axis=0)) #on sommes la ligne i de la matrice = Sum Fij = Fi = Lennard jones appliqué sur i
        forces.append(gravity() + friction(v[i]) + interaction_forces[i])
    return np.array(forces)/M

############################### main ###############################

#init des positions
position, position_before = init_lattice()
positions_for_animation = [] #permet de stocker les positions que l'on souhaite utiliser pour l'animation

#calcul des trajectoires avec Verlet
for j in range(2,N-1) :
    position, position_before = simulate(position, position_before, j)

    # stock la position pour l'animation
    if save_frames and (j % animation_interval == 0) : #pour ne pas stocker inutilement
        positions_for_animation.append(np.copy(position))
        
# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)