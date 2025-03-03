import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

Nx = 100
Nt = 100000
L = 10
TEMPS = 100
dx = L/Nx
dt = TEMPS/Nt
D = 1
etha = D*dt/(dx*dx)

intervalTime = 100
save_animation = False
save_frames = True

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
        ani.save("transition-de-phase.mp4", writer="ffmpeg", fps=20) #pour sauvegarder l'animation en .mp4 avec ffmpeg
        plt.close(fig)
    else :
        plt.show()
        
#init
positions_for_animation = []
u = np.zeros((Nt,Nx))
for i in range(Nx) :
    u[0, i] = np.cos(i*dx) + np.sin(i*dx +2) +2 

#compute
for n in range(Nt-1) :
    positions = []
    for i in range(1,Nx-1) :
        u[n+1,i] = u[n,i] + etha * (u[n,i+1] - 2 * u[n,i] + u[n,i-1])
        positions.append([i*dx, u[n,i]])
    if n%intervalTime == 0 : 
        positions_for_animation.append(positions)
            
# lance l'animation
if save_frames and len(positions_for_animation) > 1 :
    animate_trajectory(positions_for_animation, L)