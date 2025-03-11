import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

############################### paramètres ###############################

#constante physique :
SIGMA = 1 #distance at which the particle-particle potential energy V is zero
EPS = 1 #depth of the potential well
G = 0 #gravitation
K = 0 #frottement
M = 1 #masse dune particule
E = 0.8 #coefficient d'élasticité des rebonds, 1 si choque élastique (0 < E <= 1)
KB = 1 #cst de Boltzman

#constante du problème :
L  = 10 #taille de la boite
NbrPart = 90 #nombre de particule
Ti = 35 # Temperature initial
Tf = 1 # T final
T_STEPS = 35 #nombre de pas de Température avant d atteindre Tf
TEMPERATURE = np.linspace(Ti, Tf, T_STEPS)
D = 2 #dimention du probléme

#Boundry condition :
REBOND = False #la particule rebondi sur les parroies True = oui, False = non (et les particules on des conditions aux bords periodique)

#constante de numérisation :
N = 30000 #pour la precision de Verlet
TIME = 10 #temps que l'on simule
EPSILON = TIME/N #epsilon dans Verlet
EQUILIBRE_TIME = 3 * N // T_STEPS
NU = 100

#pour l'aniamtion :
save_frames = True  #si on fait une annimation
save_animation = False #si on sauvegarde l'animation sur la machine
animation_interval = 5  #Intervalle pour l'animation (tout les combiens de step on sauvegarde les positions)

#pour les mesures :
mesure_interval = 100

############################### fonctions ###############################

