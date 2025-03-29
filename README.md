# 🌌 Particle Simulation  

A collection of **numerical simulations** modeling particle interactions using the **Verlet integration method**.  

This project explores:  
✔️ **Gravitational motion** (free-fall simulation)  
✔️ **Interacting particles with the Lennard-Jones potential**  
✔️ **Phase transitions using the Andersen thermostat**  

---

## 🚀 Project Overview  

### 1️⃣ **Free-Fall Simulation (Introduction to Verlet Integration)**  
- Simulates a **particle under gravity** using the Verlet algorithm.  
- Demonstrates the accuracy of **symplectic integration** over time.  
- **Visualized with Matplotlib animations** [free-fall.mp4](free-fall/free-fall.mp4)  
- **Code:** [free-fall.py](free-fall/free-fall.py)

### 2️⃣ **Lennard-Jones Potential (Particle Interactions)**  
- Models **interactions between particles** using the **Lennard-Jones potential**.  
- Simulates **attractive and repulsive forces** at different distances.  
- Used to study **molecular interactions** and **phase behavior**.  
- **Visualization:** [lennard-jones.mp4](lennard-jones/lennard-jones.mp4)  
- **Code:** [lennard-jones.py](lennard-jones/lennard-jones.py)

### 3️⃣ **Phase Transition Simulation (Liquid-Solid Transition)**  
- Implements a **2D phase transition** from liquid to solid.  
- Uses the **Andersen thermostat** to control temperature.  
- Demonstrates the emergence of **crystalline structures** from disordered motion.  
- Result : ![phase-transition-Temperature.png](phase-transition/phase-transition-Temperature.png)  
- **Visualization:** [phase-transition.mp4](phase-transition/phase-transition.mp4)  
- **Code:** [phase-transition.py](phase-transition/phase-transition.py)

---

## 🛠 Installation & Dependencies  

Ensure you have Python **3.7+** and install the required libraries:  

```bash
pip install numpy matplotlib
```

---

## 🚀 Usage

Run any of the simulations with:

```bash
python free-fall/free-fall.py
python lennard-jones/lennard-jones-potential.py
python phase-transition/phase-transition.py
```
Animations and results will be displayed automatically.

---


## 📂 Project Structure

```bash
📂 particle-simulation/
│
├── 📂 free-fall
│    ├── 📝 free-fall.py (Gravitational simulation using Verlet method)
│    └── 🎥 free-fall.mp4 (Animation of a free-fall simulation)
│
├── 📂 lennard-jones
│    ├── 📝 lennard-jones-potential.py (Simulation of Lennard-Jones interactions)
│    └── 🎥 lennard-jones.mp4 (Particle interaction using Lennard-Jones potential)
│
└── 📂 
│    ├── 📝 transition de phase.py (2D phase transition with Andersen thermostat)
│    ├── 🎥 transition-de-phase.mp4 (Phase transition simulation output)
│    └── 📊 transition_de_phase-Temperature.png (Temperature evolution during phase transition)
│
└── 📜 README.md (This file)
```

---

## 🤝 Contributions & Contact

Contributions are welcome! You can:

- Fork the repository and improve the simulations.

- Submit a pull request for enhancements or bug fixes.

- Open an issue for discussions or questions.

📩 Feel free to reach out for any suggestions!

## 🚀 Happy simulating!
