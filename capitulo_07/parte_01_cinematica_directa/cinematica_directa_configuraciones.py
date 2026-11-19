
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import ET2

# Longitudes de los eslabones
L1 = 0.6
L2 = 0.4

# Modelo cinemático con transformaciones elementales
robot = (
    ET2.R()
    * ET2.tx(L1)
    * ET2.R()
    * ET2.tx(L2)
)

# Configuraciones articulares
configuraciones = {
    "A": [0, 0],
    "B": [30, 45],
    "C": [60, -30],
    "D": [90, 90]
}

# Representación gráfica
plt.figure(figsize=(7, 7))

# Evaluar cada configuración
for nombre, angulos in configuraciones.items():

    # Configuración articular
    q = np.deg2rad(angulos)

    # Cinemática directa con Robotics Toolbox
    T = robot.fkine(q)

    print(f"Configuración {nombre}:")
    print("Transformación homogénea:")
    print(T)
    print()

    # Posiciones de las articulaciones
    q1, q2 = q

    x0, y0 = 0.0, 0.0

    x1 = L1*np.cos(q1)
    y1 = L1*np.sin(q1)

    x2 = x1 + L2*np.cos(q1 + q2)
    y2 = y1 + L2*np.sin(q1 + q2)

    plt.plot(
        [x0, x1, x2],
        [y0, y1, y2],
        "o-",
        linewidth=3,
        markersize=8,
        label=f"{nombre}: ({angulos[0]}°, {angulos[1]}°)"
    )

plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Configuraciones articulares del manipulador 2R")
plt.grid(True)
plt.axis("equal")
plt.xlim(-1.1, 1.1)
plt.ylim(-1.1, 1.1)
plt.legend()
# Ejes coordenados
plt.axhline(y=0, color="black", linewidth=1.5)
plt.axvline(x=0, color="black", linewidth=1.5)

plt.show()