def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(execution_time))

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
        ani.save("transition-de-phase.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
        plt.close(fig)
    else :
        plt.show()

def init_lattice(T) : 
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
    vx = np.random.normal(0.0, np.sqrt(KB * Ti / M), NbrPart)  #Vitesses selon x
    vy = np.random.normal(0.0, np.sqrt(KB * Ti / M), NbrPart)
    vx -= np.mean(vx) #Centrage des vitesses
    vy -= np.mean(vy)
    vitesses = np.column_stack((vx, vy))
    position, vitesses = equilibrium_state(np.array(position), vitesses, T) #on met notre système a la temperature T
    return position, vitesses

def PBC(position, vitesses) :
    #Boundry Condition au choix :
    if REBOND : # rebond sur la paroie :
        for i in range(NbrPart):  # Pour chaque particule
            j = 0
            for d in range(D) :
                while position[i][d] > L or position[i][d] < 0 :
                    if position[i][d] > L:  # Si la particule dépasse le bord supérieur
                        position[i][d] = 2 * L - position[i][d]  # Inverser la position
                        vitesses[i][d] = - E * vitesses[i][d]  # Inverser la vitesse 
                    elif position[i][d] < 0:  # Si la particule dépasse le bord inférieur
                        position[i][d] = - position[i][d]  # Inverser la position
                        vitesses[i][d] = - E * vitesses[i][d]  # Inverser la vitesse
                    j += 1
                    if j > 10 :
                        break
    else : #bords periodiques
        position = position%L #si par exemple x = L + 2 -> x = 2 pour rester dans la boite
    return position, vitesses

def simulate(position, vitesses, i, T) :
    #Verlet vitesse
    vitesses += 0.5 * f(vitesses, position, i * EPSILON) * EPSILON
    position += vitesses * EPSILON
    
    #application des PBC
    position, vitesses = PBC(position, vitesses)
         
    vitesses += 0.5 * f(vitesses, position, i * EPSILON) * EPSILON
         
    # Thermostat d'Andersen
    vitesses = apply_andersen_thermostat(vitesses, T)
    
    return position, vitesses

def equilibrium_state(position, vitesses, T) : #on laisse le systeme ce mettre a un etat d'équilibre apres sa génération
    for t in range(EQUILIBRE_TIME) :
        position, vitesses = simulate(position, vitesses, t, T)
    return position, vitesses

def compute_temperature(v) : #Calcule la température instantanée du système à partir des vitesses
    Ke = 0.5 * M * np.sum(v*v)  # Énergie cinétique totale
    N_d = NbrPart * D  # Nombre total de degrés de liberté
    T_inst = (2 * Ke) / (N_d)  # k_B = 1 en unités réduites
    return T_inst, Ke

def apply_andersen_thermostat(v, T): #Applique le thermostat d'Andersen en remplaçant aléatoirement les vitesses
    for i in range(NbrPart) :
        if np.random.rand() <= EPSILON * NU :  # Collision avec probabilité ν * dt
            v[i] = np.random.normal(0.0, np.sqrt(KB * T / M), D)  # Nouvelle vitesse
            #print("1", end = " ") #debugage pour savoir combien de fois ca a changer de vitesse
    return v

def lennardJ(ri,rj) : #force de Lennard Jones entre la particule en position ri et celle en position rj
    rij = ri - rj
    if not(REBOND) :
        for d in range(D):
            if rij[d] >  L/2 :
                rij[d] -= L
            elif rij[d] < - L/2 :
                rij[d] += L
    norme = np.linalg.norm(rij) #calcule de la norme au carré
    if norme > L/2 :
        return np.zeros(D)
    return 48 * EPS *(SIGMA**12 * norme**(-12)-1/2* SIGMA**6* norme*(-6))* rij / norme**2

def gravity(i) : #force de gravité
    gravity_forces = [0,-G * M] #on peut mettre M[i] si on a un tableau de plusieur masse pour les particules
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
        forces.append(gravity(i) + friction(v[i]) + interaction_forces[i])
    return np.array(forces)/M

############################### main ###############################

start_time = time.perf_counter()

#init des positions
T_int = 0 #la combientième temperature intermediaire a la quelle on est ici la premiere donc Ti
position, vitesses = init_lattice(TEMPERATURE[T_int])
print(f"0000/{N}, température visé : {TEMPERATURE[T_int]}, température acctuel : {compute_temperature(vitesses)}")

#init pour les résultats
positions_for_animation = [] #permet de stocker les positions que l'on souhaite utiliser pour l'animation
mesure_time, temperature_evolution, kinetic_evolution = [], [], []
T_inst, K_inst = 0, 0

#calcul des trajectoires avec Verlet
for i in range(N) :
    position, vitesses = simulate(position, vitesses, i, TEMPERATURE[T_int])

    #change de temperature tout les {N / len(TEMPERATURE)} pas jusqu'a atteindre Tf
    if N / len(TEMPERATURE) <= i - T_int * N / len(TEMPERATURE) :
        print(f"{i}/{N}, température visé : {TEMPERATURE[T_int]}, température acctuel : {temperature_evolution[-1]}")
        T_int += 1

    # stock la position pour l'animation et la température pour le graphique
    if save_frames and (i % animation_interval == 0) : #pour ne pas stocker inutilement
        positions_for_animation.append(np.copy(position))
    
    # mesure des moyennes de température
    T_temp, K_temp = compute_temperature(vitesses)
    T_inst += T_temp
    K_inst += K_temp
    if (i % mesure_interval == 0) :
        # mesure Température
        T_inst /= mesure_interval # fait une moyenne
        temperature_evolution.append(T_inst)
        T_inst = 0

        # mesure de l'énérgie cinetique
        K_inst /= mesure_interval # fait une moyenne
        kinetic_evolution.append(K_inst)
        K_inst = 0

        # temps ou on a fait la mesure
        mesure_time.append(i*EPSILON)
        
print(f"{N}/{N}, température visé : {TEMPERATURE[T_int]}, température acctuel : {temperature_evolution[-1]}")

#temps que met le programme
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Programme exécuté en : {convert(execution_time)}")

# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    positions_for_animation = np.array(positions_for_animation)
    animate_trajectory(positions_for_animation, L)

# affiche les courbes de mesures
plt.plot(mesure_time, temperature_evolution)
plt.xlabel("Temps")
plt.ylabel("Température")
plt.title("Évolution de la température")
plt.show()