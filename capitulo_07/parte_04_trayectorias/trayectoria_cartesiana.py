
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.tools.trajectory import jtraj

# Configuraciones articulares
q0 = np.deg2rad([0, 0])
qf = np.deg2rad([60, -45])

# Vector de tiempo
T = 5.0
t = np.linspace(0, T, 251)

# Generación de trayectoria
traj = jtraj(q0, qf, t)

q = traj.q

# Trayectoria cartesiana
L1 = 0.6
L2 = 0.4

q1 = q[:, 0]
q2 = q[:, 1]

x = (
    L1*np.cos(q1)
    + L2*np.cos(q1+q2)
)

y = (
    L1*np.sin(q1)
    + L2*np.sin(q1+q2)
)

plt.figure(figsize=(7, 7))

plt.plot(x, y, label="Trayectoria cartesiana")

# Segmento recto entre las posiciones inicial y final
plt.plot(
    [x[0], x[-1]],
    [y[0], y[-1]],
    "--",
    color="gray",
    label="Trayectoria recta"
)

plt.scatter(x[0], y[0], label="Inicio")
plt.scatter(x[-1], y[-1], label="Final")

plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Trayectoria del efector final")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()
