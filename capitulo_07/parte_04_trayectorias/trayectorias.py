
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.tools.trajectory import jtraj

# Configuraciones articulares
q0 = np.deg2rad([0, 0])
qf = np.deg2rad([60, -45])

# Vector de tiempo
T = 3.0
t = np.linspace(0, T, 251)

# Generación de trayectoria
traj = jtraj(q0, qf, t)

q = traj.q
qd = traj.qd
qdd = traj.qdd

# Gráficas
fig, axes = plt.subplots(3, 1, figsize=(8, 9))

datos = [q, qd, qdd]

titulos = [
    "Posiciones articulares",
    "Velocidades articulares",
    "Aceleraciones articulares"
]

unidades = [
    "Posición [°]",
    "Velocidad [°/s]",
    "Aceleración [°/s²]"
]

for ax, valores, titulo, unidad in zip(
    axes, datos, titulos, unidades
):
    ax.plot(
        t,
        np.rad2deg(valores[:, 0]),
        label="Articulación 1"
    )

    ax.plot(
        t,
        np.rad2deg(valores[:, 1]),
        label="Articulación 2"
    )

    ax.set_title(titulo)
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel(unidad)
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.show()
